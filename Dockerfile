FROM docker:latest

RUN apk --no-cache add python3 py3-pip && \
    pip3 install docker-compose

COPY docker-compose-dev.yaml .
RUN pwd && docker-compose build

ENTRYPOINT ["docker-compose", "up"]
