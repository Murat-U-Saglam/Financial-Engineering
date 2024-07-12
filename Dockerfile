# pull official base image
FROM python:3.12-slim-bullseye

# set work directory
WORKDIR /src


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/streamlit/streamlit-example.git .

# copy requirements file
COPY ./requirements.txt /src/requirements.txt

RUN pip3 install -r requirements.txt

ARG FRONTEND_PORT

ARG FRONTEND_DEBUGGING_PORT

ENV FRONTEND_PORT=${FRONTEND_PORT}

ENV FRONTEND_DEBUGGING_PORT=${FRONTEND_DEBUGGING_PORT}

EXPOSE ${FRONTEND_PORT} ${FRONTEND_DEBUGGING_PORT} 

HEALTHCHECK CMD curl --fail http://localhost:6161/_stcore/health

