# tests/test_models.py

from src.models import Node, Message, Network

# --- Existing Tests for Node ---
def test_node_creation():
    """Tests that a Node object is created with a name and a unique ID."""
    node1 = Node(name="Ground Station Alpha")
    assert node1.name == "Ground Station Alpha"
    assert node1.id is not None
    assert len(node1.neighbors) == 0

def test_add_neighbor_is_bilateral():
    """Tests that connecting two nodes works in both directions."""
    node1 = Node(name="Command Center")
    node2 = Node(name="Mobile Unit 7")
    node1.add_neighbor(node2)
    
    # Check that node2 is in node1's neighbors
    assert node2 in node1.neighbors
    # Check that node1 is in node2's neighbors (bilateral connection)
    assert node1 in node2.neighbors

# --- New Tests for Network and Messaging ---

def test_network_add_node():
    """Tests that a node can be successfully added to the network."""
    network = Network()
    node = Node("Test Node")
    network.add_node(node)
    
    assert len(network.nodes) == 1
    assert network.get_node(node.id) == node

def test_send_direct_message_success():
    """Tests successfully sending a message between two direct neighbors."""
    network = Network()
    node_a = Node("Node A")
    node_b = Node("Node B")
    
    network.add_node(node_a)
    network.add_node(node_b)
    
    node_a.add_neighbor(node_b)
    
    message = Message(source_id=node_a.id, destination_id=node_b.id, payload="Hello from A")
    
    # The send operation should be successful
    assert network.send_direct_message(message) is True

def test_send_direct_message_failure_not_neighbors():
    """Tests that a message cannot be sent between two nodes that are not neighbors."""
    network = Network()
    node_a = Node("Node A")
    node_b = Node("Node B")
    node_c = Node("Node C") # An unconnected node
    
    network.add_node(node_a)
    network.add_node(node_b)
    network.add_node(node_c)
    
    node_a.add_neighbor(node_b)
    
    message = Message(source_id=node_a.id, destination_id=node_c.id, payload="This should fail")
    
    # The send operation should fail
    assert network.send_direct_message(message) is False

def test_node_receives_correct_message():
    """Tests that a node correctly processes a message intended for it."""
    node_a = Node("Receiver Node")
    message = Message(source_id="some_other_node", destination_id=node_a.id, payload="Test Payload")
    
    assert node_a.receive_message(message) is True

def test_node_rejects_incorrect_message():
    """Tests that a node rejects a message not intended for it."""
    node_a = Node("Receiver Node")
    message = Message(source_id="some_other_node", destination_id="a_different_id", payload="Wrong destination")

    assert node_a.receive_message(message) is False