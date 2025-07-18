# tests/test_models.py

from src.models import Node

def test_node_creation():
    """Tests that a Node object is created with a name and a unique ID."""
    node1 = Node(name="Ground Station Alpha")
    assert node1.name == "Ground Station Alpha"
    assert node1.id is not None
    assert len(node1.neighbors) == 0

def test_add_neighbor():
    """Tests that we can connect two nodes together."""
    node1 = Node(name="Command Center")
    node2 = Node(name="Mobile Unit 7")
    node1.add_neighbor(node2)
    assert len(node1.neighbors) == 1
    assert node1.neighbors[0] == node2
