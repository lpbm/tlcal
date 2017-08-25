import liquid
from datetime import datetime
from requests import get, post, codes, exceptions
import json


class Html:
    """
    """

    base_uris = {
        liquid.SC2_LABEL: "http://www.teamliquid.net",
        liquid.BW_LABEL: "http://www.teamliquid.net",
        liquid.CSGO_LABEL: "http://www.teamliquid.net",
        liquid.HOTS_LABEL: "http://www.teamliquid.net",
        liquid.SMASH_LABEL: "http://www.teamliquid.net",
        liquid.HSTONE_LABEL: "http://www.liquidhearth.com",
        liquid.DOTA_LABEL: "http://www.liquiddota.com",
        liquid.LOL_LABEL: "http://www.liquidlegends.net",
    }

    calendar_path = {
        liquid.SC2_LABEL: "/calendar/",
        liquid.BW_LABEL: "/calendar/",
        liquid.CSGO_LABEL: "/calendar/",
        liquid.HOTS_LABEL: "/calendar/",
        liquid.SMASH_LABEL: "/calendar/",
        liquid.HSTONE_LABEL: "/calendar/",
        liquid.DOTA_LABEL: "/calendar/",
        liquid.LOL_LABEL: "/calendar/",
    }

    event_path = {
        liquid.SC2_LABEL: "/calendar/manage",
        liquid.BW_LABEL: "/calendar/manage",
        liquid.CSGO_LABEL: "/calendar/manage",
        liquid.HOTS_LABEL: "/calendar/manage",
        liquid.SMASH_LABEL: "/calendar/manage",
        liquid.HSTONE_LABEL: "/calendar/manage",
        liquid.DOTA_LABEL: "/calendar/manage",
        liquid.LOL_LABEL: "/calendar/manage",
    }

    calendar_type = {
        liquid.SC2_LABEL: 1,
        liquid.BW_LABEL: 2,
        liquid.CSGO_LABEL: 3,
        liquid.HOTS_LABEL: 4,
        liquid.SMASH_LABEL: 5,
        liquid.TEAMLIQUID_LABEL: 999,
    }

    class UriBuilder:
        """
        """
        @staticmethod
        def get_uri(calendar=liquid.SC2_LABEL):
            return Html.base_uris[calendar]

        @staticmethod
        def get_calendar_uri(calendar=liquid.SC2_LABEL, by_week=True, date=None):
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
        def get_event_uri(calendar=liquid.SC2_LABEL):
            return Html.base_uris[calendar] + Html.event_path[calendar]

    @staticmethod
    def get_calendar(calendar=liquid.SC2_LABEL, by_week=True, date=None, debug=False):
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
    def get_event(calendar=liquid.SC2_LABEL, event_id=None, debug=True):
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
