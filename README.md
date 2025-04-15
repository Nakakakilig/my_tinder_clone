# My Tinder Clone

A pet project simulating core Tinder functionality – profile browsing, swiping, and matching – built with Python and FastAPI.
The main goal is to practice Python (FastAPI, SQLAlchemy), Docker, microservices architecture, Clean Architecture concepts, and deployment. A React SPA frontend is planned.

## Technologies & Stack
### Back-end:

- Python 3.12
- FastAPI
- SQLAlchemy
- Redis
- PostgreSQL
- Kafka (asynchronous messaging)
- Docker
- CI/CD

### Front-end:
- React SPA (planned)

## Architecture:

- Follows **Clean Architecture** principles with *Domain* / *Application* / *Infrastructure* / *Presentation* layers.

- Organized as modular microservices – each encapsulates a specific domain responsibility and communicates via Kafka events.

- Each microservice follows a Clean Architecture layout and leverages FastAPI + async SQLAlchemy.

## Overview
This repository is split into multiple microservices:

| Service             | Description                        | Status       |
|---------------------|------------------------------------|--------------|
| profile-service     | Manages profiles and preferences   | ✅ Done       |
| deck-service        | Generates daily user decks         | ✅ Done       |
| swipe-service       | Handles swipe actions              | ✅ Done       |
| auth-service        | Auth (JWT, registration)           | 🟡 Planned    |
| notification-service| Sends Kafka-based notifications    | 🟡 Planned    |
| client              | React frontend                     | 🟡 Planned    |

## Folder Structure in Each Microservice

-  **_domain/_**: Domain models, business logic, and abstract interfaces (repositories, etc.)
-  **_use_cases/_**: Use cases/services that orchestrate domain logic
-  **_infrastructure/_**: Implementations of repositories, database adapters, Kafka integration, etc.
-  **_presentation/_**: HTTP routes (endpoints), Pydantic request/response schemas

Additionally:

**_client/_**: A placeholder folder for the future React frontend

**_kafka/_**: Docker configuration for Kafka

**_scripts/_**: Helper shell scripts (to be replaced with **Makefiles** later)



> ### Note: All microservices are in a single repository to simplify interaction during development. In a production environment, splitting them into separate repositories is generally recommended.

## 🧩 System Architecture (Mermaid Diagram)
![alt text](mermaid-diagram-2025-04-15-171534.svg)



## Development Plan

 - [x] Improve **error handling**

 - [x] **Logging** (with trace id)

 - [ ] **Testing**

 - [ ] **Create user → profile → preferences in one step**

 - [ ] **Replace .sh scripts with Makefiles**

 - [ ] **Frontend** (React SPA)

 - [ ] **Authorization** (login, registration, JWT)

 - [ ] **Deployment**

    - [ ] Set up CI/CD pipeline (GitHub Actions)

    - [ ] Configure API Gateway (Traefik) for routing and rate limiting

 - [ ] **Notification-service** for mutual likes (via Kafka)

 - [ ] **PUT/DELETE endpoints** in profile-service & update deck-service via Kafka

 - [ ] **Use UUID** instead of numeric IDs

 - [ ] **Daily deck generation by cron** (if last generation was X hours ago)
