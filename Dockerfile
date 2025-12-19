FROM ubuntu:24.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    openssh-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create a virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements
COPY bridge/requirements.txt /app/bridge/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/bridge/requirements.txt

# Copy application code
COPY bridge /app/bridge
COPY PenaltyBoxConfigurator_Mockup.html /app/PenaltyBoxConfigurator_Mockup.html

# Create directory for repos
RUN mkdir -p /app/repos

# Expose port
EXPOSE 8000

# Run the application
CMD ["/app/venv/bin/python", "bridge/main.py"]
