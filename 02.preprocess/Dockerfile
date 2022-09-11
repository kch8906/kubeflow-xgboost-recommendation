FROM ubuntu:22.04
FROM python:3.8-slim

WORKDIR /tmp

RUN pip install -U pandas

COPY preprocess.py ./preprocess.py

# CMD [ "/bin/sh", "-c"]
ENTRYPOINT [ "python", "preprocess.py" ]
