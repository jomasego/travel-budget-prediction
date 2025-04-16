# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code directory into the container at /app
COPY src/ /app/src/

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable (optional, but good practice)
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_PORT=5001

# Run app.py when the container launches
# Use 0.0.0.0 to make it accessible outside the container
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
