import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup, Tag

from liquid.scraper.html import Html
from model import event


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

    debug = False
    type = ""

    def __init__(self, date=None, debug=False):
        if isinstance(date, datetime):
            self.date = date

        self.events = []
        self.debug = debug

    def load_calendar(self, calendar="sc2", raw_content=""):
        """
        :param calendar: string
        :param raw_content: string
        :return: bool
        """
        self.type = calendar
        if len(raw_content) == 0:
            if self.debug:
                print("Err: no content")
            return False

        soup = BeautifulSoup(raw_content, "html.parser")

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
            start_month = day.month
            start_year = self.date.year
            if start_day < day.day:
                start_month += 1
                if start_month == 13:
                    start_month = 1
                    start_year = self.date.year + 1 
            cur_day = day.replace(day=start_day, month=start_month, year=start_year)

            event_blocks = day_html.find_all("div", class_="ev-block")
            if len(event_blocks) > 0:
                if self.debug:
                    print("\t%s - %d events" % (cur_day.strftime("%d %b"), len(event_blocks)))

                for event_block in event_blocks:
                    if event_block is None:
                        continue

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
                        _event.cal_id = int(title_div.span["data-event-id"])

                    stage_block = event_block.find("div", class_="ev-stage")
                    if stage_block and len(stage_block.contents) > 0:
                        _event.stage = stage_block.contents[0]

                    body_block = event_block.find("div", class_="ev-match")
                    if body_block:
                        # look for times for the matches
                        times = body_block.find("span", class_="ev-timer")
                        if times:
                            for time in times:
                                if isinstance(time, Tag):
                                    time.decompose()

                        _event.content = body_block.get_text().strip("\n")
                        self.estimate_duration(_event)

                    if _event.is_valid():
                        _events.append(_event)

                if len(_events) > 0:
                    self.events = _events
        if self.debug:
            end_day = day + timedelta(days=no_days)
            print("__________________________________________________")
            print("Period: %29s - %s" % (day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")))
            print("Total events: %14d" % len(self.events))
            print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")

        return True

    @staticmethod
    def estimate_duration(event):
        """
        I need to fix this, the match duration depends on the event type
        return:timedelta
        """
        match_duration = 40
        if len(event.content) > 0:
            m = re.findall(' vs ', event.content)
            if len(m) > 0:
                event.match_count = len(m)

        duration = timedelta(minutes=event.match_count * match_duration)
        event.end_time = event.start_time + duration
        return duration

    def load_event_info(self, event_content, calendar="sc2"):
        """
        :cal_id: int
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
            if not isinstance(link_block, Tag):
                continue

            name = link_block.div.text
            link = link_block.find("a")
            href = link["href"]

            if "forum" in href:
                href = Html.UriBuilder.get_uri(calendar) + href

            links[name] = href

        return links
