FROM python:3.10.12

ENV TZ=America/Sao_Paulo
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /build
COPY requirements.txt .
RUN pip install --upgrade pip &&  pip install -r requirements.txt

WORKDIR /workspace
ADD . /workspace
RUN chmod +x /workspace/main.sh

ENTRYPOINT ["tail", "-f", "/dev/null"]