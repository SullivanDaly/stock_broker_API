# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app/
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the command to start uWSGI
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "stock_broker.wsgi:broker_API"]