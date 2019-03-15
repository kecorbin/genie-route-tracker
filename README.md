# genie-route-tracker

## Requirements

* python3

## Installation

```
pip install -r requirements.txt
```

## Usage

```
 python route-tracker.py --testbed default_testbed.yaml --neighbor 1.1.1.1
```


## Docker instructions

```
docker build -t rt .
docker run -ti \
           -v $(pwd)/router2.yaml:/scripts/default_testbed.yaml \
           --env-file .envfile \
           rt \
           /scripts/ospf_checker.sh
```
