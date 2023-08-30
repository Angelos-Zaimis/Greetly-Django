# Use Python 3 as a parent image
FROM python:3

# Set the working directory in the container
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pip and dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app/

# Copy the entrypoint script
COPY entrypoint.sh /usr/src/app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
