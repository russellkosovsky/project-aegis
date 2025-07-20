# tests/test_main.py

import pytest
from unittest.mock import patch
from io import StringIO

from main import main
from src.models import Network, Node

# --- MODIFIED: Added 'n' to the side_effect list to answer the "save report?" prompt ---
@patch('builtins.input', side_effect=['status', 'exit', 'n'])
@patch('sys.stdout', new_callable=StringIO)
def test_cli_status_command(mock_stdout, mock_input):
    """
    Tests the 'status' command of the CLI.
    """
    with patch('main.Network.create_from_config') as mock_create:
        test_network = Network()
        node_a = Node("Node-A")
        node_b = Node("Node-B")
        node_b.take_offline()
        test_network.add_node(node_a)
        test_network.add_node(node_b)
        
        mock_create.return_value = test_network

        # Run main() in a try/except block to catch the StopIteration from the mock
        # This is expected when the input mock runs out of values.
        try:
            main()
        except StopIteration:
            pass

    output = mock_stdout.getvalue()

    assert "Node-A" in output
    assert "ONLINE" in output
    assert "Node-B" in output
    assert "OFFLINE" in output
    # The 'Aegis>' prompt is part of the mocked input function and won't appear in stdout.


# --- MODIFIED: Added 'n' to the side_effect list ---
@patch('builtins.input', side_effect=['path Node-A Node-C', 'exit', 'n'])
@patch('sys.stdout', new_callable=StringIO)
def test_cli_path_command(mock_stdout, mock_input):
    """Tests the 'path' command of the CLI."""
    with patch('main.Network.create_from_config') as mock_create:
        network = Network()
        node_a = Node("Node-A")
        node_b = Node("Node-B")
        node_c = Node("Node-C")
        network.add_node(node_a)
        network.add_node(node_b)
        network.add_node(node_c)
        node_a.add_neighbor(node_b, 10)
        node_b.add_neighbor(node_c, 10)
        mock_create.return_value = network

        try:
            main()
        except StopIteration:
            pass

    output = mock_stdout.getvalue()
    assert "Fastest Path: Node-A -> Node-B -> Node-C" in output
    assert "(Total Latency: 20ms)" in output
