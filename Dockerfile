# Copyright 2021 Ball Aerospace & Technologies Corp.
# All Rights Reserved.
#
# This program is free software; you can modify and/or redistribute it
# under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; version 3 with
# attribution addendums as found in the LICENSE.txt

FROM alpine:3.12.7

# We require a local certificate file so set that up.
# Comment out these lines if this is not required in your environment
COPY cacert.pem /devel/cacert.pem
ENV SSL_CERT_FILE=/devel/cacert.pem
ENV CURL_CA_BUNDLE=/devel/cacert.pem
ENV REQUESTS_CA_BUNDLE=/devel/cacert.pem

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

RUN apk add --no-cache --virtual .build-dependencies \
        gcc musl-dev python3-dev \
    && apk add --update --no-cache git python3 py3-pip \
    && ln -sf python3 /usr/bin/python \
    && python -m pip install --upgrade pip \
    && python -m pip install pytest black flake8 coverage \
    && git config --global http.sslVerify false \
    && /sbin/apk del --no-cache .build-dependencies

COPY ./ ./

RUN [ "python", "/app/setup.py", "develop" ]
# RUN ["python", "/app/setup.py", "install"]

# CMD [ "tail", "-f", "/dev/null" ]
CMD [ "coverage", "run", "-m", "pytest", "./tests/" ]