#!/bin/bash

# Stop the Is It Down application
docker-compose down

if [ $? -eq 0 ]; then
    echo "Application stopped successfully."
else
    echo "Failed to stop the application."
    exit 1
fi