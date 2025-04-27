# Use the official Azure Functions Python base image
FROM mcr.microsoft.com/azure-functions/python:4-python3.9

# Copy requirements and install dependencies
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

# Copy the function app code
COPY . /home/site/wwwroot

# Set the working directory
WORKDIR /home/site/wwwroot

# Expose port 80
EXPOSE 80
