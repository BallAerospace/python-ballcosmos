 FROM alpine:3.12.7

# We require a local certificate file so set that up.
# You must place a valid cert.pem file in your COSMOS development folder for this work
# Comment out these lines if this is not required in your environment
COPY cacert.pem /devel/cacert.pem
ENV SSL_CERT_FILE=/devel/cacert.pem
ENV CURL_CA_BUNDLE=/devel/cacert.pem
ENV REQUESTS_CA_BUNDLE=/devel/cacert.pem

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache --virtual .build-dependencies \
        gcc musl-dev python3-dev \
    && apk add --update --no-cache git python3 py3-pip \
    && ln -sf python3 /usr/bin/python \
    && python -m pip install black \
    && git config --global http.sslVerify false \
    && /sbin/apk del --no-cache .build-dependencies
