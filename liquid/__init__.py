from datetime import datetime
from liquid.parser.calendar import Calendar
from liquid.scraper.html import Html
from liquid.persist.mongowrapper import MongoWrapper

__author__ = "Marius Orcsik <marius@habarnam.ro>"
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2015 Marius Orcsik"
__license__ = "MIT"

__all__ = ['model', 'parser', 'scraper', 'persist']


def load_from_date(type_="sc2", date=None, persist=None, debug=False):
    """
    :type type_: str
    :type date: datetime
    :type persist: MongoWrapper
    :return:
    """
    # file_prefix = "%s_%s_%s_" % (type_, date.strftime("%Y-%W"), datetime.utcnow().timestamp())
    # file = NamedTemporaryFile("w+b", suffix=".cache.html", prefix=file_prefix, delete=False)
    # file.write()
    # file.close()
    # os.remove(file.name)

    if persist is None:
        return False

    content = Html.get_calendar(type_, by_week=True, date=date, debug=debug)

    _parser = Calendar(content, date=date, debug=debug)

    if _parser.load(type_) and len(_parser.events) > 0:
        if debug:
            print("Loading information for event:", end=" ", flush=True)
        for event in _parser.events:
            event_content = Html.get_event(type_, event.tl_id)
            event.links = _parser.load_event_info(event_content)

        persist.save(_parser.events)
        return True
    else:
        return False
