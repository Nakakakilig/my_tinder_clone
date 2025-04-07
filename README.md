# My Tinder Clone

A pet project that implements simplified functionality similar to Tinder. The main goal is to practice Python (FastAPI, SQLAlchemy), Docker, microservices architecture, Clean Architecture concepts, and deployment. A React SPA frontend is planned.

## Technologies & Stack
### Back-end:

- Python 3.12
- FastAPI
- SQLAlchemy
- Redis
- PostgreSQL
- Kafka (asynchronous messaging)
- Docker

### Front-end:
- React SPA (planned)

## Architecture:

- Follows **Clean Architecture** principles with *Domain* / *Application* / *Infrastructure* / *Presentation* layers.

- Organized as microservices, where each core feature can be isolated into a separate service.

## Overview
This repository is split into multiple microservices:

- **profile-service**: Manages user profiles, preferences.

- **deck-service**: Creates candidate decks (match lists).

- **swipe-service**: Records swipes (like/dislike).

- **auth-service**: Authentication & authorization (JWT) (planned).

- **notification-service**: Listens for events (via Kafka) and triggers notifications (planned).

- **client**: React (planned).


## Folder Structure in Each Microservice

-  **_domain/_**: Domain models, business logic, and abstract interfaces (repositories, etc.)
-  **_application/_**: Use cases/services that orchestrate domain logic
-  **_infrastructure/_**: Implementations of repositories, database adapters, Kafka integration, etc.
-  **_presentation/_**: HTTP routes (endpoints), Pydantic request/response schemas

Additionally:

**_client/_**: A placeholder folder for the future React frontend

**_kafka/_**: Docker configuration for Kafka

**_scripts/_**: Helper shell scripts (to be replaced with **Makefiles** later)



> ### Note: All microservices are in a single repository to simplify interaction during development. In a production environment, splitting them into separate repositories is generally recommended.





## Development Plan

 - [ ] Improve **error handling**

 - [ ] **Logging** (with trace id)

 - [ ] **Testing**

 - [ ] **Create user → profile → preferences in one step**

 - [ ] **Replace .sh scripts with Makefiles**

 - [ ] **Frontend** (React SPA)

 - [ ] **Authorization** (login, registration, JWT)

 - [ ] **Deployment**

    - [ ] Correctly manage URLs in each microservice

    - [ ] Pass them via configuration (env vars, config files)

 - [ ] **Notification-service** for mutual likes (via Kafka)

 - [ ] **PUT/DELETE endpoints** in profile-service & update deck-service via Kafka

 - [ ] **Use UUID** instead of numeric IDs

 - [ ] **Daily deck generation by cron** (if last generation was X hours ago)
