FROM python:3.12-slim

WORKDIR /app

# Copy simulator files
COPY simulator.py context.yaml triggers.yaml /app/
COPY static ./static


# Install dependencies
RUN pip install pyyaml flask

# Run Flask app
CMD ["python", "simulator.py"]




