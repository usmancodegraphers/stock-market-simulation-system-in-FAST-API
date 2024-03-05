# stock-market-simulation-system-in-FAST-API


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


## Data Models Overview
### 🤵 Users

   - 'user_id': Unique identifier for each user.
   - 'username': User's username.
   - 'balance': User's current balance.

### 📈  StockData

   - 'ticker': Stock ticker symbol.
   -  'open_price': Opening stock price.
   -  'close_price': Closing stock price.
   -  'high': Highest stock price.
   -  'volume': Stock trading volume.
   -  'timestamp': Timestamp of stock data.


### 🔄 Transactions

   - 'transaction_id': Unique identifier for each transaction.
   - 'user_id': Foreign key referencing the Users table.
   - 'ticker': Stock ticker symbol.
   - 'transaction_type': Type of transaction (buy/sell).
   - 'transaction_volume': Volume of the transaction.
   - 'transaction_price': Price of the transaction.
   - 'timestamp': Timestamp of the transaction.

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


---

## Assumptions
- The system assumes a PostgreSQL database for storing user data, stock data, and transactions.
- Redis is used for caching user data and stock data to reduce database load.
- Celery is employed for handling asynchronous tasks, especially for processing transactions.
- Swagger documentation is available for easy exploration of the API endpoints.
- Flower is used for monitoring Celery tasks and their states

Feel free to modify the setup based on your specific requirements

---
