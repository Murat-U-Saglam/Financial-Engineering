# pull official base image
FROM python:3.12-slim-bullseye

# set work directory
WORKDIR /src

ARG BACKEND_PORT=${BACKEND_PORT} 

ARG BACKEND_DEBUGGING_PORT=${BACKEND_DEBUGGING_PORT}

EXPOSE ${BACKEND_PORT} ${BACKEND_DEBUGGING_PORT}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Upgrade pip 
RUN python -m pip install --upgrade pip

WORKDIR /backend/app

# copy requirements file
COPY ./requirements.txt requirements.txt

# install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# copy project
COPY . .

