# src/reporter.py

import csv
import datetime

class Reporter:
    """Logs simulation events and generates a CSV report."""

    def __init__(self):
        """Initializes the reporter with an empty log."""
        self.log_entries = []
        print("Reporter initialized.")

    def log_routing_attempt(self, message, source_node, dest_node, path, latency, success):
        """Logs the result of a single message routing attempt."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = {
            "timestamp": timestamp,
            "message_id": message.id,
            "source_node": source_node.name,
            "intended_destination": dest_node.name,
            "payload": message.payload,
            "status": "SUCCESS" if success else "FAILED",
            "path_taken": ' -> '.join([n.name for n in path]) if path else "No path found",
            "total_latency_ms": latency if success else "N/A"
        }
        self.log_entries.append(entry)

    def write_report(self, filename="simulation_report.csv"):
        """Writes all logged entries to a specified CSV file."""
        if not self.log_entries:
            print("No events to report.")
            return False
            
        # Use the keys from the first entry as headers
        headers = self.log_entries[0].keys()
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(self.log_entries)
            print(f"Successfully wrote report to {filename}")
            return True
        except IOError as e:
            print(f"Error writing report to file: {e}")
            return False
