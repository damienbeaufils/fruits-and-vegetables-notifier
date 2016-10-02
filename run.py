#!/usr/bin/env python

import logging
import pprint
from datetime import datetime

from fruits_and_vegetables_notifier.crawler import Crawler

logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)

current_month = datetime.now().strftime('%m')
current_fruits_and_vegetables = Crawler().get_fruits_and_vegetables_of_month(current_month)
print("Fruits and vegetables of month %s:" % current_month)
pp.pprint(current_fruits_and_vegetables)
