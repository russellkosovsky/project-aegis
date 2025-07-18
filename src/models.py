# src/models.py

import uuid
import logging

# It's good practice to set up a logger for better output.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

        # Check if the destination is a direct neighbor of the source
        if destination_node in source_node.neighbors:
            logging.info(f"Attempting to send message from '{source_node.name}' to neighbor '{destination_node.name}'...")
            return destination_node.receive_message(message)
        else:
            logging.warning(f"Failed to send: '{destination_node.name}' is not a direct neighbor of '{source_node.name}'.")
            return False