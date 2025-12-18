# Base Image: Python 3.10 (Slim version to keep it small)
FROM python:3.10-slim-bullseye


# 1. Install Java (Required for Spark) and System Tools
# 'procps' is needed for Spark UI, 'libgeos-dev' for GeoPandas
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless procps libgeos-dev && \
    rm -rf /var/lib/apt/lists/*

# 2. Set Environment Variables
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PYSPARK_PYTHON=python3

# 3. Set Working Directory
WORKDIR /app

# 4. Install Python Libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Default Command (Keeps the container running)
CMD ["tail", "-f", "/dev/null"]