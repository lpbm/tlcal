from sys import argv

from argparse import ArgumentParser
from mastodon import Mastodon
from persist.mongowrapper import MongoWrapper
from datetime import datetime, timedelta
from liquid.scraper.html import Html as liquid_Html
from plusfw.scraper.html import Html as plusfw_Html
try:
    from credentials import get_credentials
except ImportError:
    print("Fatal error: credentials file is not accessible")
    exit(0)

plusfw_types = list(plusfw_Html.base_uris.keys())
liquid_types = list(liquid_Html.base_uris.keys())
default_types = plusfw_types + liquid_types

parser = ArgumentParser(prog="tooter")
parser.add_argument('--debug', nargs='?', help="Enable debug output", const=True, default=False)
parser.add_argument('--dry-run', nargs='?', help="Do not toot", const=True, default=False)
parser.add_argument('--interval', nargs='?', help="Interval of minutes to search for events", type=int, default=5)
parser.add_argument('--types', nargs='+',  help="Which types to load events for",
                    default=default_types[0], choices=default_types, metavar=default_types[0])

args = parser.parse_args()
if len(argv) == 1:
    parser.print_help()
    exit(1)

debug = args.debug
types = args.types
dry_run = args.dry_run
interval = args.interval

now = datetime.now()
now_with_interval = now + timedelta(minutes=interval)

start_time = min(now, now_with_interval)
end_time = max(now, now_with_interval)

soonish_events = MongoWrapper(debug=True).load_events(types, start_time, end_time)
if debug:
    if len(soonish_events) == 0:
        print("No events found")
    else:
        print("Found {} events".format(len(soonish_events)))

for _event in soonish_events:
    toot = False
    if not dry_run:
        user_credentials = get_credentials(_event.type)
        if user_credentials is None:
            continue
        # Login using generated auth
        mastodon = Mastodon(
            client_id='app_credentials',
            api_base_url=user_credentials['url']
        )
        if len(user_credentials['email']) > 0 and len(user_credentials['pass']) > 0:
            toot = True
        else:
            if debug:
                print("Will skip tooting for event type {}".format(_event.type))

    if _event.stage:
        title = "{}: {}".format(_event.category, _event.stage)
    else:
        title = "{}".format(_event.category)
    storyid = _event.tl_id
    event_time = _event.start_time - now
    in_minutes = int(event_time.total_seconds() / 60)
    if in_minutes == 0:
        when = "starts NOW !!"
    elif in_minutes < 0:
        when = "has started {} min ago!".format(abs(in_minutes))
    else:
        when = "begins in {} min!".format(abs(in_minutes))

    if len(_event.links):
        links = _event.links.values().join("\n")

        post = "{} {}\n{}\n\n#{}".format(title, when, links, _event.type)
    else:
        post = "{} {}\n\n#{}".format(title, when, _event.type)

    if debug:
        print(post)

    if toot and not dry_run:
        mastodon.log_in(user_credentials['email'], user_credentials['pass'])
        mastodon.toot(post)
