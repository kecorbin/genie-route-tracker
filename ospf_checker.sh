#!/bin/sh

echo "Sleeping for 60 seconds"
sleep 60

source /pyats/bin/activate
cd /scripts
easypy ospf_neighbor_check_job.py -html_logs . -testbed_file default_testbed.yaml
pip install requests_toolbelt
python webex_teams_notifications.py
rm -rf archive
