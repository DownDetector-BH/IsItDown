# Is It Down? - CTF Challenge

A Flask web application that provides website connectivity testing services.

## Overview

This web application provides a simple interface for checking website and server connectivity using curl commands.

### Features

- Clean, responsive web interface
- Real-time connectivity testing  
- Global network monitoring

## Prerequisites

- Docker and Docker Compose installed
- Basic understanding of web applications

## Quick Setup

1. **Clone this repository**
```bash
git clone <repository-url>
cd isitdown-ctf
```

2. **Start the application**
```bash
./start.sh
```
Or manually:
```bash
docker-compose up --build
```

3. **Access the application**
- Open your browser to `http://localhost:5000`
- The application provides two modes: Easy and Medium

## Configuration

### Adding Environment Variables
Set additional environment variables in `docker-compose.yml`:
```yaml
environment:
  - FLASK_ENV=production
```

## Stopping the Challenge

```bash
docker-compose down
```

## Troubleshooting

### View logs
```bash
docker-compose logs -f
```

### Restart the application
```bash
docker-compose restart
```

### Rebuild after changes
```bash
docker-compose up --build
```