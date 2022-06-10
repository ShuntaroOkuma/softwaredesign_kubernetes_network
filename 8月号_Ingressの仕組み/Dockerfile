FROM python:3.7

RUN apt update \
  && apt install -y wget \
  && rm -rf /var/lib/apt/lists/* \
  && wget https://storage.googleapis.com/kubernetes-release/release/v1.13.0/bin/linux/amd64/kubectl \
  && mv kubectl /usr/local/bin/kubectl \
  && chmod +x /usr/local/bin/kubectl

ADD app.py /app/
WORKDIR /app/
RUN pip install flask

