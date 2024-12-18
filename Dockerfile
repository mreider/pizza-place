FROM python:3.10.4-slim-buster

# Set the working directory
WORKDIR /project

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "app.py"]