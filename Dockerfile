FROM python:3.13-alpine

USER root

# Runtime dependency
RUN apk add --no-cache ffmpeg

RUN pip install markitdown

# Default USERID and GROUPID
ARG USERID=10000
ARG GROUPID=10000

USER $USERID:$GROUPID

ENTRYPOINT [ "markitdown" ]
