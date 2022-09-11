FROM python:3.8-slim

WORKDIR /tmp

RUN pip install -U boto3

COPY download.py ./down_from_s3.py

ENTRYPOINT [ "python", "down_from_s3.py" ]