#!/usr/bin/env python

import logging
import pprint

from fruits_and_vegetables_notifier.crawler import Crawler

logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)

current_fruits_and_vetegables = Crawler().get_current_fruits_and_vetegables()
pp.pprint(current_fruits_and_vetegables)
