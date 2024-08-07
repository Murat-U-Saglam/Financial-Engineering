# pull official base image
FROM python:3.10.4-slim-bullseye

# set work directory
WORKDIR /backend

ARG BACKEND_PORT 
ARG BACKEND_DEBUGGING_PORT 
ARG MYSQL_HOST 
ARG MYSQL_PORT 
ARG MYSQL_USER 
ARG MYSQL_PASSWORD 
ARG MYSQL_DATABASE

EXPOSE ${BACKEND_PORT} ${BACKEND_DEBUGGING_PORT}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BACKEND_PORT ${BACKEND_PORT}
ENV BACKEND_DEBUGGING_PORT ${BACKEND_DEBUGGING_PORT}
ENV MYSQL_HOST ${MYSQL_HOST}
ENV MYSQL_PORT ${MYSQL_PORT}
ENV MYSQL_USER ${MYSQL_USER}
ENV MYSQL_PASSWORD ${MYSQL_PASSWORD}
ENV MYSQL_DATABASE ${MYSQL_DATABASE}



RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git
    
# Upgrade pip 
RUN python -m pip install --upgrade pip

# copy requirements file
COPY requirements.txt requirements.txt

# install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /backend
