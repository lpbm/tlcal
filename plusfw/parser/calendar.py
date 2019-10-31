import re

from datetime import datetime, timedelta

from bs4 import BeautifulSoup, Tag

import plusfw
from plusfw.scraper.html import Html
from model import event


class Calendar:
    """
    A class that parses html from the plusforward week calendar
    """

    class EventMapper:
        event_types = {
            0: plusfw.LABEL_UNKNOWN,
            3: plusfw.LABEL_QLIVE,
            4: plusfw.LABEL_QIV,
            5: plusfw.LABEL_QIII,
            6: plusfw.LABEL_QII,
            7: plusfw.LABEL_QWORLD,
            8: plusfw.LABEL_DIABOT,
            9: plusfw.LABEL_DOOM,
            10: plusfw.LABEL_REFLEX,
            13: plusfw.LABEL_OWATCH,
            14: plusfw.LABEL_GG,
            15: plusfw.LABEL_UNREAL,
            16: plusfw.LABEL_WARSOW,
            17: plusfw.LABEL_DBMB,
            18: plusfw.LABEL_XONOT,
            20: plusfw.LABEL_QCHAMP,
            21: plusfw.LABEL_QCPMA,
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
            return Calendar.EventMapper.event_types.get(key)

    debug = False
    type = ""

    def __init__(self, date=None, debug=False):
        if isinstance(date, datetime):
            self.date = date

        self.events = []
        self.debug = debug

    def load_calendar(self, calendar=plusfw.LABEL_QCHAMP, raw_content=""):
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
            try: 
                cur_day = day.replace(day=start_day, month=start_month, year=start_year)
            except ValueError as e:
                print(e, "start_day {} - cur_day {}".format(start_day, cur_day)) 
            event_blocks = day_html.find_all("div", class_="cal_event")

            if event_blocks is None or len(event_blocks) == 0:
                continue
            else:
                if self.debug:
                    print("\t%s - %d events" % (cur_day.strftime("%d %b"), len(event_blocks)))

            for event_block in event_blocks:
                if event_block is None:
                    continue

                event_id = None
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
                if title_div and title_div.a is not None:
                    event_category = title_div.a.text
                    uri = Html.UriBuilder.get_uri(event_type)
                    if uri is not None:
                        event_links['event'] = uri + title_div.a.get('href')
                        m = re.search('quake/post/(\d+)/.*', event_links['event'])
                        if m:
                            key = int(m.group(1))
                            event_id = key

                if subtitle_div:
                    event_stage = subtitle_div.text

                if matches_container_div:
                    matches_div = matches_container_div.find_all("div", class_="cal_match")
                    for match_div in matches_div:
                        if match_div is None:
                            continue

                        sub_event_id = None
                        sub_event_type = None
                        sub_event_start_time = None
                        sub_event_links = {}

                        cat_div = event_block.find('div', class_='cal_cat')
                        if cat_div:
                            sub_event_type = Calendar.EventMapper.get_event_type(cat_div)

                        a_div = match_div.find('a')
                        if a_div:
                            sub_event_content = a_div.text
                            sub_event_links['event'] = Html.UriBuilder.get_uri(event_type) + a_div.get('href')
                            m = re.search('quake/post/(\d+)/.*', sub_event_links['event'])
                            if m:
                                key = int(m.group(1))
                                sub_event_id = key

                            time_div = match_div.findChild("div", class_="cal_time")
                            if time_div:
                                start_time_str = time_div.contents[0]
                                sub_event_start_time = datetime.strptime(
                                    "%s %s" % (cur_day.strftime("%Y-%m-%d"), start_time_str), "%Y-%m-%d %H:%M"
                                )

                            if sub_event_type and sub_event_start_time and event_category:
                                event_match_count += 1
                                sub_event = event.Event()
                                sub_event.cal_id = sub_event_id
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
                    _event.cal_id = event_id
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
    def estimate_duration(_event):
        """
        I need to fix this, the match duration depends on the event type
        return:timedelta
        :type _event: event.Event
        """
        match_duration = 30
        buffer_duration = 15
        duration = timedelta(minutes=(_event.match_count * (match_duration + buffer_duration) - buffer_duration))
        _event.end_time = _event.start_time + duration
        return match_duration

    def load_event_info(self, event_content, calendar=plusfw.LABEL_QCHAMP):
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
            if isinstance(link_block, Tag):
                name = link_block.div.text
                link = link_block.find("a")
                href = link["href"]

                if "forum" in href:
                    href = Html.UriBuilder.get_uri(calendar) + href

                links[name] = href

        return links
