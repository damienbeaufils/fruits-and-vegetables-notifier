#!/usr/bin/env python
import os
from datetime import datetime

from mailjet_rest import Client

from fruits_and_vegetables_notifier import logger
from fruits_and_vegetables_notifier.crawler import Crawler
from fruits_and_vegetables_notifier.diff import Diff
from fruits_and_vegetables_notifier.mailjet_sender import MailJetSender


def main(crawler, mailjet_sender, current_month):
    travis_event_type_key = 'TRAVIS_EVENT_TYPE'
    if travis_event_type_key in os.environ and os.environ[travis_event_type_key] != 'cron':
        return

    next_month = current_month + 1 if current_month < 12 else 1

    current_fruits_and_vegetables = crawler.get_fruits_and_vegetables_of_month(current_month)
    next_fruits_and_vegetables = crawler.get_fruits_and_vegetables_of_month(next_month)

    logger.debug("Current fruits and vegetables: %s", current_fruits_and_vegetables)
    logger.debug("Next fruits and vegetables: %s", next_fruits_and_vegetables)

    diff = Diff()
    next_fruits = diff.next_fruits_without_current(current_fruits_and_vegetables, next_fruits_and_vegetables)
    next_vegetables = diff.next_vegetables_without_current(current_fruits_and_vegetables, next_fruits_and_vegetables)

    mailjet_client = __build_mailjet_client()
    notification = mailjet_sender.build_notification(current_fruits_and_vegetables['fruits'],
                                                     current_fruits_and_vegetables['vegetables'],
                                                     next_fruits, next_vegetables)

    notification_sent = mailjet_sender.send_notification(mailjet_client, notification)
    if notification_sent:
        logger.info('Fruits and vegetables notification successfully sent!')
    else:
        logger.error('Error when sending fruits and vegetables notification!')


def __build_mailjet_client():
    api_key = os.environ['MJ_APIKEY_PUBLIC']
    api_secret = os.environ['MJ_APIKEY_PRIVATE']
    mailjet_client = Client(auth=(api_key, api_secret))
    return mailjet_client


if __name__ == '__main__':
    current_month = int(datetime.now().strftime('%m'))
    main(Crawler(), MailJetSender(), current_month)
