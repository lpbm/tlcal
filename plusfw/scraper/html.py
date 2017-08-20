from datetime import datetime
from requests import get, post, codes, exceptions
import json


class Html:
    """
    """

    base_uris = {
        # +->
        "pfw": "https://www.plusforward.net",
        "qlv": "https://www.plusforward.net",
        "qiv": "https://www.plusforward.net",
        "qiii": "https://www.plusforward.net",
        "qii": "https://www.plusforward.net",
        "qw": "https://www.plusforward.net",
        "dbt": "https://www.plusforward.net",
        "doom": "https://www.plusforward.net",
        "rfl": "https://www.plusforward.net",
        "ovw": "https://www.plusforward.net",
        "gg": "https://www.plusforward.net",
        "ut": "https://www.plusforward.net",
        "wsw": "https://www.plusforward.net",
        "dbmb": "https://www.plusforward.net",
        "xnt": "https://www.plusforward.net",
        "qch": "https://www.plusforward.net",
        "cpma": "https://www.plusforward.net",
    }

    calendar_path = {
        # +->
        "pfw": "/calendar/",
        "qlv": "/calendar/",
        "qiv": "/calendar/",
        "qiii": "/calendar/",
        "qii": "/calendar/",
        "qw": "/calendar/",
        "dbt": "/calendar/",
        "doom": "/calendar/",
        "rfl": "/calendar/",
        "ovw": "/calendar/",
        "gg": "/calendar/",
        "ut": "/calendar/",
        "wsw": "/calendar/",
        "dbmb": "/calendar/",
        "xnt": "/calendar/",
        "qch": "/calendar/",
        "cpma": "/calendar/",
    }

    event_path = {
        # +->
        "pwf": "/calendar/manage/",
        "qlv": "/calendar/manage/",
        "qiv": "/calendar/manage/",
        "qiii": "/calendar/manage/",
        "qii": "/calendar/manage/",
        "qw": "/calendar/manage/",
        "dbt": "/calendar/manage/",
        "doom": "/calendar/manage/",
        "rfl": "/calendar/manage/",
        "ovw": "/calendar/manage/",
        "gg": "/calendar/manage/",
        "ut": "/calendar/manage/",
        "wsw": "/calendar/manage/",
        "dbmb": "/calendar/manage/",
        "xnt": "/calendar/manage/",
        "qch": "/calendar/manage/",
        "cpma": "/calendar/manage/",
    }

    calendar_type = {
        # +->
        "unk": 0,
        "qlv": 3,
        "qiv": 4,
        "qiii": 5,
        "qii": 6,
        "qw": 7,
        "dbt": 8,
        "doom": 9,
        "rfl": 10,
        "ovw": 13,
        "gg": 14,
        "ut": 15,
        "wsw": 16,
        "dbmb": 17,
        "xnt": 18,
        "qch": 20,
        "cpma": 21,
        "pfw": 999,
    }

    class UriBuilder:
        """
        """

        @staticmethod
        def get_uri(calendar="pfw"):
            return Html.base_uris[calendar]

        @staticmethod
        def get_calendar_uri(calendar="pfw", by_week=True, date=None):
            if by_week:
                view_by = "week"
            else:
                view_by = "month"

            if date is None:
                date = datetime.now()

            fmt = date.strftime
            url = Html.base_uris[calendar] + Html.calendar_path[calendar] + \
                '?view=%s&year=%s&month=%s&day=%s&current=0' % (view_by, fmt("%Y"), fmt("%m"), fmt("%d"))

            return url

        @staticmethod
        def get_event_uri(calendar="pfw"):
            return Html.base_uris[calendar] + Html.event_path[calendar]

    @staticmethod
    def get_calendar(calendar="+fw", by_week=True, date=None, debug=False):
        """
        :param debug:
        :param date:
        :param by_week:
        :param calendar:
        :return: str
        """

        calendar_uri = Html.UriBuilder.get_calendar_uri(calendar, by_week, date)
        if debug:
            print("Loading calendar from: %s" % calendar_uri)

        post_data = {
            "cat": str(Html.calendar_type[calendar])
        }
        try:
            if calendar != "pfw":
                tl_response = post(calendar_uri, post_data)
            else:
                tl_response = get(calendar_uri)
        except exceptions.ConnectionError as h:
            return "" % h

        if tl_response.status_code == codes.ok:
            return tl_response.content
        else:
            return ""

    @staticmethod
    def get_event(calendar="qch", event_id=None, debug=True):
        if event_id is None:
            return ""

        if debug:
            print(event_id, end=" ", flush=True)

        html = ""
        event_uri = Html.UriBuilder.get_event_uri(calendar)

        post_data = {
            "action": "view-event-popup",
            "event_id": event_id
        }

        tl_response = post(event_uri, post_data)
        if tl_response.status_code == codes.ok and tl_response.headers.get('content-type') == "application/json":
            decoded_response = json.loads(tl_response.content.decode(encoding="UTF-8"))
            if "html" in decoded_response:
                html = decoded_response["html"]

        return html
