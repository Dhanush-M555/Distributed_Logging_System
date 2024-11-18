from kafka_utils import KafkaWrapper
from datetime import datetime
from elasticsearch import Elasticsearch
from colorama import Fore, Style, init
import logging

# Initialize colorama and logging
init(autoreset=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogConsumer:
    def __init__(self, es_host='localhost', es_port=9200):
        self.kafka = KafkaWrapper()
        self.es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'http'}])  # Added scheme

        # Ensure the Elasticsearch index exists
        self.log_index = "microservice_logs"
        if not self.es.indices.exists(index=self.log_index):
            self.es.indices.create(index=self.log_index)
            logger.info(f"Created Elasticsearch index: {self.log_index}")

    def format_timestamp(self, timestamp_str):
        """Format ISO timestamp to a more readable format"""
        try:
            dt = datetime.fromisoformat(timestamp_str)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logger.warning(f"Invalid timestamp format: {timestamp_str} - {e}")
            return timestamp_str

    def store_log(self, message):
        """Store log message in Elasticsearch"""
        try:
            self.es.index(index=self.log_index, document=message)
            logger.info(f"Log stored in Elasticsearch: {message}")
        except Exception as e:
            logger.error(f"Failed to store log in Elasticsearch: {e}")

    def handle_alert(self, message, level_color):
        """Display alerts for WARN and ERROR logs"""
        print(f"{level_color}[ALERT] {message}{Style.RESET_ALL}")

    def handle_log(self, message):
        """Handle incoming log messages"""
        log_level = message.get('log_level', 'UNKNOWN')
        color = {
            'INFO': Fore.GREEN,
            'WARN': Fore.YELLOW,
            'ERROR': Fore.RED
        }.get(log_level, Fore.WHITE)
        
        timestamp = self.format_timestamp(message.get('timestamp', ''))
        service_name = message.get('service_name', 'Unknown')
        node_id = message.get('node_id', 'Unknown')[:8]
        msg = message.get('message', '')

        # Alert for WARN and ERROR logs
        if log_level in ('WARN', 'ERROR'):
            self.handle_alert(message, color)

        # Add extra details for WARN and ERROR logs
        extra_info = ""
        if log_level == 'WARN':
            response_time = message.get('response_time_ms', '')
            threshold = message.get('threshold_limit_ms', '')
            if response_time and threshold:
                extra_info = f" [Response: {response_time}ms, Threshold: {threshold}ms]"
        elif log_level == 'ERROR':
            error_details = message.get('error_details', {})
            if error_details:
                error_code = error_details.get('error_code', '')
                error_msg = error_details.get('error_message', '')
                extra_info = f" [Code: {error_code}, Details: {error_msg}]"

        # Print log to terminal
        print(f"{color}[{timestamp}] [{log_level}] {service_name} ({node_id}): {msg}{extra_info}{Style.RESET_ALL}")
        
        # Store log in Elasticsearch
        self.store_log(message)

    def start(self):
        """Start consuming messages from the Kafka topic"""
        self.kafka.start_consumer('microservice_logs', self.handle_log, 'log-consumer')
        logger.info("Started consuming messages from 'microservice_logs' topic")
        
        # Keep the main thread running
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("Shutting down consumers...")
            self.kafka.close()

if __name__ == "__main__":
    consumer = LogConsumer()
    consumer.start()

