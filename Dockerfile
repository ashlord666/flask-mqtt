# Use the official Python 3.13 slim image as the base image
# 'slim' variant is smaller than the full Python image
FROM python:3.13-slim

# Set the working directory inside the container to /app
# All subsequent commands will be executed from this directory
WORKDIR /app

# Copy the requirements.txt file from the host to the container's /app directory
COPY requirements.txt .

# Install the Python dependencies listed in requirements.txt
# RUN executes this command during the image build process
RUN pip install -r requirements.txt

# Copy the app.py file from the host to the container's /app directory
COPY app.py .

# Expose port 5000 to allow external connections to the container
# This is informational and doesn't actually publish the port
EXPOSE 5000

# Specify the command to run when the container starts
# Runs app.py using the Python interpreter
CMD ["python", "app.py"]
