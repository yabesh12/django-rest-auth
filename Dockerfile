# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables for Docker image
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Expose port 8000 for the Django app
EXPOSE 8005


# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8005"]
