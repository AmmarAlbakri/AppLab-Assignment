# Use an official Python slim image.
FROM python:3.13-slim

# Install system dependencies and supervisor.
RUN apt-get update && apt-get install -y supervisor && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements.txt file into the container.
COPY requirements.txt .

# Upgrade pip and install Python dependencies.
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your application code into the container.
COPY . /app

# Expose the ports that your backend and frontend will use.
EXPOSE 8000 7860

# Copy the Supervisor configuration file into the container.
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run Supervisor which will launch the FastAPI and Gradio processes.
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
