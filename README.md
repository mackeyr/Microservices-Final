# Fun Fact Generator Microservice

## Overview

The **Fun Fact Generator** is a containerized microservice application built with **FastAPI**, **PostgreSQL**, **Docker**, and **Kafka**. It allows users to retrieve random fun facts, submit new facts securely using API keys, and track usage and events in a scalable, event-driven architecture.

The system is designed following modern microservices principles, including:

* RESTful APIs
* Database-backed persistence
* API key–based authentication
* Event-driven messaging using Kafka

---

## System Architecture

```
Client
  │
  ▼
FastAPI Service
  │  ├── PostgreSQL (facts, api keys, usage stats)
  │  └── Kafka (event publishing)
  ▼
Kafka Topics (facts.created, facts.viewed)
  ▼
Consumers (analytics, logging, future services)
```

* **FastAPI** handles HTTP requests
* **PostgreSQL** stores application data
* **Kafka** handles asynchronous events
* **Docker Compose** orchestrates all services

---

## Installation & Setup

### Prerequisites

* Docker Desktop (with Docker Compose)
* Git

### Clone the Repository

```bash
git clone <your-repo-url>
cd fun-fact-generator
```

### Build and Run the Application

```bash
docker compose up --build
```

This will start:

* FastAPI server at `http://localhost:8000`
* PostgreSQL database
* Kafka and Zookeeper

---

## API Usage

### Create an API Key

API keys are required to create new facts.

**Request**

```bash
curl -X POST "http://localhost:8000/auth/create_key?role=admin"
```

**Response**

```json
{
  "key": "f5ae954bbe52df764083f44e1698f5e9",
  "role": "admin"
}
```

Save this key for authenticated requests.

---

### Create a New Fun Fact

**Endpoint**

```
POST /facts/
```

**Headers**

```
Content-Type: application/json
x-api-key: YOUR_API_KEY
```

**Body**

```json
{
  "text": "Bananas are berries, but strawberries are not!",
  "source": "user"
}
```

**Example**

```bash
curl -X POST http://localhost:8000/facts/ \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d "{\"text\": \"Bananas are berries, but strawberries are not!\", \"source\": \"user\"}"
```

---

### Get a Random Fun Fact

**Endpoint**

```
GET /facts/random
```

**Example**

```bash
curl http://localhost:8000/facts/random
```

**Response**

```json
{
  "id": 5,
  "text": "Octopuses have three hearts.",
  "source": "user",
  "views": 12,
  "score": 0
}
```

Each request increments the view count and emits a Kafka event.

---

## Database Schema (Simplified)

### facts

* `id`
* `text`
* `source`
* `views`
* `score`
* `created_at`

### api_keys

* `key`
* `role`

### usage_stats

* `endpoint`
* `method`
* `status_code`
* `api_key`

---

## Kafka Integration

The API publishes events to Kafka:

| Event        | Topic           |
| ------------ | --------------- |
| Fact created | `facts.created` |
| Fact viewed  | `facts.viewed`  |

These events can be consumed by independent services for:

* Analytics
* Logging
* Monitoring
* Future features

---

## Development Notes

* The API waits for PostgreSQL to be ready before starting
* Kafka enables asynchronous, scalable processing
* The system is designed to be easily extensible

---

## Future Improvements

* Frontend UI
* Rate limiting
* Fact voting system
* Kafka consumer analytics dashboard
* Deployment to cloud infrastructure


