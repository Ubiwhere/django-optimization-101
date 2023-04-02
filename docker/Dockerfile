FROM python:3.10.9-slim-bullseye

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

# Install needed 
RUN apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client libpq-dev gcc git python3-dev gdal-bin gettext && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*

# Add requirements and install them
COPY requirements.txt requirements.txt
RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Needed for translations
ENV PYTHONPATH="/code:$PYTHONPATH"

# Copy the current directory contents into the container at /code/
COPY . /code/
# Set the working directory to /code/
WORKDIR /code/

# Run the entrypoint bash script
ADD docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
