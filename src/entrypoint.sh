#!/bin/bash

# Wait for the database service to become available
until nc -z db 3306; do
  echo "Waiting for the database service to start..."
  sleep 1
done

# Check if there are any changes in the database schema
check_output=$(alembic check)
if echo "$check_output" | grep -q "New upgrade operations detected"; then
  echo "Changes detected in the database schema. Creating revision..."
  # Run the alembic revision command
  alembic revision --autogenerate -m "auto-generated migration"
  # Apply Alembic migration
  alembic upgrade head
elif echo "$check_output" | grep -q "Target database is not up to date"; then
  echo "Target database is not up to date. Applying migration..."
  # Apply Alembic migration
  alembic upgrade head
else
  echo "No changes detected in the database schema."
fi

# Start the uvicorn server
exec uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
