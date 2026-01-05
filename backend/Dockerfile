# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps (libpq for Postgres, plus build tools just in case)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

# Create folders for media/static (optional but handy)
RUN mkdir -p /app/media /app/static

# Default command: migrate then run gunicorn
# NOTE: for dev you might prefer runserver; see docker-compose override below.
CMD ["bash", "-lc", "python manage.py migrate && gunicorn backend.wsgi:application --bind 0.0.0.0:8000"]
