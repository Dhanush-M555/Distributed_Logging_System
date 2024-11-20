from node import Node

if __name__ == "__main__":
    order_node = Node(
        service_name="OrderService",
        kafka_bootstrap_servers="192.168.194.95:9092"
    )
    order_node.start_heartbeat()
    order_node.start_log_generation()