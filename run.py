#!/usr/bin/env python
import os
from datetime import datetime

from mailjet_rest import Client

from fruits_and_vegetables_notifier import logger
from fruits_and_vegetables_notifier.crawler import Crawler
from fruits_and_vegetables_notifier.diff import Diff
from fruits_and_vegetables_notifier.mailjet_sender import MailJetSender

current_month = int(datetime.now().strftime('%m'))
next_month = current_month + 1 if current_month < 12 else 1

crawler = Crawler()
diff = Diff()
mailjet_sender = MailJetSender()

api_key = os.environ['MJ_APIKEY_PUBLIC']
api_secret = os.environ['MJ_APIKEY_PRIVATE']
mailjet_client = Client(auth=(api_key, api_secret))

current_fruits_and_vegetables = crawler.get_fruits_and_vegetables_of_month(current_month)
next_fruits_and_vegetables = crawler.get_fruits_and_vegetables_of_month(next_month)

next_fruits = diff.next_fruits(current_fruits_and_vegetables, next_fruits_and_vegetables)
next_vegetables = diff.next_vegetables(current_fruits_and_vegetables, next_fruits_and_vegetables)

notification = mailjet_sender.build_notification(current_fruits_and_vegetables, next_fruits, next_vegetables)
notification_sent = mailjet_sender.send_notification(mailjet_client, notification)
if notification_sent:
    logger.info('Fruits and vegetables notification successfully sent!')
else:
    logger.error('Error when sending fruits and vegetables notification!')
