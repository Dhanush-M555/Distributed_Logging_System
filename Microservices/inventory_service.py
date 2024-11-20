from node import Node

if __name__ == "__main__":
    inventory_node = Node(
        service_name="InventoryService",
        kafka_bootstrap_servers="192.168.222.127:9092"
    )
    inventory_node.start_heartbeat()
    inventory_node.start_log_generation()