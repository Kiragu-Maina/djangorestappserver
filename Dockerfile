# Use an official Python runtime as a parent image
FROM python:3.8


# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create virtual environment and activate it
RUN python -m venv /opt/venv && . /opt/venv/bin/activate

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ARG PGDATABASE
ARG PGUSER
ARG PGPASSWORD
ARG PGHOST
ARG PGPORT
ARG REDISHOST
ARG REDISPASSWORD
ARG REDISUSER
ARG REDISPORT

# Run migrations and collect static files
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn mysite.wsgi  --bind 0.0.0.0:$PORT




