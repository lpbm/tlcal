from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Tag
from liquid.model import event
from liquid.scraper.html import Html
import re


class Calendar:
    """
    A class that parses html from the TL week calendar
    """

    class EventMapper:
        event_types = {
            0: "unk",
            1: "sc2",
            2: "brw",
            3: "csg",
            4: "hot",
            5: "sma"
        }
        """
        A class get the event type
        """
        @staticmethod
        def get_event_type(event_tag):
            key = "0"
            element = event_tag.findChild("span", class_="league-sprite-small")
            if element:
                m = re.search('\d+', element["style"])
                if m:
                    key = int(m.group(0))
            return Calendar.EventMapper.event_types[key]

    raw_content = ""
    debug = False
    type = ""

    def __init__(self, raw_content, date=None, debug=False):
        if isinstance(date, datetime):
            self.date = date

        self.raw_content = raw_content
        self.events = []
        self.debug = debug

    def load(self, calendar="sc2"):
        """
        :return bool
        """
        self.type = calendar
        if len(self.raw_content) == 0:
            if self.debug:
                print("Err: no content")
            return False

        soup = BeautifulSoup(self.raw_content, "html.parser")

        days_html_list = soup.find_all("div", class_="ev-feed")
        no_days = len(days_html_list)

        day = datetime(
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
        )
        _events = []
        for day_html in days_html_list:
            start_day = int(day_html["data-day"])
            cur_day = day.replace(day=start_day)

            event_blocks = day_html.find_all("div", class_="ev-block")
            if len(event_blocks) > 0:
                # if self.debug:
                #     print("\t%s - %d events" % (cur_day.strftime("%d %b"), len(event_blocks)))

                for event_block in event_blocks:
                    if event_block:
                        _event = event.Event()
                        if calendar == "sc2":
                            _event.type = Calendar.EventMapper.get_event_type(event_block)
                        else:
                            _event.type = calendar

                        start_block = event_block.findChild("span", class_="ev-timer")
                        if start_block:
                            start_time = start_block.contents[0]

                        _event.start_time = datetime.strptime(
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
                            # look for times for the matches
                            times = body_block.find("span", class_="ev-timer")
                            if times is not None:
                                for time in times:
                                    if isinstance(time, Tag):
                                        time.decompose()

                            _event.content = body_block.get_text().strip("\n")
                            _event.estimate_duration()

                        if _event.is_valid():
                            _events.append(_event)

                if len(_events) > 0:
                    self.events = _events
        if self.debug:
            end_day = day + timedelta(days=no_days)
            print("Period: %s - %s" % (day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")))
            print("Total events: %d" % len(self.events))

        return True

    def load_event_info(self, event_content):
        """
        :tl_id: int
        :return:
        """
        if len(event_content) == 0:
            if self.debug:
                print("Err: no content")
            return False
        links = {}

        soup = BeautifulSoup(event_content, "html.parser")
        link_blocks = soup.find("div", class_="evc-link")

        for link_block in link_blocks:
            if isinstance(link_block, Tag):
                name = link_block.div.text
                link = link_block.find("a")
                href = link["href"]

                if "forum" in href:
                    href = Html.UriBuilder.get_uri(self.type) + href

                links[name] = href

        return links
