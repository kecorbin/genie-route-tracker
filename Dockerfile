FROM ciscotestautomation/pyats:latest
# WIP: support alpine image
# FROM ciscotestautomation/pyats:latest-alpine
COPY . /scripts
WORKDIR /scripts
CMD python /scripts/route-tracker.py --testbed /scripts/virl2.yaml --neighbor 1.1.1.2
