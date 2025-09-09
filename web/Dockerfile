# web/Dockerfile - lightweight Python image for Flask app
FROM python:3.10-slim

# Do not buffer Python stdout/stderr (helps logs)
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install system deps required for some Python packages (optional)
# Keep this minimal; uncomment if your requirements need compilation
# RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Flask port
EXPOSE 5000

# Provide default env var if not set from compose
ENV VLLM_URL=http://vllm:8000

# Run the app (assumes app.py will call app.run(host="0.0.0.0", port=5000))
CMD ["python", "app.py"]
