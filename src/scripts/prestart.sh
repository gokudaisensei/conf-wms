#!/bin/bash

# Let the DB start
python /usr/src/app/app/backend_pre_start.py

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

# Create initial data in DB
python /usr/src/app/app/initial_data.py

exec uvicorn app.api.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
