FROM python:3.9-slim

# Define working directory.
WORKDIR /app
COPY . /app/

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos "" user

# Install tools
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt -t /app

# Optional: install coverage (commented out)
# RUN pip3 install coverage

# Change ownership
RUN chown -R user:user /app
# RUN chmod +x ./run_tests.sh
USER user

# Install FastAPI dependencies from requirements.txt
# RUN pip3 install --no-cache-dir -r /app/app/requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Create the logs directory and file
RUN mkdir -p /app/tmp && touch /app/tmp/fastapi.log && chmod -R 777 /app/tmp

# Start Uvicorn and redirect logs to a file
CMD ["/bin/sh", "-c", "/home/user/.local/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > /app/tmp/fastapi.log 2>&1"]