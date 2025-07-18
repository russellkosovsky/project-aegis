# main.py

import logging
from src.models import Network, Message

# --- Helper Functions for the CLI ---

def print_help():
    """Prints the list of available commands."""
    print("\n--- Project Aegis CLI Help ---")
    print("  status                            - Shows the status of all nodes in the network.")
    print("  path <from_node> <to_node>        - Finds and displays the fastest path between two nodes.")
    print("  route <from> <to> <payload>     - Routes a message from a source to a destination node.")
    print("  offline <node_name>               - Takes a specified node offline.")
    print("  online <node_name>                - Brings a specified node back online.")
    print("  help                              - Displays this help message.")
    print("  exit / quit                       - Exits the simulator.")
    print("--------------------------------\n")

def print_status(network):
    """Prints the status of every node in the network with color coding."""
    print("\n--- Network Status ---")
    if not network.nodes:
        print("Network is empty.")
        return
    
    # Sort nodes alphabetically for consistent output
    for node in sorted(network.nodes.values(), key=lambda n: n.name):
        # Use ANSI escape codes for color: Green for ONLINE, Red for OFFLINE
        if node.is_active:
            status_colored = "\033[92mONLINE\033[0m" # Green
        else:
            status_colored = "\033[91mOFFLINE\033[0m" # Red
            
        print(f"Node: {node.name:<20} | Status: {status_colored}")
        
        neighbor_strings = []
        # Sort neighbors by name for consistent output
        for neighbor, latency in sorted(node.neighbors.items(), key=lambda item: item[0].name):
            neighbor_status = "ONLINE" if neighbor.is_active else "OFFLINE"
            neighbor_strings.append(f"{neighbor.name} ({latency}ms, {neighbor_status})")
        
        if neighbor_strings:
            print(f"  - Neighbors: {', '.join(neighbor_strings)}")
        else:
            print("  - Neighbors: None")
    print("----------------------\n")


# --- Main Application Logic ---

def main():
    """
    The main entry point for the interactive simulator.
    """
    # Set logging to WARNING to keep the CLI clean. The backend still logs everything,
    # but only warnings and errors will appear on the console by default.
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("--- Starting Project Aegis Network Simulator ---")
    network = Network.create_from_config('network_config.yml')
    print("--- Network Initialization Complete ---")
    print_help()

    # --- Interactive Command Loop ---
    while True:
        try:
            # Get user input and split it into command and arguments
            raw_input = input("Aegis> ").strip()
            if not raw_input:
                continue
            
            parts = raw_input.split()
            command = parts[0].lower()
            args = parts[1:]

            if command in ["exit", "quit"]:
                print("Shutting down simulator. Goodbye.")
                break
            
            elif command == "help":
                print_help()
            
            elif command == "status":
                print_status(network)

            elif command == "offline":
                if len(args) != 1:
                    print("Usage: offline <node_name>")
                    continue
                node = network.get_node_by_name(args[0])
                if node:
                    node.take_offline()
                    print(f"Confirmation: Node '{node.name}' is now offline.")
                else:
                    print(f"Error: Node '{args[0]}' not found.")

            elif command == "online":
                if len(args) != 1:
                    print("Usage: online <node_name>")
                    continue
                node = network.get_node_by_name(args[0])
                if node:
                    node.bring_online()
                    print(f"Confirmation: Node '{node.name}' is now online.")
                else:
                    print(f"Error: Node '{args[0]}' not found.")
            
            elif command == "path":
                if len(args) != 2:
                    print("Usage: path <from_node> <to_node>")
                    continue
                from_node = network.get_node_by_name(args[0])
                to_node = network.get_node_by_name(args[1])
                if not from_node or not to_node:
                    print("Error: One or both nodes not found.")
                    continue
                
                path, latency = network.find_shortest_path(from_node.id, to_node.id)
                if path:
                    path_names = ' -> '.join([n.name for n in path])
                    print(f"Fastest Path: {path_names} (Total Latency: {latency}ms)")
                else:
                    print(f"No path found between '{from_node.name}' and '{to_node.name}'.")

            elif command == "route":
                if len(args) < 3:
                    print("Usage: route <from_node> <to_node> <payload>")
                    continue
                from_node = network.get_node_by_name(args[0])
                to_node = network.get_node_by_name(args[1])
                payload = " ".join(args[2:])
                
                if not from_node or not to_node:
                    print("Error: One or both nodes not found.")
                    continue
                
                message = Message(from_node.id, to_node.id, payload)
                # Set logging to INFO just for this operation to see the detailed path
                logging.getLogger().setLevel(logging.INFO)
                if not network.route_message(message):
                    print("Message routing failed. See logs for details.")
                else:
                    print("Message routed successfully.")
                # Set logging back to WARNING
                logging.getLogger().setLevel(logging.WARNING)

            else:
                print(f"Unknown command: '{command}'. Type 'help' for a list of commands.")

        except KeyboardInterrupt:
            # Allow Ctrl+C to exit gracefully
            print("\nShutting down simulator. Goodbye.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
