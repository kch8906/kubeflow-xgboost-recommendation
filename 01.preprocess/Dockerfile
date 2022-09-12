FROM python:3.8-slim

WORKDIR /tmp

RUN pip install -U pandas boto3

COPY preprocess.py ./preprocess.py

ENTRYPOINT [ "python", "preprocess.py" ]
