# Use an official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Command to run the app
CMD ["waitress-serve", "--listen=0.0.0.0:8080", "app:app"]