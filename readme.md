
# REST API for "Teams" and "People"

This project is a RESTful API that provides CRUD (Create, Read, Update, Delete) operations for managing "teams" and the "people" within those teams.
## Table of Contents

1. [Tech Stack](#tech-stack)
2. [Installation](#installation)
3. [Running the Project](#running-the-project)
4. [Additional Information](#additional-information)
## Tech Stack

- **WEB-server**: Django
- **Database**: PostgreSQL 13
- **Containerization**: Docker
- **OPEN API Documentation**: Yasg/Swagger
## Installation

**Prerequisites**: Ensure Docker is installed on your system.
**Clone the Repository**: Use your preferred method to clone the project repository to your local machine.
**Build the Project**: Navigate to the project directory and execute the following command to build the necessary components:
```bash
docker-compose build
```
## Running the Project

1. Start the project using the following command:
```bash
docker-compose up
```
2. Access the API documentation by navigating to: http://127.0.0.1:8000/docs/ in your preferred web browser.
---
**NOTE:** If you encounter any access issues, please ensure that port 8000 is not being used by other services on your system.
---

## Additional Information

If there are any changes to the database models or structure, you will need to generate and apply migrations. This ensures that the database schema remains consistent with the codebase. Use the following commands to manage migrations:

- Generate migrations based on changes:
```bash
docker-compose run makemigrations
```
- Apply the generated migrations to update the database schema:
```bash
docker-compose run migrate