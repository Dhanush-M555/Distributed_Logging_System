from node import Node

if __name__ == "__main__":
    payment_node = Node(
        service_name="PaymentService",
        kafka_bootstrap_servers="192.168.194.95:9092"
    )
    payment_node.start_heartbeat()
    payment_node.start_log_generation()