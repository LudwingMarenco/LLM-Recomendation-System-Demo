FROM python:3.10.12

ENV TZ=America/Sao_Paulo
ENV DEBIAN_FRONTEND=noninteractive

RUN pip install --upgrade pip &&  pip install mesop

WORKDIR /workspace
ADD . /workspace

RUN chmod +x /workspace/run_mesop.sh