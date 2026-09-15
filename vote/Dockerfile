FROM python:3.12-slim

# Prevent Python from creating .pyc files
# and ensure logs are sent directly to stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first for better Docker layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app ./app

# Create and use a non-root user
RUN useradd --create-home appuser

USER appuser

EXPOSE 5000

CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--threads", "4", \
     "--timeout", "30", \
     "app.main:app"]