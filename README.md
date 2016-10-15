# fruits-and-vegetables-notifier

[![Build Status](https://travis-ci.org/damienbeaufils/fruits-and-vegetables-notifier.svg?branch=master)](https://travis-ci.org/damienbeaufils/fruits-and-vegetables-notifier)

Crawl fruits and vegetables of current and next months, then send results by mail.

## Install

```
virtualenv -p /usr/bin/python3 venv
. venv/bin/activate
pip install -r requirements.txt
```

## Test

```
pytest
```

## Run

```
export MJ_APIKEY_PUBLIC=your_mailjet_api_public_key
export MJ_APIKEY_PRIVATE=your_mailjet_api_private_key
export FROM_EMAIL=your.sender.email@example.org
export TO_EMAILS=recipent1.email@example.org,recipent2.email@example.org
export REPLY_TO=your.replyto.email@example.org (optional)

python run.py
```
