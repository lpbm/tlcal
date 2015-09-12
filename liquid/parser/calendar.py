from datetime import datetime
import re
from bs4 import BeautifulSoup
from liquid.model import event
from liquid.static import icon


class Calendar:
    """
    A class that parses html from the TL week calendar
    """

    class SC2IconMapper(icon.Icon):
        icon_mappings = {
            0: "unk",
            1: "sc2",
            2: "brw",
            3: "csg",
            4: "hot",
            5: "sma"
        }
        """
        A class to map the icons from TL events
        """
        @staticmethod
        def get_icon_identifier(event_tag):
            key = "0"
            element = event_tag.findChild("span", class_="league-sprite-small")
            if element:
                m = re.search('\d+', element["style"])
                if m:
                    key = int(m.group(0))
            return Calendar.SC2IconMapper.icon_mappings[key]

    raw_content = ""
    debug = False

    def __init__(self, rawContent, date=None, debug=False):
        """
        calendar: str
        file: tempfile.NamedTemporaryFile
        :return:
        """
        if isinstance(date, datetime):
            self.date = date

        self.raw_content = rawContent
        self.events = []
        self.debug = debug

    def load(self, calendar="sc2"):
        """
        :return bool
        """
        if len(self.raw_content) == 0:
            if self.debug:
                print("Err: file-size 0")
            return False

        if self.debug:
            print("processing content")
        soup = BeautifulSoup(self.raw_content, "html.parser")

        days_html_list = soup.find_all("div", class_="ev-feed")
        no_days = len(days_html_list)

        if self.debug:
            print("\tFound %d days" % no_days)

        day = self.date
        for day_html in days_html_list:
            start_day = int(day_html["data-day"])
            cur_day = day.replace(day=start_day)

            event_blocks = day_html.find_all("div", class_="ev-block")
            if len(event_blocks) > 0:
                if self.debug:
                    print("\t\t%s - %d events" % (cur_day.strftime("%Y-%m-%d"), len(event_blocks)))

                _events = []
                for event_block in event_blocks:
                    if event_block:
                        _event = event.Event()
                        if calendar == "sc2":
                            _event.icon = Calendar.SC2IconMapper.get_data(Calendar.SC2IconMapper.get_icon_identifier(event_block))
                        else:
                            _event.icon = icon.Icon.get_data(calendar)

                        start_block = event_block.findChild("span", class_="ev-timer")
                        if start_block:
                            start_time = start_block.contents[0]

                        _event.date_time = datetime.strptime(
                            "%s %s" % (cur_day.strftime("%Y-%m-%d"), start_time), "%Y-%m-%d %H:%M"
                        )

                        title_div = event_block.find("div", class_="ev-ctrl")
                        if title_div:
                            _event.category = title_div.span.contents[0]
                            _event.tl_id = int(title_div.span["data-event-id"])

                        stage_block = event_block.find("div", class_="ev-stage")
                        if stage_block and len(stage_block.contents) > 0:
                            _event.stage = stage_block.contents[0]

                        body_block = event_block.find("div", class_="ev-match")
                        if body_block:
                            _event.content = body_block.prettify()

                        if _event.is_valid():
                            _events.append(_event)

                if len(_events) > 0:
                    self.events = _events
        return True
