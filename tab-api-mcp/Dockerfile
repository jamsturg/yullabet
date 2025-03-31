FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir .

# Copy the rest of the application
COPY . .

# Expose the ports
EXPOSE 8081 8082

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the server
CMD ["python", "-m", "tab_api_mcp"]