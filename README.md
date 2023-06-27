# bitespeed-identity-reconciliation

This repository contains the bitespeed-identity-reconciliation Django project that can be easily set up and run using Docker.

## Documentation

API Documentation is hosted locally - application should be run first

- [API Schema](http://localhost:8000/api/schema/)
- [Swagger Documentation](http://localhost:8000/api/schema/swagger-ui/)
- [ReDoc Documentation](http://localhost:8000/api/schema/redoc/)


## Prerequisites

Make sure you have the following tools installed on your system:

- Docker: [Install Docker](https://www.docker.com/get-started)

## Getting Started

Follow these steps to set up and run the Django project:

1. Clone the repository:


   ```bash
   git clone https://github.com/aravind575/bitespeed-identity-reconciliation
   cd bitespeed-identity-reconciliation

2. Build the Docker image:

   ```bash
   docker build -t bitespeed-identity-reconciliation .

3. Run the Docker container:
   
   ```bash
   docker run -p 8000:8000 bitespeed-identity-reconciliation