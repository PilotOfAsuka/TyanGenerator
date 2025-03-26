# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your project files into the container
COPY . .

# Load .env variables (optional)
ENV PYTHONUNBUFFERED=1

# Run the bot (replace with your actual main file)
CMD ["python", "main.py"]
