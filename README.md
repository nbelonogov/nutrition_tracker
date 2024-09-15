# Nutrition tracker dockerized Project

This project is a Django 4.2 application using Django Rest Framework (DRF) and PostgreSQL 16. The project is fully containerized using Docker and Docker Compose.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/nbelonogov/nutrition_tracker.git
cd nutrition_tracker
```

### 2. Add environment variables.
Create a .env file in the root directory and add your environment variables. For example:
```
SECRET_KEY=your_secret_key
DEBUG=1
DB_NAME="db_name"
DB_USER="db_user"
DB_PASSWORD='db_password'
DB_HOST="db_host"
DB_PORT="5432"
```
### 3. Build and Run the Application
Use the following command to build and start the containers, apply migrations, and start the Django development server.
```bash
docker-compose up -d --build
```
This command will:
* Build the Docker images.
* Start the PostgreSQL and Django containers.
* Automatically apply database migrations.

### 4. Load Initial Data (Optional)
```bash
docker-compose exec web python manage.py loaddata <your_fixture_file>.json
```

### 5.Access the Application
Once the application is running, you can access it at:
```
http://localhost:8000
```
## Additional Docker Commands
* Stop the application:
```bash
docker-compose down
```
* Rebuild the application:
```bash
docker-compose up -d --build
```
* Check logs:
```bash
docker-compose logs
```
* Run Django management commands:
```bash
docker-compose exec web python manage.py <command>
```
