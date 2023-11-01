FROM python:3.11-slim-bullseye


COPY requirements.txt /opt/unella/


RUN apt-get update \
  && apt-get install -y build-essential tree git \
  && python -m pip install -r /opt/unella/requirements.txt


ENV PYTHONPATH /opt/unella:$PYTHONPATH

RUN mkdir /path


COPY . /opt/unella/


WORKDIR /opt/unella

ENTRYPOINT ["python", "unella/main.py"]
