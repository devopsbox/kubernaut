FROM python:3.6-alpine
MAINTAINER Datawire <dev@datawire.io>
LABEL PROJECT_REPO_URL         = "git@github.com:datawire/kubernaut.git" \
      PROJECT_REPO_BROWSER_URL = "https://github.com/datawire/kubernaut" \
      DESCRIPTION              = "Kubernaut - Disposable Kubernetes clusters for rapid development and testing" \
      VENDOR                   = "Datawire, Inc." \
      VENDOR_URL               = "https://datawire.io/" \
      PROJECT_URL              = "https://kubernaut.io/"

ENV SCOUT_DISABLE=1

COPY requirements.txt .
RUN  pip install -Ur requirements.txt

COPY . .
RUN  pip install -e .

ENTRYPOINT ["/bin/sh", "-c", "kubernaut \"$@\"", "--"]
