# main.py

import logging
import argparse
from src.models import Network, Message
from src.reporter import Reporter
from src.visualizer import Visualizer # <-- New import

# --- Helper Functions (print_help, print_status) ---
def print_help():
    """Prints the list of available commands for interactive mode."""
    print("\n--- Project Aegis CLI Help ---")
    print("  status                            - Shows the status of all nodes in the network.")
    print("  visualize [filename.png]          - Generates a PNG image of the network topology.")
    print("  path <from_node> <to_node>        - Finds and displays the fastest path between two nodes.")
    print("  route <from> <to> <payload>     - Routes a message from a source to a destination node.")
    print("  offline <node_name>               - Takes a specified node offline.")
    print("  online <node_name>                - Brings a specified node back online.")
    print("  report [filename.csv]             - Saves the session log to a CSV file.")
    print("  help                              - Displays this help message.")
    print("  exit / quit                       - Exits the simulator.")
    print("--------------------------------\n")

def print_status(network):
    # ... (This function is unchanged) ...
    print("\n--- Network Status ---")
    if not network.nodes: print("Network is empty."); return
    for node in sorted(network.nodes.values(), key=lambda n: n.name):
        status_colored = "\033[92mONLINE\033[0m" if node.is_active else "\033[91mOFFLINE\033[0m"
        print(f"Node: {node.name:<25} | Status: {status_colored}")
        neighbor_strings = []
        for neighbor, latency in sorted(node.neighbors.items(), key=lambda item: item[0].name):
            neighbor_status = "ONLINE" if neighbor.is_active else "OFFLINE"
            neighbor_strings.append(f"{neighbor.name} ({latency}ms, {neighbor_status})")
        print(f"  - Neighbors: {', '.join(neighbor_strings) if neighbor_strings else 'None'}")
    print("----------------------\n")

def run_automated_test(network, reporter, visualizer):
    # ... (This function is mostly unchanged, just add visualization steps) ...
    print("--- Running Automated Test Scenario ---")
    command_center = network.get_node_by_name("Command_Center")
    backup_center = network.get_node_by_name("Backup_Center")
    satellite = network.get_node_by_name("Satellite_Relay")
    if not all([command_center, backup_center, satellite]):
        print("\nError: Could not find all required nodes for the automated test. Exiting.")
        return
    
    print("\n[STEP 1] Generating initial topology map.")
    visualizer.generate_graph_image(network, "auto_test_step1_initial.png")
    
    print("\n[STEP 2] Simulating critical node failure.")
    satellite.take_offline()
    
    print("\n[STEP 3] Generating topology map with failed node.")
    visualizer.generate_graph_image(network, "auto_test_step3_failure.png")
    
    print("\n[STEP 4] Routing message to demonstrate resilience.")
    msg = Message(command_center.id, backup_center.id, "Rerouted message")
    network.route_message(msg)

    print("\n--- Automated Test Scenario Complete ---")


def main():
    """
    The main entry point for the simulator. Handles mode selection.
    """
    parser = argparse.ArgumentParser(description="Project Aegis Network Simulator")
    parser.add_argument('--mode', type=str, choices=['interactive', 'auto'], default='interactive', help="Run mode.")
    args = parser.parse_args()

    log_level = logging.INFO if args.mode == 'auto' else logging.WARNING
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("--- Starting Project Aegis Network Simulator ---")
    reporter = Reporter()
    visualizer = Visualizer() # <-- Create a Visualizer instance
    network = Network.create_from_config('network_config.yml', reporter=reporter)
    print("--- Network Initialization Complete ---\n")

    if args.mode == 'auto':
        run_automated_test(network, reporter, visualizer)
    else:
        print_help()
        while True:
            try:
                raw_input = input("Aegis> ").strip()
                if not raw_input: continue
                
                parts = raw_input.split()
                command = parts[0].lower()
                cli_args = parts[1:]

                if command in ["exit", "quit"]:
                    # ... (exit logic is unchanged) ...
                    save_choice = input("Save simulation report before exiting? (y/n): ").lower().strip()
                    if save_choice == 'y': reporter.write_report()
                    print("Shutting down simulator. Goodbye."); break
                
                elif command == "help": print_help()
                elif command == "status": print_status(network)
                
                # --- NEW COMMAND ---
                elif command == "visualize":
                    filename = cli_args[0] if cli_args else "network_topology.png"
                    visualizer.generate_graph_image(network, filename)

                # ... (rest of the CLI commands are unchanged) ...
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
                print("\nShutting down simulator. Goodbye."); break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
