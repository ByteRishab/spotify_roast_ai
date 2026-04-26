# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Expose the port Hugging Face expects
EXPOSE 7860

# Start the app using Gunicorn for better performance
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]