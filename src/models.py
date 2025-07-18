# src/models.py

import uuid
import logging
import yaml
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ... (Message class is unchanged) ...
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
        self.neighbors = []
        self.is_active = True # --- NEW ATTRIBUTE ---
        logging.info(f"Node '{self.name}' created with ID {self.id}")

    # --- NEW METHODS ---
    def take_offline(self):
        """Sets the node's status to inactive."""
        self.is_active = False
        logging.warning(f"Node '{self.name}' has been taken OFFLINE.")

    def bring_online(self):
        """Sets the node's status to active."""
        self.is_active = True
        logging.info(f"Node '{self.name}' has been brought ONLINE.")

    # ... (add_neighbor and receive_message are unchanged) ...
    def add_neighbor(self, neighbor_node):
        """Establishes a bilateral connection to another node."""
        if neighbor_node not in self.neighbors:
            self.neighbors.append(neighbor_node)
            neighbor_node.neighbors.append(self) # Make the connection two-way
            logging.info(f"Node '{self.name}' is now connected to '{neighbor_node.name}'")

    def receive_message(self, message):
        """Handles an incoming message for this node."""
        if message.destination_id == self.id:
            logging.info(f"Node '{self.name}' ({self.id}) received final message: '{message.payload}'")
            return True
        else:
            logging.warning(f"Node '{self.name}' received message intended for {message.destination_id}. Discarding.")
            return False


class Network:
    # ... (init, add_node, get_node_by_name, get_node, send_direct_message, create_from_config are unchanged) ...
    def __init__(self):
        self.nodes = {} # A dictionary to store nodes by their ID for quick lookup

    def add_node(self, node):
        """Adds a node to the network."""
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            logging.info(f"Node '{node.name}' added to the network.")
    
    def get_node_by_name(self, name):
        """Retrieves a node from the network by its unique name."""
        for node in self.nodes.values():
            if node.name == name:
                return node
        return None

    def get_node(self, node_id):
        """Retrieves a node from the network by its ID."""
        return self.nodes.get(node_id)

    def send_direct_message(self, message):
        """
        Sends a message from a source node to a destination node
        if they are direct neighbors.
        """
        source_node = self.get_node(message.source_id)
        destination_node = self.get_node(message.destination_id)

        if not source_node or not destination_node:
            logging.error("Source or Destination node not found in the network.")
            return False

        if destination_node in source_node.neighbors:
            logging.info(f"Attempting to send message from '{source_node.name}' to neighbor '{destination_node.name}'...")
            return destination_node.receive_message(message)
        else:
            logging.warning(f"Failed to send: '{destination_node.name}' is not a direct neighbor of '{source_node.name}'.")
            return False

    @classmethod
    def create_from_config(cls, config_path):
        """
        Factory method to create and configure a Network instance from a YAML file.
        """
        network = cls()
        name_to_node_map = {}

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        logging.info("Creating nodes from config...")
        for node_data in config.get('nodes', []):
            node_name = node_data['name']
            if node_name not in name_to_node_map:
                node = Node(name=node_name)
                network.add_node(node)
                name_to_node_map[node_name] = node

        logging.info("Creating links between nodes...")
        for link_data in config.get('links', []):
            node1_name, node2_name = link_data
            node1 = name_to_node_map.get(node1_name)
            node2 = name_to_node_map.get(node2_name)

            if node1 and node2:
                node1.add_neighbor(node2)
            else:
                logging.error(f"Could not create link: Node not found for '{node1_name}' or '{node2_name}'")
        
        return network

    # --- MODIFIED METHOD ---
    def find_shortest_path(self, start_node_id, end_node_id):
        """
        Finds the shortest path between two nodes using Breadth-First Search (BFS),
        avoiding any nodes that are not active.
        """
        start_node = self.get_node(start_node_id)
        end_node = self.get_node(end_node_id)

        if not start_node or not end_node:
            logging.error("Pathfinding error: Start or end node not in network.")
            return None
        
        # --- CRITICAL CHANGE: Check if start or end nodes are offline ---
        if not start_node.is_active or not end_node.is_active:
            logging.warning("Pathfinding error: Start or end node is offline.")
            return None

        queue = deque([[start_node]])
        visited = {start_node.id}

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == end_node:
                return path

            for neighbor in node.neighbors:
                # --- CRITICAL CHANGE: Only consider active neighbors ---
                if neighbor.id not in visited and neighbor.is_active:
                    visited.add(neighbor.id)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        
        logging.warning(f"No path found between '{start_node.name}' and '{end_node.name}'")
        return None