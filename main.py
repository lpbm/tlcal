from datetime import datetime
from tempfile import NamedTemporaryFile
from liquid.model import event, calday
from liquid.parser import calendar
from liquid.scraper import html
from liquid import debug as _debug

"""
"""

__author__ = "Marius Orcsik <marius@habarnam.ro>"
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2015 Marius Orcsik"
__license__ = "MIT"


# html = get_current_week("hrt")
# parser = WeekParser(html, "hrt")
#
# print(parser.days)
# for _day in parser.days:
#     for _event in _day.events:
#         print(_event.icon)
week = {}
_debug = True
_type = "sc2"
current_date = datetime.now()
print("now: %s" % current_date.strftime("%W"))

file_prefix = "%s_%s_%s_" % (_type, current_date.strftime("%W"), datetime.utcnow().timestamp())
file = NamedTemporaryFile("w+b", suffix=".cache.html", prefix=file_prefix, delete=False)
file.write(
    html.Html.get_calendar(_type, by_week=True, date_=current_date)
)
file.close()

parser = calendar.Calendar(file)
if parser.load(_type):
    _days = parser.days
    print(_days)
exit()

for _type in html.Html.UriBuilder.uris:
    parser = calendar.Calendar(_type, by_week=True)
    week[_type] = parser.days

for cal_days in week:
    for _day in week[cal_days]:
        if isinstance(_day, calday.CalDay):
            for _event in _day.events:
                if isinstance(_event, event.Event):
                    print(_event.category, _event.date_time)

