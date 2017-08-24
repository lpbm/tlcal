from argparse import ArgumentParser
from datetime import datetime, timedelta
from sys import argv

from persist.eventencoder import EventEncoder
from pymongo.database import Database

from liquid import load_event_data
from liquid.scraper.html import Html
from persist.mongowrapper import MongoWrapper

"""
"""

__author__ = "Marius Orcsik <marius@habarnam.ro>"
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2015 Marius Orcsik"
__license__ = "MIT"

week = {}

default_types = list(Html.base_uris.keys())
default_start = datetime.now() - timedelta(days=1)

parser = ArgumentParser(prog="tlevents")
parser.add_argument('--start-date', help="The start date for loading events YYYY-MM-DD",
                    default=default_start.strftime("%Y-%m-%d"))
parser.add_argument('--debug', nargs='?', help="Enable debug output", const=True, default=False)
parser.add_argument('--dry-run', nargs='?', help="Do not persist", const=True, default=False)
parser.add_argument('--calendar', nargs='+',  help="Which calendars to load events from",
                    default=default_types[0], choices=default_types, metavar=default_types[0])

args = parser.parse_args()
if len(argv) == 1:
    parser.print_help()
    exit(1)

debug = args.debug
start = datetime.strptime(args.start_date, "%Y-%m-%d")
days_delta = 1
types = args.calendar
dry_run = args.dry_run

if dry_run:
    print('Need Mongo connection')
    exit(1)
else:
    wrapper = MongoWrapper(debug=debug)

encoder = EventEncoder()

date = start
date_end = start + timedelta(days=days_delta)

for _type in types:
    if debug:
        print("Loading events from calendar %s" % _type)

    if not isinstance(wrapper.db, Database):
        print("Failed to connect to Mongo")
        exit(1)

    while True:
        if debug:
            print("Date %s + %d days" % (date.strftime("%Y-%m-%d"), days_delta), end=" ", flush=True)

        _events = []
        what = {"type": _type, "start_time": {"$gte": date, "$lt": date_end}}
        count_events = wrapper.db.events.count(what)
        if count_events == 0:
            if days_delta <= 7:
                days_delta += 2
            else:
                break
        else:
            if days_delta > 2:
                days_delta = 1

        cursor = wrapper.db.events.find(what)
        for db_event in cursor:
            _events.append(encoder.decode(db_event))

        if debug:
            print("... found: %d" % len(_events))

        if len(_events) > 0:
            load_event_data(_events, persist=wrapper, debug=debug)

        date = what["start_time"]["$lt"]
        date_end = date + timedelta(days=days_delta)

        what["start_time"]["$gte"] = date
        what["start_time"]["$lt"] = date_end

exit()
