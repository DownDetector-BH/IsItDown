FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    iputils-ping \
    net-tools \
    procps \
    curl \
    wget \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctfuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set proper ownership and remove write permissions
RUN chown -R root:root /app
RUN chmod -R 555 /app
RUN chown -R root:root /home/ctfuser
RUN chmod -R 555 /home/ctfuser

# Remove write permissions from common directories and make filesystem immutable
RUN chmod 555 /usr /usr/local /opt /etc
RUN find /usr -type d -exec chmod 555 {} \; 2>/dev/null || true
RUN find /opt -type d -exec chmod 555 {} \; 2>/dev/null || true

# Create a completely read-only user environment
RUN mkdir -p /home/ctfuser/.cache /home/ctfuser/.local
RUN chown -R root:root /home/ctfuser/.cache /home/ctfuser/.local
RUN chmod -R 555 /home/ctfuser/.cache /home/ctfuser/.local

# Switch to restricted user
USER ctfuser

# Set environment to discourage file operations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "app.py"]