# src/models.py

import uuid
import logging
import yaml
from collections import deque # <-- Import deque for an efficient queue

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ... (Message and Node classes remain the same) ...
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
        self.neighbors = [] # A list of other Node objects it's connected to
        logging.info(f"Node '{self.name}' created with ID {self.id}")

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
    """Manages the collection of all nodes and their connections."""
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

    # --- NEW METHOD ---
    def find_shortest_path(self, start_node_id, end_node_id):
        """
        Finds the shortest path between two nodes using Breadth-First Search (BFS).
        Returns a list of Node objects representing the path, or None if no path exists.
        """
        start_node = self.get_node(start_node_id)
        end_node = self.get_node(end_node_id)

        if not start_node or not end_node:
            logging.error("Pathfinding error: Start or end node not in network.")
            return None

        # A queue to store the paths to explore. We start with a path containing only the start_node.
        queue = deque([[start_node]])
        # A set to keep track of visited nodes to prevent cycles and redundant work.
        visited = {start_node.id}

        while queue:
            # Get the first path from the queue
            path = queue.popleft()
            # Get the last node from the path
            node = path[-1]

            # If we've reached the destination, we've found the shortest path
            if node == end_node:
                return path

            # Explore the neighbors of the current node
            for neighbor in node.neighbors:
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    # Create a new path by extending the current one and add it to the queue
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        
        # If the queue is empty and we haven't found a path, none exists
        logging.warning(f"No path found between '{start_node.name}' and '{end_node.name}'")
        return None