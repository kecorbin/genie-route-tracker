FROM ciscotestautomation/pyats:latest-alpine
COPY requirements.txt /tmp/requirements.txt
RUN /pyats/bin/pip install -r /tmp/requirements.txt

COPY . /scripts
WORKDIR /scripts
