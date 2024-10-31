# Distributed Logging System

## Project Overview

Effective log management is crucial for operational excellence in a microservices architecture. This project aims to streamline the collection, storage, and analysis of logs generated by various services, enhancing the ability to quickly track application behavior and identify errors. By capturing relevant metadata alongside each log entry and enabling real-time ingestion and querying, the system improves operational visibility and facilitates proactive responses to potential issues. Ultimately, this distributed logging framework enhances resilience and maintainability in a dynamic application landscape.


## System Architecture & Flow
![image](https://github.com/user-attachments/assets/60db1e53-cc5f-47db-b429-680677d1f3d8)


### Components

1. **Microservices(Process):** Represent distributed nodes that independently generate logs and send heartbeat signals to monitor their status.
2. **Log Accumulator:** Collects log data from each node, structures it, and forwards it to the Pub-Sub model for centralized log management.
3. **Pub-Sub Model:**  Acts as a communication layer, facilitating reliable, asynchronous distribution of logs.
4. **Log Storage:** A system for indexing and storing logs in a searchable format for easy access and monitoring.
5. **Alerting System:** Listens for specific log levels (e.g., ERROR, FATAL, etc) in real-time, generating alerts to ensure prompt responses to critical events.
6. **Heartbeat Mechanism:** Provides failure detection by alerting when a node stops sending heartbeats, signaling that the node may have failed.

---

## Weekly Commit Milestones

### Week 1: Microservice and Log Generation Setup

**Completed Tasks:**  
*(Tick the boxes below to indicate completion.)*

- [x] Created 3 independent microservices:
  - PaymentService
  - OrderService
  - InventoryService
- [x] Implemented log generation for each microservice.
- [x] Added a heartbeat mechanism for periodic status updates.
- [x] Implemented log message color coding for clarity.

**Next Steps:**
- [ ] Create a trigger for missing heartbeats once the Pub-Sub model is implemented.

---

### Week 2: Log Accumulator and Pub-Sub Model Integration

**Tasks:**

- [ ] Configure the log accumulator to collect and structure logs.
- [ ] Set up the Pub-Sub model (Apache Kafka) for log management.
- [ ] Configure the subscriber to ensure seamless log consumption.

---

### Week 3: Alerting, Log Storage, and Final Integration

**Tasks:**

- [ ] Implement the alerting system for critical logs (ERROR, WARN).
- [ ] Configure log storage using Elasticsearch.
- [ ] Conduct final testing and validation of the complete pipeline.

---

## Tools & Technologies

- **Programming Language:** Python
- **Log Accumulator:** Fluentd or Apache Flume
- **Pub-Sub Model:** Apache Kafka
- **Log Storage:** Elasticsearch
- **Visualization (Optional):** Kibana

---

## Log Levels

- **INFO:** General system operations information.
- **WARN:** Indications of potential issues.
- **ERROR:** Errors that allow continued operation.
- **FATAL:** Critical issues requiring immediate attention.

---

## Metadata for Logs

**Example Structures:**

- **Microservice Registration Message:**
```json
{
    "node_id": "<unique node-id>",
    "message_type": "REGISTRATION",
    "service_name": "PaymentService",
    "timestamp": "<timestamp>"
}
```

- **INFO Log:**
```json
{
    "log_id": "<unique log-id>",
    "node_id": "<node-id>",
    "log_level": "INFO",
    "message_type": "LOG",
    "message": "<Log Message>",
    "service_name": "<ServiceName>",
    "timestamp": "<timestamp>"
}
```

- **WARN Log:**
```json
{
    "log_id": "<unique log-id>",
    "node_id": "<node-id>",
    "log_level": "WARN",
    "message_type": "LOG",
    "message": "",
    "service_name": "<ServiceName>",
    "response_time_ms": "",
    "threshold_limit_ms": "",
    "timestamp": "<timestamp>"
}
```

- **ERROR Log:**
```json
{
    "log_id": "<unique log-id>",
    "node_id": "<node-id>",
    "log_level": "ERROR",
    "message_type": "LOG",
    "message": "",
    "service_name": "<ServiceName>",
    "error_details": {
        "error_code": "",
        "error_message": ""
    },
    "timestamp": "<timestamp>"
}
```

- **Heartbeat Message:**
```json
{
    "node_id": "<node-id>",
    "message_type": "HEARTBEAT",
    "status": "UP/DOWN",
    "timestamp": "<timestamp>"
}
```

- **Microservice Registry:**
```json
{
    "message_type":"REGISTRATION",
    "node_id": "<node-id>",
    "service_name": "<ServiceName>",
    "status": "UP/DOWN",
    "timestamp": "<timestamp>"
}
```


## References

- [Distributed Logging System Design on Medium](<https://medium.com/@krrishan7495/distributed-logging-designing-a-robust-system-for-enhanced-monitoring-64ddb0838882>)
- [Distributed Logging Architecture on DZone](<https://dzone.com/articles/distributed-logging-architecture-for-microservices>)
- [Remote Kafka Connection Guide by Bitnami](<https://docs.bitnami.com/google-templates/infrastructure/kafka/administration/connect-remotely/>)
- [Fluentd Output to Kafka Documentation](<https://docs.fluentd.org/0.12/output/kafka>)
- [Python Client for Elasticsearch - Getting Started Guide](<https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/getting-started-python.html>)


