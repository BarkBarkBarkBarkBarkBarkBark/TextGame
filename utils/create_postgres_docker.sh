#!/bin/bash
# This script creates a Docker container running PostgreSQL.
# Usage: ./create_postgres_docker.sh [postgres_user] [postgres_password] [database_name] [container_name] [host_port]
# Defaults: postgres_user="postgres", postgres_password="password", database_name="mydatabase", container_name="pg_container", host_port="5432"

POSTGRES_USER="${1:-postgres}"
POSTGRES_PASSWORD="${2:-postgres}"
POSTGRES_DB="${3:-climb}"
CONTAINER_NAME="${4:-climb}"
HOST_PORT="${5:-5432}"
IMAGE="postgres:latest"

echo "Creating Docker container '$CONTAINER_NAME' running PostgreSQL..."
docker run --rm --name "$CONTAINER_NAME" \
  -e POSTGRES_USER="$POSTGRES_USER" \
  -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  -e POSTGRES_DB="$POSTGRES_DB" \
  -p "$HOST_PORT":5432 \
  -d "$IMAGE"

if [ $? -eq 0 ]; then
  echo "Container '$CONTAINER_NAME' created successfully and running PostgreSQL."
else
  echo "Error creating Docker container '$CONTAINER_NAME'."
fi 