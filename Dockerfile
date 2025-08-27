# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install deps first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Ensure the start script is executable
RUN chmod +x /app/start.sh

# Render will provide $PORT; start.sh runs migrations then gunicorn
CMD ["/app/start.sh"]
