# src/visualizer.py

import networkx as nx
import matplotlib.pyplot as plt

class Visualizer:
    """Handles the creation of network graph visualizations."""

    def generate_graph_image(self, network, filename="network_topology.png"):
        """
        Creates a visual graph of the network and saves it as a PNG image.
        
        - Nodes are colored based on their active status (Green for ONLINE, Red for OFFLINE).
        - Node labels are displayed above the nodes for clarity.
        - Edges (links) are labeled with their latency.
        """
        if not network.nodes:
            print("Cannot generate graph: Network has no nodes.")
            return

        # Create a new graph object
        G = nx.Graph()
        
        node_colors = []
        node_labels = {}

        # Add nodes to the graph and set their properties
        for node in network.nodes.values():
            G.add_node(node.id)
            node_labels[node.id] = node.name
            node_colors.append('green' if node.is_active else 'red')

        # Add edges (links) to the graph
        edge_labels = {}
        for node in network.nodes.values():
            for neighbor, latency in node.neighbors.items():
                if not G.has_edge(node.id, neighbor.id):
                    G.add_edge(node.id, neighbor.id)
                    edge_labels[(node.id, neighbor.id)] = f"{latency}ms"

        # Determine the layout of the graph for a nice visual spread
        pos = nx.spring_layout(G, k=2.0, iterations=50)

        # Create the plot
        plt.figure(figsize=(16, 12))
        
        # Draw the nodes and edges
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500)
        nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7, edge_color='gray')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=9)

        # --- MODIFIED SECTION ---
        # Draw node labels separately with a vertical offset to place them above the nodes
        label_pos = {k: (v[0], v[1] + 0.08) for k, v in pos.items()}
        nx.draw_networkx_labels(G, label_pos, labels=node_labels, font_size=12, font_color='black')
        # --- END MODIFIED SECTION ---

        # Customize and save the plot
        plt.title("Project Aegis - Network Topology", size=20)
        plt.margins(0.1)
        plt.axis('off')
        
        try:
            plt.savefig(filename, format="PNG", bbox_inches="tight")
            print(f"Successfully saved network graph to '{filename}'")
        except IOError as e:
            print(f"Error saving graph image: {e}")
        finally:
            plt.clf()
            plt.close()
