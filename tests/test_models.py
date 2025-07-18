# tests/test_models.py

import yaml
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

def test_create_network_from_config():
    """Tests that a network can be created from a YAML configuration."""
    # Create a dummy YAML config as a string
    yaml_config_string = """
    nodes:
      - name: Node A
      - name: Node B
      - name: Node C
    links:
      - [Node A, Node B]
    """
    # Use yaml.safe_load to parse the string
    config = yaml.safe_load(yaml_config_string)

    # We need a temporary way to pass this data to the method.
    # Let's adapt the method slightly to handle data directly for testing.
    # (Or, for a real test, write to a temp file). For now, let's just test the logic.
    
    network = Network()
    name_to_node_map = {}

    # Test node creation
    for node_data in config.get('nodes', []):
        node = Node(name=node_data['name'])
        network.add_node(node)
        name_to_node_map[node.name] = node
    
    assert len(network.nodes) == 3

    # Test link creation
    for link_data in config.get('links', []):
        node1 = name_to_node_map.get(link_data[0])
        node2 = name_to_node_map.get(link_data[1])
        node1.add_neighbor(node2)

    node_a = name_to_node_map.get("Node A")
    node_b = name_to_node_map.get("Node B")
    node_c = name_to_node_map.get("Node C")

    assert node_b in node_a.neighbors
    assert node_a in node_b.neighbors
    assert len(node_c.neighbors) == 0

# --- NEW TEST for AEGIS-4 ---
def test_find_shortest_path_success():
    """Tests that the BFS algorithm finds the correct shortest path."""
    # Build a simple network for testing
    # A -> B -> C
    # A -> D
    network = Network()
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D")
    
    network.add_node(node_a)
    network.add_node(node_b)
    network.add_node(node_c)
    network.add_node(node_d)
    
    node_a.add_neighbor(node_b)
    node_b.add_neighbor(node_c)
    node_a.add_neighbor(node_d)
    
    # Path from A to C should be [A, B, C]
    path = network.find_shortest_path(node_a.id, node_c.id)
    
    assert path is not None
    assert len(path) == 3
    assert path[0].name == "A"
    assert path[1].name == "B"
    assert path[2].name == "C"

def test_find_shortest_path_no_path():
    """Tests that the algorithm returns None when no path exists."""
    # Build a disjointed network
    # A -> B   C -> D
    network = Network()
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    node_d = Node("D")

    network.add_node(node_a)
    network.add_node(node_b)
    network.add_node(node_c)
    network.add_node(node_d)

    node_a.add_neighbor(node_b)
    node_c.add_neighbor(node_d)

    # There should be no path from A to D
    path = network.find_shortest_path(node_a.id, node_d.id)
    
    assert path is None

# --- NEW TESTS for AEGIS-5 ---

def test_node_can_be_taken_offline_and_online():
    """Tests that a node's active status can be toggled."""
    node = Node("Test Node")
    assert node.is_active is True
    
    node.take_offline()
    assert node.is_active is False
    
    node.bring_online()
    assert node.is_active is True

def test_pathfinder_avoids_offline_nodes():
    """Tests that the pathfinder finds an alternate route around an offline node."""
    # Build a network with a redundant path
    # A -> B -> C
    # |---------|  (A is also connected to C)
    network = Network()
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")
    
    network.add_node(node_a)
    network.add_node(node_b)
    network.add_node(node_c)
    
    node_a.add_neighbor(node_b)
    node_b.add_neighbor(node_c)
    node_a.add_neighbor(node_c) # The alternate, shorter path
    
    # Take the direct path node (B) offline
    node_b.take_offline()
    
    # Path from A to C should now be [A, C], not [A, B, C]
    path = network.find_shortest_path(node_a.id, node_c.id)
    
    assert path is not None
    assert len(path) == 2
    assert path[0].name == "A"
    assert path[1].name == "C"

def test_pathfinder_fails_if_no_alternate_path():
    """Tests that the pathfinder returns None if an offline node breaks the only path."""
    # A -> B -> C
    network = Network()
    node_a = Node("A")
    node_b = Node("B")
    node_c = Node("C")

    network.add_node(node_a)
    network.add_node(node_b)
    network.add_node(node_c)

    node_a.add_neighbor(node_b)
    node_b.add_neighbor(node_c)

    # Take the critical node B offline
    node_b.take_offline()

    # There should be no path from A to C now
    path = network.find_shortest_path(node_a.id, node_c.id)
    
    assert path is None