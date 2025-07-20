# src/models.py

import uuid
import logging
import yaml
import heapq
from src.reporter import Reporter # <-- New import

# ... (Message and Node classes are unchanged) ...
class Message:
    """Represents a data packet moving through the network."""
    def __init__(self, source_id, destination_id, payload):
        self.id = str(uuid.uuid4())
        self.source_id = source_id
        self.destination_id = destination_id
        self.payload = payload
        logging.info(f"Message {self.id} created from {source_id} to {destination_id}")


class Node:
    """Represents a single communications node in the network."""
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.neighbors = {} # {neighbor_node: latency}
        self.is_active = True
        logging.info(f"Node '{self.name}' created with ID {self.id}")

    def take_offline(self):
        self.is_active = False
        logging.warning(f"Node '{self.name}' has been taken OFFLINE.")

    def bring_online(self):
        self.is_active = True
        logging.info(f"Node '{self.name}' has been brought ONLINE.")

    def add_neighbor(self, neighbor_node, latency):
        """Establishes a bilateral connection to another node with a given latency."""
        if neighbor_node not in self.neighbors:
            self.neighbors[neighbor_node] = latency
            neighbor_node.neighbors[self] = latency # Make the connection two-way
            logging.info(f"Node '{self.name}' connected to '{neighbor_node.name}' with latency {latency}ms")

    def receive_message(self, message):
        if message.destination_id == self.id:
            logging.info(f"Node '{self.name}' ({self.id}) received final message: '{message.payload}'")
            return True
        else:
            logging.warning(f"Node '{self.name}' received message intended for {message.destination_id}. Discarding.")
            return False

class Network:
    def __init__(self, reporter=None):
        self.nodes = {}
        self.reporter = reporter if reporter else self._create_dummy_reporter()

    def _create_dummy_reporter(self):
        class DummyReporter:
            def log_routing_attempt(self, *args, **kwargs): pass
        return DummyReporter()

    def add_node(self, node):
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            logging.info(f"Node '{node.name}' added to the network.")
    
    def get_node_by_name(self, name):
        for node in self.nodes.values():
            if node.name == name:
                return node
        return None

    def get_node(self, node_id):
        return self.nodes.get(node_id)
    
    # --- NEW METHOD for AEGIS-11 ---
    def set_link_latency(self, node1_name, node2_name, new_latency):
        """Updates the latency of an existing link between two nodes."""
        node1 = self.get_node_by_name(node1_name)
        node2 = self.get_node_by_name(node2_name)

        if not node1 or not node2:
            logging.error(f"Set latency failed: Node '{node1_name or node2_name}' not found.")
            return False

        # Check if they are actually neighbors before trying to update
        if node2 in node1.neighbors:
            node1.neighbors[node2] = new_latency
            node2.neighbors[node1] = new_latency # Update the bilateral link
            logging.info(f"Updated latency between '{node1.name}' and '{node2.name}' to {new_latency}ms.")
            return True
        else:
            logging.warning(f"Set latency failed: No direct link exists between '{node1.name}' and '{node2.name}'.")
            return False

    @classmethod
    def create_from_config(cls, config_path, reporter=None):
        # ... (This method is unchanged) ...
        network = cls(reporter=reporter)
        name_to_node_map = {}
        with open(config_path, 'r') as f: config = yaml.safe_load(f)
        for node_data in config.get('nodes', []):
            node_name = node_data['name']
            if node_name not in name_to_node_map:
                node = Node(name=node_name)
                network.add_node(node)
                name_to_node_map[node_name] = node
        for link_data in config.get('links', []):
            node1_name, node2_name, latency = link_data
            node1, node2 = name_to_node_map.get(node1_name), name_to_node_map.get(node2_name)
            if node1 and node2:
                node1.add_neighbor(node2, int(latency))
        return network

    def find_shortest_path(self, start_node_id, end_node_id):
        # ... (This method is unchanged) ...
        start_node, end_node = self.get_node(start_node_id), self.get_node(end_node_id)
        if not all([start_node, end_node, start_node.is_active, end_node.is_active]):
            return None, float('inf')
        distances = {node_id: float('inf') for node_id in self.nodes}
        distances[start_node_id] = 0
        previous_nodes = {node_id: None for node_id in self.nodes}
        pq = [(0, start_node_id)]
        while pq:
            current_latency, current_node_id = heapq.heappop(pq)
            if current_latency > distances[current_node_id]: continue
            current_node = self.get_node(current_node_id)
            if not current_node.is_active: continue
            if current_node_id == end_node_id: break
            for neighbor, latency in current_node.neighbors.items():
                if not neighbor.is_active: continue
                distance = current_latency + latency
                if distance < distances[neighbor.id]:
                    distances[neighbor.id] = distance
                    previous_nodes[neighbor.id] = current_node
                    heapq.heappush(pq, (distance, neighbor.id))
        path = []
        current_node = end_node
        while current_node is not None:
            path.insert(0, current_node)
            current_node = previous_nodes.get(current_node.id)
        if path and path[0] == start_node:
            return path, distances[end_node_id]
        return None, float('inf')

    def route_message(self, message):
        # ... (This method is unchanged) ...
        source_node, dest_node = self.get_node(message.source_id), self.get_node(message.destination_id)
        if not source_node or not dest_node: return False
        path, total_latency = self.find_shortest_path(source_node.id, dest_node.id)
        if not path:
            self.reporter.log_routing_attempt(message, source_node, dest_node, None, 0, False)
            return False
        success = path[-1].receive_message(message)
        self.reporter.log_routing_attempt(message, source_node, dest_node, path, total_latency, success)
        return success
