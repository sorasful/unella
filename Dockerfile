FROM python:3.11-slim-bullseye


RUN apt-get update \
  && apt-get install -y build-essential tree wget git gcc

# install golang
RUN wget https://dl.google.com/go/go1.19.8.linux-amd64.tar.gz \
  && tar -C /usr/local -xzf go1.19.8.linux-amd64.tar.gz \
  && rm go1.19.8.linux-amd64.tar.gz

ENV GOPATH /go
ENV PATH $PATH:/usr/local/go/bin:$GOPATH/bin
# install gitleaks
RUN go install github.com/zricethezav/gitleaks/v8@latest
RUN git config --global --add safe.directory /path

COPY requirements.txt /opt/unella/

RUN python -m pip install -r /opt/unella/requirements.txt


ENV PYTHONPATH /opt/unella:$PYTHONPATH

RUN mkdir /path


COPY . /opt/unella/


WORKDIR /opt/unella

ENTRYPOINT ["python", "unella/main.py"]
