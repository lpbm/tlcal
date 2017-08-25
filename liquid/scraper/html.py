import liquid
from datetime import datetime
from requests import get, post, codes, exceptions
import json


class Html:
    """
    """

    base_uris = {
        liquid.LABEL_TEAMLIQUID: "http://www.teamliquid.net",
        liquid.LABEL_SC2: "http://www.teamliquid.net",
        liquid.LABEL_BW: "http://www.teamliquid.net",
        liquid.LABEL_CSGO: "http://www.teamliquid.net",
        liquid.LABEL_HOTS: "http://www.teamliquid.net",
        liquid.LABEL_SMASH: "http://www.teamliquid.net",
        liquid.LABEL_HSTONE: "http://www.liquidhearth.com",
        liquid.LABEL_DOTA: "http://www.liquiddota.com",
        liquid.LABEL_LOL: "http://www.liquidlegends.net",
    }

    calendar_path = {
        liquid.LABEL_TEAMLIQUID: "/calendar/",
        liquid.LABEL_SC2: "/calendar/",
        liquid.LABEL_BW: "/calendar/",
        liquid.LABEL_CSGO: "/calendar/",
        liquid.LABEL_HOTS: "/calendar/",
        liquid.LABEL_SMASH: "/calendar/",
        liquid.LABEL_HSTONE: "/calendar/",
        liquid.LABEL_DOTA: "/calendar/",
        liquid.LABEL_LOL: "/calendar/",
    }

    event_path = {
        liquid.LABEL_TEAMLIQUID: "/calendar/manage",
        liquid.LABEL_SC2: "/calendar/manage",
        liquid.LABEL_BW: "/calendar/manage",
        liquid.LABEL_CSGO: "/calendar/manage",
        liquid.LABEL_HOTS: "/calendar/manage",
        liquid.LABEL_SMASH: "/calendar/manage",
        liquid.LABEL_HSTONE: "/calendar/manage",
        liquid.LABEL_DOTA: "/calendar/manage",
        liquid.LABEL_LOL: "/calendar/manage",
    }

    calendar_type = {
        liquid.LABEL_SC2: 1,
        liquid.LABEL_BW: 2,
        liquid.LABEL_CSGO: 3,
        liquid.LABEL_HOTS: 4,
        liquid.LABEL_SMASH: 5,
    }

    class UriBuilder:
        """
        """
        @staticmethod
        def get_uri(calendar=liquid.LABEL_SC2):
            return Html.base_uris[calendar]

        @staticmethod
        def get_calendar_uri(calendar=liquid.LABEL_SC2, by_week=True, date=None):
            if by_week:
                view_by = "week"
            else:
                view_by = "month"

            if date is None:
                date = datetime.now()

            fmt = date.strftime
            url = Html.base_uris[calendar] + Html.calendar_path[calendar] + \
                "?view=%s&year=%s&month=%s&day=%s" % (view_by, fmt("%Y"), fmt("%m"), fmt("%d"))

            if calendar in Html.calendar_type.keys():
                url += "&game=" + str(Html.calendar_type[calendar])

            return url

        @staticmethod
        def get_event_uri(calendar=liquid.LABEL_SC2):
            return Html.base_uris[calendar] + Html.event_path[calendar]

    @staticmethod
    def get_calendar(calendar=liquid.LABEL_SC2, by_week=True, date=None, debug=False):
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

        try:
            tl_response = get(calendar_uri)
        except exceptions.ConnectionError as h:
            return "" % h

        if tl_response.status_code == codes.ok:
            return tl_response.content
        else:
            return ""

    @staticmethod
    def get_event(calendar=liquid.LABEL_SC2, event_id=None, debug=True):
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
