
# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /
WORKDIR /

# Copy the current directory contents into the container at /app
COPY . /

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install default-jdk for Solr
RUN apt-get update && apt-get install -y default-jdk

# Download and install Solr
RUN curl -O https://dlcdn.apache.org/solr/solr/9.2.0/solr-9.2.0.tgz && \
    tar xzf solr-9.2.0.tgz solr-9.2.0/bin/install_solr_service.sh && \
    bash ./solr-9.2.0/bin/install_solr_service.sh solr-9.2.0.tgz



# Start Solr and run migrations, collectstatic, and gunicorn
CMD service solr start && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    gunicorn mysite.wsgi
