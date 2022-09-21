FROM python:3.8-slim
WORKDIR /tmp
RUN apt-get update
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY metrics.py ./metrics.py
ENTRYPOINT [ "python", "metrics.py" ]