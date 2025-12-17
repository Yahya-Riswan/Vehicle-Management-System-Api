# 1. Use an official lightweight Python image
FROM python:3.10-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Install system dependencies 
# (pkg-config and gcc are often needed for database drivers like mysqlclient)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first (to leverage Docker cache)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application code
COPY . .

# 7. Expose the port 
# (We use 8000 internally; Render will map this to the outside world)
EXPOSE 8000

# 8. Command to run the application
# We use "0.0.0.0" to allow external access inside the container network
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]