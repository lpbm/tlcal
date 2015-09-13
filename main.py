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

start = datetime.now() - timedelta(weeks=1)
_types = ["sc2", "hrt", "dot", "lol"]

_debug = False

wrapper = MongoWrapper(debug=_debug)

status = {}
for _type in _types:
    date = start
    while liquid.load_from_date(_type, date, persist=wrapper, debug=_debug):
        print("Week: %s - processing %s" % (date.strftime("%W"), _type))
        date += timedelta(weeks=1)
exit()
