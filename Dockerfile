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

RUN pip3 install -r requirements.txt

EXPOSE 6161

HEALTHCHECK CMD curl --fail http://localhost:6161/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=6161", "--server.address=0.0.0.0", "server.runOnSave=True"]