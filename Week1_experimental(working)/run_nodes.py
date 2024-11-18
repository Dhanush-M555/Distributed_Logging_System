# run_nodes.py
from node import Node

if __name__ == "__main__":
    services = ["PaymentService", "OrderService", "InventoryService"]
    nodes = [Node(service) for service in services]
    
    # Start log generation and heartbeat for each node
    for node in nodes:
        node.start_heartbeat()
        node.start_log_generation()
