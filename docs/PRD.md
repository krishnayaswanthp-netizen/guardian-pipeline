# Product Requirements Document (PRD): Event-Driven Job Processing Pipeline

## 1. Executive Summary
The Event-Driven Job Processing Pipeline is a robust, queue-backed system designed to provide guaranteed delivery for asynchronous tasks (e.g., AI inference, batch compute). The system addresses the critical need for a backend primitive that ensures every job reaches a terminal state exactly once in effect, even in the face of worker failures, broker instability, or downstream service outages. By utilizing the Transactional Outbox pattern and lease-based recovery, the system eliminates job loss and minimizes duplicate side effects.

## 2. Problem Statement
Current ad-hoc job processing methods (cron jobs, unmanaged threads) lack formal guarantees, leading to:
*   **Job Loss:** Workers killed mid-execution (OOM, spot instance reclamation) leave jobs in an ambiguous state.
*   **Unbounded Retries:** Transient downstream failures cause "retry storms" or silent drops.
*   **Poison Messages:** Malformed jobs block queue progress and consume worker capacity.
*   **Lack of Visibility:** Difficulty in tracing a job's lifecycle or diagnosing failures in real-time.

## 3. Goals & Objectives
*   **Zero Job Loss:** 100% of accepted jobs must reach a terminal state (Success or DLQ).
*   **Effectively-Once Processing:** Prevent duplicate terminal side effects through idempotency.
*   **Bounded Retries:** Implement predictable exponential backoff with a maximum attempt cap.
*   **Horizontal Scalability:** Support millions of jobs per day via stateless worker scaling.
*   **Operational Excellence:** Provide full lifecycle observability and manual recovery tools (DLQ Replay).

## 4. Target Users / Stakeholders
*   **API Clients / Producers:** Systems submitting jobs requiring durable acknowledgment.
*   **Operations/SRE Team:** Responsible for monitoring system health and triaging the DLQ.
*   **Downstream Services:** External APIs or inference engines consumed by the pipeline.

## 5. Functional Requirements

### 5.1 Client & Ingest
*   **Durable Acceptance:** The system must persist the job to the Primary Datastore before acknowledging receipt to the producer.
*   **Idempotent Ingestion:** Duplicate submissions with the same idempotency key must not create new job records.
*   **API Gateway:** Must handle authentication, rate limiting, and request routing.

### 5.2 Queue & Compute
*   **Transactional Outbox:** The Outbox Relay must poll the database and publish to Kafka to ensure atomicity between DB state and queue transport.
*   **Stateless Processing:** Workers must be stateless, pulling tasks from Kafka and updating job status in the Primary Datastore.
*   **Lease Management:** The Lease/Reaper service must detect "zombie" jobs (stuck in-progress) and re-queue them for processing.
*   **Large Payload Handling:** Workers must use Blob Storage for heavy data requirements rather than passing large payloads through the message broker.

### 5.3 Retry & DLQ
*   **Exponential Backoff:** The Retry Scheduler must manage failed tasks with increasing delays.
*   **Isolation (DLQ):** Jobs exceeding the retry limit must be moved to a Dead Letter Queue to prevent blocking the primary pipeline.
*   **Manual Replay:** An Operations tool must allow engineers to inspect DLQ messages and re-inject them into the primary queue after remediation.

### 5.4 Observability & Ops
*   **Lifecycle Tracing:** Every job state transition must be logged and traceable by Job ID.
*   **Health Monitoring:** Real-time dashboards must display throughput, error rates, and DLQ depth.
*   **Alerting:** Automated notifications for systemic failures (e.g., DLQ spikes, high worker failure rates).

## 6. Non-Functional Requirements
*   **Availability:** 99.9% uptime for the ingestion path.
*   **Reliability:** 0% job loss under induced worker failure.
*   **Scalability:** Linear scaling of workers to handle millions of jobs/day.
*   **Performance:** 95% of jobs should begin execution within 30 seconds of acceptance.
*   **Durability:** Job records and audit logs must be retained for 30 days.
*   **Security:** Tenant-level isolation for job data and access.

## 7. System Architecture Overview
The system is divided into four functional zones:
1.  **Client & Ingest Zone:** Entry point; ensures the "Database as Source of Truth" principle.
2.  **Queue & Compute Zone:** Decouples ingestion from execution using Kafka and the Transactional Outbox pattern. Includes a Lease/Reaper for crash recovery.
3.  **Retry & DLQ Zone:** Manages failure states, retries, and manual intervention.
4.  **Observability & Ops Zone:** Provides the "Observability-first" layer for monitoring and alerting.

## 8. Tech Stack
*   **Languages:** Go, Python, Node.js.
*   **API Gateway:** NGINX, Kong, or AWS API Gateway.
*   **Primary Datastore:** PostgreSQL or MySQL.
*   **Message Broker:** Apache Kafka or Redpanda.
*   **Outbox Relay:** Debezium or Custom Go Relay.
*   **Worker Framework:** Celery (Python) or native Go workers.
*   **Blob Storage:** AWS S3, MinIO, or Azure Blob Storage.
*   **Observability:** Prometheus, Grafana, ELK Stack, Jaeger.
*   **Alerting:** Alertmanager, PagerDuty.

## 9. Data Requirements
*   **Job State Schema:** Must include `job_id`, `status` (Submitted, In-Progress, Completed, Failed), `payload_ref`, `retry_count`, `last_heartbeat`, and `idempotency_key`.
*   **Outbox Table:** A dedicated table in the Primary Datastore to capture events for the Relay service.
*   **Retention:** Database records should be archived after 30 days to maintain performance.

## 10. API Specifications
*   **POST /v1/jobs:** Submit a new job. Requires an idempotency key.
*   **GET /v1/jobs/{id}:** Retrieve current status and attempt history.
*   **POST /v1/ops/dlq/replay:** (Internal) Re-inject specific job IDs from DLQ to the primary queue.

## 11. Security Requirements
*   **Authentication:** All ingest requests must be authenticated via API Keys or OAuth2.
*   **Authorization:** Role-Based Access Control (RBAC) for the Operations Dashboard and Replay Tool.
*   **Encryption:** Data must be encrypted at rest (DB/Blob) and in transit (TLS).

## 12. Deployment & Infrastructure
*   **Containerization:** All services (Ingest, Workers, Relay) must be containerized (Docker).
*   **Orchestration:** Deployment via Kubernetes to manage horizontal scaling and self-healing.
*   **CI/CD:** Automated pipelines for testing idempotency and failure recovery scenarios.

## 13. Success Metrics
*   **Job Completion Rate:** % of jobs reaching 'Completed' vs 'Failed'.
*   **Duplicate Rate:** % of jobs with multiple terminal side effects (Target: 0%).
*   **Recovery Time:** Average time for the Reaper service to reclaim a job after worker failure.
*   **MTTD:** Mean Time to Detect systemic failures via alerting.

## 14. Timeline & Milestones
*   **Phase 1 (Foundation):** API Ingest, Primary DB, and Outbox Relay setup.
*   **Phase 2 (Compute):** Kafka integration and stateless Worker Pool implementation.
*   **Phase 3 (Reliability):** Lease/Reaper service and Retry Scheduler.
*   **Phase 4 (Ops):** DLQ Replay tool and full Observability Stack integration.

## 15. Open Questions & Risks
*   **Risk:** Idempotency relies on correct developer implementation within the worker handlers.
*   **Risk:** Correlated downstream failures could lead to DLQ saturation.
*   **Open Question:** What is the maximum payload size before forcing a move to Blob Storage?
*   **Open Question:** Are there specific regional compliance requirements for data residency in Blob Storage?