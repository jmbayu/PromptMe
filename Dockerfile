# Base image
FROM python:3.11-slim

# Set up the working directory
WORKDIR /app

# Copy all the application code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r all_requirements.txt

# Expose ports
EXPOSE 5000-5010

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["./entrypoint.sh"]
