# Use an official Python runtime as a parent image
FROM python:3.10.6

# Set the working directory in the container
WORKDIR C:\Users\user\OneDrive - National University of Singapore\DSA3101\Project\Team-21-Project

# Copy the current directory contents into the container at /main
COPY . .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "main.py"]
