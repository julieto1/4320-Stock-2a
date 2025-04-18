# Use an official Python runtim as the parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run upgrade pip
RUN pip install --upgrade pip

# Install any requirements needed from a requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run when starting the container
CMD ["python", "app.py"]
