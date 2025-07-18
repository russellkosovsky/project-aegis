# main.py

import logging
from src.models import Network, Message

def main():
    """
    The main entry point for the simulation.
    """
    logging.info("--- Starting Project Aegis Network Simulator ---")
    
    # 1. Create a network from our configuration file
    network = Network.create_from_config('network_config.yml')
    
    logging.info("--- Network Initialization Complete ---")
    
    # --- SIMULATION SCENARIO ---
    print("\n--- Running Simulation Scenario ---")

    # Get specific nodes to work with
    command_center = network.get_node_by_name("Command Center")
    mobile_unit = network.get_node_by_name("Mobile Unit 7")
    backup_center = network.get_node_by_name("Backup Center")
    satellite = network.get_node_by_name("Satellite Relay")

    if not all([command_center, mobile_unit, backup_center, satellite]):
        logging.error("Scenario failed: One or more required nodes not found in config.")
        return

    # Scenario 1: Send a message from Command Center to the Backup Center
    # The direct path is through the Satellite Relay
    print("\n[SCENARIO 1] Routing message with all nodes online...")
    msg1 = Message(command_center.id, backup_center.id, "Operational status: GREEN")
    network.route_message(msg1)

    # Scenario 2: A node failure forces a reroute
    print("\n[SCENARIO 2] Simulating node failure and rerouting...")
    
    # Take the satellite offline
    satellite.take_offline()
    
    # Try sending the message again. It should find a new path.
    # Command Center -> Ground Station Alpha -> Backup Center
    msg2 = Message(command_center.id, backup_center.id, "Operational status: DEGRADED, rerouting")
    network.route_message(msg2)

    # Bring the satellite back online
    satellite.bring_online()

if __name__ == "__main__":
    main()