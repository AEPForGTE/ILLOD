FROM python:3.10.0-slim

HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD wget --no-proxy -O - -q localhost:8080/textobjects/ping

ENV PATH "$PATH:/root/.local/bin"
ENV PYTHONUNBUFFERED=1

RUN apt-get update -qq && apt-get install --no-install-recommends --yes build-essential

RUN mkdir -p /usr/ILLOD
WORKDIR /usr/ILLOD

COPY main.py /usr/ILLOD
COPY ILLOD_IST /usr/ILLOD/ILLOD_IST
COPY ILLOD_REFSQ /usr/ILLOD/ILLOD_REFSQ
COPY MAIN /usr/ILLOD/MAIN

RUN pip install --upgrade pip==22.0.2
RUN pip install -r MAIN/requirements_lin.txt

CMD ["python", "./main.py"]
