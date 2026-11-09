# Message Queue + Visit Counter with Redis

## Project Description
This project is a Cloud Computing and DevOps midterm project that demonstrates communication between two Flask web applications using Redis and Docker Compose.

## Project Components

**App1 – Message Collector**
- Allows users to submit feedback messages.
- Stores messages in a Redis list.
- Increments the visit counter when the page is loaded.

**App2 – Dashboard**
- Displays the total number of submitted messages.
- Displays the total number of visits.
- Provides a button to refresh the statistics.

**Redis Database**
- Stores messages and visit counts.
- Shares data between both applications.
- Uses a Docker volume and append-only persistence to preserve data.

## Technologies Used
- Python
- Flask
- Redis
- Docker
- Docker Compose
- Git and GitHub

## How to Run

Make sure Docker Desktop is running.

Run the following command in the project directory:

```bash
docker compose up -d --build
```

## Application URLs

- Message Collector: http://localhost:5001
- Dashboard: http://localhost:5002

## Check Running Containers

```bash
docker compose ps
```

## Stop the Project

```bash
docker compose down
```

The Redis volume preserves the stored data when the containers are stopped and recreated without removing the volume.