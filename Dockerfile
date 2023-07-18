FROM python:3.11.0-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/app"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set work directory
WORKDIR /usr/src/app

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Make entrypoint script executable
COPY ./scripts/prestart.sh ./scripts/prestart.sh
RUN chmod +x ./scripts/prestart.sh

# Copy the rest of the project
COPY . .

# Expose port at which uvicorn runs
EXPOSE 8000

# Set entrypoint
ENTRYPOINT [ "/usr/src/app/scripts/prestart.sh" ]
