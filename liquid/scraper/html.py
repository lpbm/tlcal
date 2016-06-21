from datetime import datetime
from requests import get, post, codes, exceptions
import json


class Html:
    """
    """

    base_uris = {
        "sc2": "https://www.teamliquid.net",
        "brw": "https://www.teamliquid.net",
        "csg": "https://www.teamliquid.net",
        "hot": "https://www.teamliquid.net",
        "sma": "https://www.teamliquid.net",
        "hrt": "https://www.liquidhearth.com",
        "dot": "https://www.liquiddota.com",
        "lol": "https://www.liquidlegends.net"
    }

    calendar_path = {
        "sc2": "/calendar/",
        "brw": "/calendar/",
        "csg": "/calendar/",
        "hot": "/calendar/",
        "sma": "/calendar/",
        "hrt": "/calendar/",
        "dot": "/calendar/",
        "lol": "/calendar/"
    }

    event_path = {
        "sc2": "/calendar/manage",
        "brw": "/calendar/manage",
        "csg": "/calendar/manage",
        "hot": "/calendar/manage",
        "sma": "/calendar/manage",
        "hrt": "/calendar/manage",
        "dot": "/calendar/manage",
        "lol": "/calendar/manage"
    }

    calendar_type = {
        "sc2": 1,
        "brw": 2,
        "csg": 3,
        "hot": 4,
        "sma": 5
    }

    class UriBuilder:
        """
        """
        @staticmethod
        def get_uri(calendar="sc2"):
            return Html.base_uris[calendar]

        @staticmethod
        def get_calendar_uri(calendar="sc2", by_week=True, by_month=False, date=None):
            if by_week:
                view_by = "week"
            if by_month:
                view_by = "month"

            if date is None:
                date = datetime.now()

            fmt = date.strftime
            url = Html.base_uris[calendar] + Html.calendar_path[calendar] + "?view=%s&year=%s&month=%s&day=%s" \
                                                                            % (view_by, fmt("%Y"), fmt("%m"), fmt("%d"))

            if calendar in Html.calendar_type.keys():
                url += "&game=" + str(Html.calendar_type[calendar])

            return url

        @staticmethod
        def get_event_uri(calendar="sc2"):
            return Html.base_uris[calendar] + Html.event_path[calendar]

    @staticmethod
    def get_calendar(calendar="sc2", by_week=True, by_month=False, date=None, debug=False):
        """
        :param debug:
        :param date:
        :param by_month:
        :param by_week:
        :param calendar:
        :return: str
        """

        calendar_uri = Html.UriBuilder.get_calendar_uri(calendar, by_week, by_month, date)
        if debug:
            print("Loading calendar from: %s" % calendar_uri)

        try:
            tl_response = get(calendar_uri)
        except exceptions.ConnectionError as h:
            return ""

        if tl_response.status_code == codes.ok:
            return tl_response.content
        else:
            return ""

    @staticmethod
    def get_event(calendar="sc2", event_id=None, debug=True):
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
