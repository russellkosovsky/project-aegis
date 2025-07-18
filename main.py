# main.py

import logging
from src.models import Network

# Set up basic logging to see the output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    The main entry point for the simulation.
    """
    logging.info("--- Starting Project Aegis Network Simulator ---")
    
    # Create a network from our configuration file
    network = Network.create_from_config('network_config.yml')
    
    logging.info("--- Network Initialization Complete ---")
    logging.info(f"Total nodes in network: {len(network.nodes)}")
    
    # Print a summary of the network topology
    for node_id, node in network.nodes.items():
        neighbor_names = [n.name for n in node.neighbors]
        print(f"\nNode: {node.name} ({node.id})")
        print(f"  - Neighbors: {', '.join(neighbor_names) if neighbor_names else 'None'}")

if __name__ == "__main__":
    main()