# Use Python 3.10 base image (matches your .python-version file)
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/storage data/configs data/wizard_stages logs

# Expose port 80
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "--reload", "app.main:app"]