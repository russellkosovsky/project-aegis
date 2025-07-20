# main.py

import logging
import argparse # <-- New import for command-line arguments
from src.models import Network, Message
from src.reporter import Reporter

# --- Helper Functions (print_help, print_status) ---
# These are unchanged.

def print_help():
    """Prints the list of available commands for interactive mode."""
    print("\n--- Project Aegis CLI Help ---")
    print("  status                            - Shows the status of all nodes in the network.")
    print("  path <from_node> <to_node>        - Finds and displays the fastest path between two nodes.")
    print("  route <from> <to> <payload>     - Routes a message from a source to a destination node.")
    print("  offline <node_name>               - Takes a specified node offline.")
    print("  online <node_name>                - Brings a specified node back online.")
    print("  report [filename.csv]             - Saves the session log to a CSV file.")
    print("  help                              - Displays this help message.")
    print("  exit / quit                       - Exits the simulator.")
    print("--------------------------------\n")

def print_status(network):
    """Prints the status of every node in the network with color coding."""
    print("\n--- Network Status ---")
    if not network.nodes:
        print("Network is empty.")
        return
    for node in sorted(network.nodes.values(), key=lambda n: n.name):
        status_colored = "\033[92mONLINE\033[0m" if node.is_active else "\033[91mOFFLINE\033[0m"
        print(f"Node: {node.name:<25} | Status: {status_colored}")
        neighbor_strings = []
        for neighbor, latency in sorted(node.neighbors.items(), key=lambda item: item[0].name):
            neighbor_status = "ONLINE" if neighbor.is_active else "OFFLINE"
            neighbor_strings.append(f"{neighbor.name} ({latency}ms, {neighbor_status})")
        print(f"  - Neighbors: {', '.join(neighbor_strings) if neighbor_strings else 'None'}")
    print("----------------------\n")

# --- New Function for Automated Test ---

def run_automated_test(network, reporter):
    """Runs a predefined sequence of events to showcase the simulator's features."""
    print("--- Running Automated Test Scenario ---")
    
    # Get nodes for the scenario, using underscore names to match common configs.
    command_center = network.get_node_by_name("Command_Center")
    backup_center = network.get_node_by_name("Backup_Center")
    satellite = network.get_node_by_name("Satellite_Relay")
    mobile_unit = network.get_node_by_name("Mobile_Unit_7")

    if not all([command_center, backup_center, satellite, mobile_unit]):
        print("\nError: Could not find all required nodes for the automated test. Exiting.")
        print("Please ensure your network_config.yml contains: Command_Center, Backup_Center, Satellite_Relay, and Mobile_Unit_7")
        return

    # 1. Initial State
    print("\n[STEP 1] Initial network status.")
    print_status(network)

    # 2. Successful Route
    print("\n[STEP 2] Routing message from Command_Center to Backup_Center. Should take the fastest path.")
    msg1 = Message(command_center.id, backup_center.id, "Status report: All systems nominal.")
    network.route_message(msg1)

    # 3. Simulate Failure
    print("\n[STEP 3] Simulating critical node failure. Taking Ground_Station_Alpha offline.")
    ground_station = network.get_node_by_name("Ground_Station_Alpha")
    if ground_station:
        ground_station.take_offline()
    print_status(network)

    # 4. Demonstrate Resilience
    print("\n[STEP 4] Re-routing same message. Should find a new, higher-latency path via Satellite_Relay.")
    msg2 = Message(command_center.id, backup_center.id, "Status report: Rerouting due to node failure.")
    network.route_message(msg2)

    # 5. Demonstrate a Failed Route
    print("\n[STEP 5] Attempting to route a message from Mobile_Unit_7, which is now isolated.")
    msg3 = Message(mobile_unit.id, backup_center.id, "This message should fail.")
    if not network.route_message(msg3):
        print("Routing correctly failed as expected.")

    # 6. Restore Node
    print("\n[STEP 6] Restoring failed node. Bringing Ground_Station_Alpha back online.")
    if ground_station:
        ground_station.bring_online()
    print_status(network)

    # 7. Final Report
    print("\n[STEP 7] Generating final simulation report.")
    reporter.write_report("automated_test_report.csv")

    print("\n--- Automated Test Scenario Complete ---")

# --- Main Application Logic (Modified) ---

def main():
    """
    The main entry point for the simulator. Handles mode selection.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Project Aegis Network Simulator")
    parser.add_argument(
        '--mode', 
        type=str, 
        choices=['interactive', 'auto'], 
        default='interactive',
        help="Run in 'interactive' CLI mode or run the 'auto'mated test scenario."
    )
    args = parser.parse_args()

    # Set logging level
    log_level = logging.INFO if args.mode == 'auto' else logging.WARNING
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("--- Starting Project Aegis Network Simulator ---")
    reporter = Reporter()
    network = Network.create_from_config('network_config.yml', reporter=reporter)
    print("--- Network Initialization Complete ---\n")

    # --- Mode Selection ---
    if args.mode == 'auto':
        run_automated_test(network, reporter)
    else:
        # Run the interactive CLI loop
        print_help()
        while True:
            try:
                raw_input = input("Aegis> ").strip()
                if not raw_input:
                    continue
                
                parts = raw_input.split()
                command = parts[0].lower()
                cli_args = parts[1:]

                if command in ["exit", "quit"]:
                    save_choice = input("Save simulation report before exiting? (y/n): ").lower().strip()
                    if save_choice == 'y':
                        reporter.write_report()
                    print("Shutting down simulator. Goodbye.")
                    break
                
                # ... (The rest of the CLI command handling is unchanged) ...
                elif command == "help":
                    print_help()
                elif command == "status":
                    print_status(network)
                elif command in ["offline", "online"]:
                    if len(cli_args) != 1: print(f"Usage: {command} <node_name>"); continue
                    node = network.get_node_by_name(cli_args[0])
                    if node:
                        if command == "offline": node.take_offline()
                        else: node.bring_online()
                        print(f"Confirmation: Node '{node.name}' is now {command}.")
                    else: print(f"Error: Node '{cli_args[0]}' not found.")
                elif command == "path":
                    if len(cli_args) != 2: print("Usage: path <from_node> <to_node>"); continue
                    from_node, to_node = network.get_node_by_name(cli_args[0]), network.get_node_by_name(cli_args[1])
                    if not from_node or not to_node: print("Error: One or both nodes not found."); continue
                    path, latency = network.find_shortest_path(from_node.id, to_node.id)
                    if path: print(f"Fastest Path: {' -> '.join([n.name for n in path])} (Total Latency: {latency}ms)")
                    else: print(f"No path found between '{from_node.name}' and '{to_node.name}'.")
                elif command == "route":
                    if len(cli_args) < 3: print("Usage: route <from_node> <to_node> <payload>"); continue
                    from_node, to_node = network.get_node_by_name(cli_args[0]), network.get_node_by_name(cli_args[1])
                    payload = " ".join(cli_args[2:])
                    if not from_node or not to_node: print("Error: One or both nodes not found."); continue
                    message = Message(from_node.id, to_node.id, payload)
                    logging.getLogger().setLevel(logging.INFO)
                    if network.route_message(message): print("Message routed successfully.")
                    else: print("Message routing failed. See logs for details.")
                    logging.getLogger().setLevel(logging.WARNING)
                elif command == "report":
                    filename = cli_args[0] if cli_args else "simulation_report.csv"
                    reporter.write_report(filename)
                else:
                    print(f"Unknown command: '{command}'. Type 'help' for a list of commands.")

            except KeyboardInterrupt:
                print("\nShutting down simulator. Goodbye.")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
