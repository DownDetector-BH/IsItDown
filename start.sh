#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and start the container
docker-compose down 2>/dev/null
docker-compose up --build -d

if [ $? -eq 0 ]; then
    echo "Application is now running at: http://localhost:5000"
else
    echo "Failed to start the application. Check the logs with: docker-compose logs"
    exit 1
fi