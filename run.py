#!/usr/bin/env python

import logging
import pprint
from datetime import datetime

from fruits_and_vegetables_notifier.crawler import Crawler
from fruits_and_vegetables_notifier.diff import Diff

logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)

current_month = int(datetime.now().strftime('%m'))
next_month = current_month + 1 if current_month < 12 else 1
current_fruits_and_vegetables = Crawler().get_fruits_and_vegetables_of_month(current_month)
next_fruits_and_vegetables = Crawler().get_fruits_and_vegetables_of_month(next_month)

print("Fruits and vegetables of month %s:" % current_month)
pp.pprint(current_fruits_and_vegetables)

print("Next incoming fruits:")
pp.pprint(Diff().next_fruits(current_fruits_and_vegetables, next_fruits_and_vegetables))

print("Next incoming vegetables:")
pp.pprint(Diff().next_vegetables(current_fruits_and_vegetables, next_fruits_and_vegetables))
