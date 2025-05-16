FROM python:3.11-slim

WORKDIR /app

# Copy into the container
COPY . .

# Run
CMD ["python", "main.py"]
