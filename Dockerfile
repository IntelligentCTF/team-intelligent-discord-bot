FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        tesseract-ocr \
        libtesseract-dev \
        git \
        cmake \
        make \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create data directory (where persistent data will be stored)
RUN mkdir -p /app/data

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone and build pycdc
RUN git clone https://github.com/zrax/pycdc /tmp/pycdc && \
    cd /tmp/pycdc && \
    cmake . && \
    make && \
    mv pycdc /usr/local/bin/ && \
    rm -rf /tmp/pycdc

# Copy source code
COPY . .

# Default command (can be overridden by docker-compose)
CMD ["python3", "main.py"]
