# pull official base image
FROM python:3.12-slim-bullseye

# set work directory
WORKDIR /src

ARG FRONTEND_PORT=${FRONTEND_PORT}

ARG FRONTEND_DEBUGGING_PORT=${FRONTEND_DEBUGGING_PORT}

EXPOSE ${FRONTEND_DEBUGGING_PORT} ${FRONTEND_PORT} 

WORKDIR /frontend/app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git

# copy requirements file
COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

HEALTHCHECK CMD curl --fail http://localhost:${FRONTEND_PORT}/_stcore/health

COPY . .