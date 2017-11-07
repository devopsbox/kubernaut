FROM python:3.6-alpine
MAINTAINER Datawire <dev@datawire.io>
LABEL PROJECT_REPO_URL         = "git@github.com:datawire/forge-jdk-multimodule.git" \
      PROJECT_REPO_BROWSER_URL = "https://github.com/datawire/forge-jdk-multimodule" \
      DESCRIPTION              = "Datawire Forge multi-module JDK example" \
      VENDOR                   = "Datawire, Inc." \
      VENDOR_URL               = "https://datawire.io/"

COPY requirements.txt .
RUN  pip install -Ur requirements.txt

COPY . .
RUN  pip install -e .

ENTRYPOINT ["/bin/sh", "-c", "kubernaut \"$@\"", "--"]
