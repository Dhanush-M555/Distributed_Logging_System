# log_consumer.py
from kafka_utils import KafkaWrapper
import logging
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama and logging
init(autoreset=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogConsumer:
    def __init__(self):
        self.kafka = KafkaWrapper()
        
    def format_timestamp(self, timestamp_str):
        """Format ISO timestamp to a more readable format"""
        try:
            dt = datetime.fromisoformat(timestamp_str)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return timestamp_str

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
        node_id = message.get('node_id', 'Unknown')[:8]  # Show first 8 chars of node_id
        msg = message.get('message', '')
        
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

        print(f"{color}[{timestamp}] [{log_level}] {service_name} ({node_id}): {msg}{extra_info}{Style.RESET_ALL}")
        
    def handle_heartbeat(self, message):
        """Handle incoming heartbeat messages"""
        timestamp = self.format_timestamp(message.get('timestamp', ''))
        service_name = message.get('service_name', 'Unknown')
        node_id = message.get('node_id', 'Unknown')[:8]
        status = message.get('status', 'UNKNOWN')
        
        color = Fore.GREEN if status == 'UP' else Fore.RED
        print(f"{color}[{timestamp}] [HEARTBEAT] {service_name} ({node_id}): Status: {status}{Style.RESET_ALL}")
        
    def handle_registration(self, message):
        """Handle incoming registration messages"""
        timestamp = self.format_timestamp(message.get('timestamp', ''))
        service_name = message.get('service_name', 'Unknown')
        node_id = message.get('node_id', 'Unknown')[:8]
        
        print(f"{Fore.MAGENTA}[{timestamp}] [REGISTRATION] New service registered: {service_name} ({node_id}){Style.RESET_ALL}")
    
    def start(self):
        """Start consuming messages from all topics"""
        self.kafka.start_consumer('microservice_logs', self.handle_log, 'log-consumer')
        self.kafka.start_consumer('microservice_heartbeats', self.handle_heartbeat, 'heartbeat-consumer')
        self.kafka.start_consumer('microservice_registration', self.handle_registration, 'registration-consumer')
        
        logger.info("Started consuming messages from all topics")
        
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