from datetime import datetime
from persist.mongowrapper import MongoWrapper

__author__ = "Marius Orcsik <marius@habarnam.ro>"
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2015 Marius Orcsik"
__license__ = "MIT"

__all__ = ['parser', 'scraper', 'load_from_date']

SC2_LABEL = "sc2"
SCREMASTERED_LABEL = "scrm"
BW_LABEL = "bw"
CSGO_LABEL = "csgo"
HOTS_LABEL = "hots"
SMASH_LABEL = "smash"
HSTONE_LABEL = "hs"
DOTA_LABEL = "dota"
LOL_LABEL = "lol"
TEAMLIQUID_LABEL = "tl"
LABEL_UNKNOWN = "unk"


def load_from_date(type_="sc2", date=None, persist=None, debug=False):
    """
    :type type_: str
    :type date: datetime
    :type persist: MongoWrapper
    :return:
    """
    from liquid.parser.calendar import Calendar
    from liquid.scraper.html import Html
    # file_prefix = "%s_%s_%s_" % (type_, date.strftime("%Y-%W"), datetime.utcnow().timestamp())
    # file = NamedTemporaryFile("w+b", suffix=".cache.html", prefix=file_prefix, delete=False)
    # file.write()
    # file.close()
    # os.remove(file.name)

    if persist is None:
        return False

    raw_content = Html.get_calendar(type_, by_week=True, date=date, debug=debug)

    _parser = Calendar(date=date, debug=debug)
    if _parser.load_calendar(type_, raw_content) and len(_parser.events) > 0:
        return persist.save(_parser.events)
    else:
        return False


def load_event_data(_events, persist=None, debug=False):
    from liquid.parser.calendar import Calendar
    from liquid.scraper.html import Html

    if persist is None:
        return False

    _parser = Calendar(date=None, debug=debug)

    if debug:
        print("Loading events:", end=" ", flush=True)
    for event in _events:
        event_content = Html.get_event(event.type, event.cal_id, debug=debug)
        event.links = _parser.load_event_info(event_content, event.type)

    if debug:
        print()
    return persist.save(_events)
