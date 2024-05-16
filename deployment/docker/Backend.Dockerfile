FROM python:3.12-slim

WORKDIR /app

COPY ../../ .

RUN python3 -m pip install --upgrade pip

RUN pip install -r ./src/requirements.txt
