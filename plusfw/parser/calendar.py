import re
import copy
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
            if event_tag is None:
                return 0

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
            event_blocks = day_html.find_all("div", class_="cal_event")

            if event_blocks is None or len(event_blocks) == 0:
                continue

            for event_block in event_blocks:
                if event_block:
                    event_id = None
                    event_type = None
                    event_start_time = None
                    event_stage = ''
                    event_category = None
                    event_links = {}
                    event_match_count = 1

                    category_div = event_block.find("div", class_="cal_e_title")

                    if category_div is None:
                        continue

                    subtitle_div = event_block.find("div", class_="cal_e_subtitle")
                    matches_container_div = event_block.find("div", class_="cal_matches")

                    event_type = Calendar.EventMapper.get_event_type(event_block.find('div', class_='cal_cat'))

                    start_block = event_block.findChild("div", class_="cal_time")
                    if start_block:
                        start_time_str = start_block.contents[0]

                    event_start_time = datetime.strptime(
                        "%s %s" % (cur_day.strftime("%Y-%m-%d"), start_time_str), "%Y-%m-%d %H:%M"
                    )

                    title_div = category_div.find("div", class_="cal_title")
                    if title_div:
                        event_category = title_div.a.text
                        event_links['event'] = Html.UriBuilder.get_uri(event_type) + title_div.a.get('href')
                        m = re.search('quake/post/(\d+)/.*', event_links['event'])
                        if m:
                            key = int(m.group(1))
                            event_id = key

                    if subtitle_div:
                        event_stage = subtitle_div.text

                    if matches_container_div:
                        sub_event_id = None
                        sub_event_links = {}

                        matches_div = matches_container_div.find_all("div", class_="cal_match")
                        for match_div in matches_div:
                            if match_div is None:
                                continue

                            sub_event_type = Calendar.EventMapper.get_event_type(
                                event_block.find('div', class_='cal_cat')
                            )

                            a_div = match_div.find('a')
                            if a_div:
                                sub_event_content = a_div.text
                                sub_event_links['event'] = Html.UriBuilder.get_uri(event_type) + a_div.get('href')
                                m = re.search('quake/post/(\d+)/.*', sub_event_links['event'])
                                if m:
                                    key = int(m.group(1))
                                    sub_event_id = key

                            start_block = match_div.findChild("div", class_="cal_time")
                            if start_block:
                                start_time_str = start_block.contents[0]

                            sub_event_start_time = datetime.strptime(
                                "%s %s" % (cur_day.strftime("%Y-%m-%d"), start_time_str), "%Y-%m-%d %H:%M"
                            )
                            if sub_event_type and sub_event_start_time and event_category:
                                event_match_count += 1
                                sub_event = event.Event()
                                sub_event.tl_id = sub_event_id
                                sub_event.category = event_category
                                sub_event.stage = event_stage
                                sub_event.content = sub_event_content
                                sub_event.start_time = sub_event_start_time
                                sub_event.links = sub_event_links
                                sub_event.type = sub_event_type
                                self.estimate_duration(sub_event)
                                _events.append(sub_event)

                    if event_id and event_type and event_start_time and event_category:
                        _event = event.Event()
                        _event.tl_id = event_id
                        _event.match_count = event_match_count
                        _event.category = event_category
                        _event.stage = event_stage
                        _event.start_time = event_start_time
                        _event.type = event_type
                        _event.links = event_links
                        self.estimate_duration(_event)
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
        match_duration = 90
        duration = timedelta(minutes=1 * match_duration)
        event.end_time = event.start_time + duration
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
