# Use Python 3.11.9 slim base image
FROM python:3.11.9-slim

# Set working directory inside container
WORKDIR /app

# Install PyYAML for YAML support
RUN pip install pyyaml

# Copy all project files into the container
COPY . .

# Run the simulator when container starts
CMD ["python", "simulator.py"]



