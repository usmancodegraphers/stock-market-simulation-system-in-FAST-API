# Stock-Market-Simulation-System-in-FAST-API


This repository contains the implementation of a stock trading system with various endpoints for user registration and authentication, stock data management, transaction handling, and more. The system is designed to use Redis for caching and Celery for asynchronous task processing.

---

## Features 🚀

- **FASTAPI** RESTful API Development Framework
- **PostgreSQL** database
- **Poetry** Poetry is a tool for dependency management and packaging in Python
- **Redis** in-memory data structure store
- **Celery** worker and beat services for running background tasks asynchronously
- **Flower**  monitoring and managing Celery clusters
- **Swagger** API Documentation and Testing
- **Jwt** Token-based authentication mechanism
- **Docker** Containerization and Deployment Tool


## Requirements 📋

- Docker & Docker Compose - [Install and Use Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)
- Python 3.10 or higher

---

## Getting Started 🏁

### Development Prerequisites

Follow the steps below to set up the stock trading system:

#### Clone the Repository:

```
git clone https://github.com/usmancodegraphers/stock-market-simulation-system-in-FAST-API.git
cd stock-market-simulation-system-in-FAST-API
```


## For Docker Setup ⚙️

#### Build docker

```
sudo docker-compose build
```

#### Start docker

```
sudo docker-compose up
```

#### Build and run in detached mode

```
sudo docker-compose up --build -d
```

### Stop docker-compose

```
sudo docker-compose down
```
---
#### Access Swagger Documentation:

Visit [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)


#### Monitor Celery Tasks with Flower:

Visit [http://0.0.0.0:5555/](http://0.0.0.0:5555/) to monitor Celery tasks using Flower.

#### Access pgAdmin:

Visit [http://0.0.0.0:5050](http://0.0.0.0:5050) to monitor database.

### Test Cases

To run test, run the following command.

```
pytest -vv -s
```

---
