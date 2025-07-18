# src/models.py

import uuid

class Message:
    """Represents a data packet moving through the network."""
    def __init__(self, source_id, destination_id, payload):
        self.source_id = source_id
        self.destination_id = destination_id
        self.payload = payload
        print(f"New message created from {source_id} to {destination_id}")

class Node:
    """Represents a single communications node in the network."""
    def __init__(self, name):
        self.id = str(uuid.uuid4()) # Each node gets a unique ID
        self.name = name
        self.neighbors = [] # A list of other Node objects it's connected to
        print(f"Node '{self.name}' created with ID {self.id}")

    def add_neighbor(self, neighbor_node):
        """Establishes a connection to another node."""
        self.neighbors.append(neighbor_node)
        print(f"Node '{self.name}' is now connected to '{neighbor_node.name}'")
