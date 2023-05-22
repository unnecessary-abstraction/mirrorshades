# Copyright The mirrorshades Contributors.
# SPDX-License-Identifier: Apache-2.0

FROM python:3.11-alpine

COPY . /build-dir

RUN apk add --no-cache dumb-init git rclone isync && \
    pip install --no-cache-dir yacron PyGithub python-gitlab /build-dir && \
    rm -rf /build-dir

ENTRYPOINT ["/usr/bin/dumb-init"]
CMD ["mirrorshades"]
