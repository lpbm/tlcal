from datetime import datetime, timedelta
from liquid.persist.mongowrapper import MongoWrapper
from liquid.persist.outputwrapper import OutputWrapper
from liquid import load_from_date
from liquid.scraper.html import Html
from argparse import ArgumentParser
from sys import argv

"""
"""

__author__ = "Marius Orcsik <marius@habarnam.ro>"
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2015 Marius Orcsik"
__license__ = "MIT"

week = {}

default_types = list(Html.base_uris.keys())
default_start = datetime.now() - timedelta(weeks=1)

parser = ArgumentParser(prog="tlscraper")
parser.add_argument('--start-date', help="The start date for loading events YYYY-MM-DD",
                    default=default_start.strftime("%Y-%m-%d"))
parser.add_argument('--debug', nargs='?', help="Enable debug output", const=True, default=False)
parser.add_argument('--dry-run', nargs='?', help="Do not persist", const=True, default=False)
parser.add_argument('--calendar', nargs='+',  help="Which calendars to load events from",
                    default=default_types[0], choices=default_types, metavar="sc2")

args = parser.parse_args()
if len(argv) == 1:
    parser.print_help()
    exit(1)

debug = args.debug
start = datetime.strptime(args.start_date, "%Y-%m-%d")
types = args.calendar
dry_run = args.dry_run

if dry_run:
    wrapper = OutputWrapper(debug=debug)
else:
    wrapper = MongoWrapper(debug=debug)

for _type in types:
    date = start
    while load_from_date(_type, date, persist=wrapper, debug=debug):
        date += timedelta(weeks=1)
exit()
