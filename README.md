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
docker build -t route-checker .
docker run -ti route-checker /bin/sh
```
