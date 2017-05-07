# Use an official Python runtime as a base image
FROM frolvlad/alpine-python3

# Set the working directory to /app
WORKDIR /moodle_scraper

# Copy the current directory contents into the container at /app
ADD . /moodle_scraper

# Install any needed packages specified in requirements.txt
# RUN apt-get install libfontconfig

RUN pip install -r requirements.txt

RUN . bin/activate

RUN ls
RUN pwd

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "moodle_scraper.py"]