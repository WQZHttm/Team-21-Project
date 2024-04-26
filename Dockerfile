# Use an official Python runtime as a parent image
FROM python:3.10.6

# Set the working directory in the container
WORKDIR /main

# Copy the wait-for-it script into the container
COPY wait-for-it.sh /usr/wait-for-it.sh

# Copy the current directory contents into the container at /app
COPY . /main

# Install any needed packages specified in requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Expose the port number on which the Dash app will run
EXPOSE 8050

# Run app.py when the container launches
CMD ["python", "main.py"]


