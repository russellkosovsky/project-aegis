# src/models.py

import uuid
import logging
import yaml # <-- Import the new library

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

    # --- NEW METHOD ---
    @classmethod
    def create_from_config(cls, config_path):
        """
        Factory method to create and configure a Network instance from a YAML file.
        """
        network = cls()
        name_to_node_map = {}

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # First pass: create all the nodes
        logging.info("Creating nodes from config...")
        for node_data in config.get('nodes', []):
            node_name = node_data['name']
            if node_name not in name_to_node_map:
                node = Node(name=node_name)
                network.add_node(node)
                name_to_node_map[node_name] = node

        # Second pass: create all the links
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