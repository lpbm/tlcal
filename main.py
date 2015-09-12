from datetime import datetime, timedelta
import liquid
from liquid.persist.mongowrapper import MongoWrapper

"""
"""

__author__ = "Marius Orcsik <marius@habarnam.ro>"
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2015 Marius Orcsik"
__license__ = "MIT"

week = {}

# 2015-09-29
start = datetime(year=2015, month=8, day=1)
_types = ["sc2", "hrt", "dot", "lol"]

wrapper = MongoWrapper()

status = {}
for _type in _types:
    date = start
    status[date.strftime("%Y%m%d")] = False
    while liquid.load_from_date(_type, date, persist=wrapper):
        print("Week: %s" % start.strftime("%W"))
        status[date.strftime("%Y%m%d")] = True

        date += timedelta(weeks=1)
exit()
