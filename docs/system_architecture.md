# System Architecture

## Architecture Diagram
```
[Frontend (React/Node.js)] <--> [REST API & WebSockets (FastAPI)] <--> [Database (SQLite/PostgreSQL)]
                                          |
                                   [ML Prediction Pipeline]
```

## Data Flow
1. User updates status in Frontend.
2. Request hits FastAPI endpoint.
3. Database is updated.
4. WebSocket broadcasts update to all connected clients.
5. ML pipeline uses historical data for predictions.
