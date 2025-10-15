# Use a lightweight official Python image
FROM python:3.10-slim

# Set environment variables for non-root user and path
ENV PYTHONUNBUFFERED 1
ENV PATH="/home/user/.local/bin:$PATH"

# Create a non-root user and set up the working directory
RUN useradd -m -u 1000 user
USER user
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code and the trained model artifact
COPY --chown=user:user . .

# Hugging Face Spaces with Docker requires the service to listen on port 7860
EXPOSE 7860

# Command to run the FastAPI application using Uvicorn
# The command is [uvicorn module:app_object --host 0.0.0.0 --port 7860]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
