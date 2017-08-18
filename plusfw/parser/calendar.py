import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup, Tag

from plusfw.scraper.html import Html
from model import event


class Calendar:
    """
    A class that parses html from the plusforward week calendar
    """

    class EventMapper:
        event_types = {
            0: "unk",
            3: "qlv",
            4: "qiv",
            5: "q3",
            6: "qii",
            7: "qw",
            8: "dbt",
            9: "doom",
            10: "rfl",
            13: "ovw",
            14: "gg",
            15: "ut",
            16: "wsw",
            17: "dbmb",
            18: "xnt",
            20: "qch",
            21: "cpma",
        }
        """
        A class get the event type
        """
        @staticmethod
        def get_event_type(event_tag):
            key = 0
            element = event_tag.findChild("i", class_="pfcat")
            if element:
                m = re.search('\d+', element["class"][1])
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

    def load_calendar(self, calendar="qch", raw_content=""):
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

        days_html_list = soup.find_all("td", class_="cal_day")
        no_days = len(days_html_list)

        day = datetime(
            year=self.date.year,
            month=self.date.month,
            day=self.date.day,
        )
        _events = []
        for day_html in days_html_list:
            start_month = day.month
            start_year = self.date.year

            date_div = day_html.find("div", class_="cal_date").text
            try:
                start_day = datetime.strptime(date_div, "%A%B %d").day
            except ValueError:
                start_day = datetime.strptime(date_div, "%A%d").day

            if start_day < day.day:
                start_month += 1
                if start_month == 13:
                    start_month = 1
                    start_year = self.date.year + 1
            cur_day = day.replace(day=start_day, month=start_month, year=start_year)
            event_blocks = day_html.find("div", class_="cal_event")

            if event_blocks is None or len(event_blocks) == 0:
                continue

            for event_block in event_blocks:
                if event_block:
                    _event = event.Event()
                    _event.type = Calendar.EventMapper.get_event_type(event_block.find('div', class_='cal_cat'))

                    start_block = event_block.findChild("div", class_="cal_time")
                    if start_block:
                        start_time = start_block.contents[0]

                    _event.start_time = datetime.strptime(
                        "%s %s" % (cur_day.strftime("%Y-%m-%d"), start_time), "%Y-%m-%d %H:%M"
                    )

                    title_div = event_block.find("div", class_="cal_title")
                    if title_div:
                        _event.category = title_div.a.text
                        _event.links['event'] = Html.UriBuilder.get_uri(_event.type) + title_div.a.get('href')
                        m = re.search('quake/post/(\d+)/.*', title_div.a.get('href'))
                        if m:
                            key = int(m.group(1))
                        _event.tl_id = key

                    body_block = event_block.find("div", class_="ev-match")
                    if body_block:
                        # look for times for the matches
                        times = body_block.find("div", class_="cal_time")
                        if times is not None:
                            for time in times:
                                if isinstance(time, Tag):
                                    time.decompose()

                        self.estimate_duration(_event)

                    # _event.category = "q"
                    # _event.stage = "q"
                    if _event.is_valid():
                        _events.append(_event)

                if len(_events) > 0:
                    self.events = _events

        if self.debug:
            end_day = day + timedelta(days=no_days)
            print("Period: %s - %s" % (day.strftime("%Y-%m-%d"), end_day.strftime("%Y-%m-%d")))
            print("Total events: %d" % len(self.events))

        return True

    @staticmethod
    def estimate_duration(event):
        """
        I need to fix this, the match duration depends on the event type
        return:timedelta
        """
        match_duration = 90
        event.end_time = event.start_time + match_duration
        return match_duration

    def load_event_info(self, event_content, calendar="qch"):
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
                    href = Html.UriBuilder.get_uri(calendar) + href

                links[name] = href

        return links
