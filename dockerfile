FROM python:3.10.0-slim

HEALTHCHECK --interval=10s --timeout=5s --retries=3 CMD wget --no-proxy -O - -q localhost:8080/textobjects/ping

#ARG http_proxy=http://128.7.3.56:3128
#ARG https_proxy=http://128.7.3.56:3128
ENV PATH "$PATH:/root/.local/bin"

RUN apt-get update -qq && apt-get install --no-install-recommends --yes build-essential

RUN mkdir -p /usr/ILLOD
WORKDIR /usr/ILLOD

COPY main.py /usr/ILLOD
COPY ILLOD_IST /usr/ILLOD/ILLOD_IST
COPY ILLOD_REFSQ /usr/ILLOD/ILLOD_REFSQ
COPY MAIN /usr/ILLOD/MAIN

RUN pip install --upgrade pip==22.0.2
RUN pip install --proxy http://128.7.3.56:3128 -r MAIN/requirements_lin.txt

CMD ["python", "./main.py"]
