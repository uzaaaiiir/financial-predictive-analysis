# Use Python image.
FROM python:3.10

# Set the working directory in the container.
WORKDIR /app

# Copy the dependencies file to the working directory.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local app directory to the working directory.
COPY . .

# Export the port the app runs on.
EXPOSE 8000

# Run the command to run FastAPI app.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
