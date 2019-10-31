import plusfw

from datetime import datetime
from requests import get, post, codes, exceptions
import json


class Html:
    """
    """

    base_uris = {
        plusfw.LABEL_PFW: "https://www.plusforward.net",
        plusfw.LABEL_QLIVE: "https://www.plusforward.net",
        plusfw.LABEL_QIV: "https://www.plusforward.net",
        plusfw.LABEL_QIII: "https://www.plusforward.net",
        plusfw.LABEL_QII: "https://www.plusforward.net",
        plusfw.LABEL_QWORLD: "https://www.plusforward.net",
        plusfw.LABEL_DIABOT: "https://www.plusforward.net",
        plusfw.LABEL_DOOM: "https://www.plusforward.net",
        plusfw.LABEL_REFLEX: "https://www.plusforward.net",
        plusfw.LABEL_OWATCH: "https://www.plusforward.net",
        plusfw.LABEL_GG: "https://www.plusforward.net",
        plusfw.LABEL_UNREAL: "https://www.plusforward.net",
        plusfw.LABEL_WARSOW: "https://www.plusforward.net",
        plusfw.LABEL_DBMB: "https://www.plusforward.net",
        plusfw.LABEL_XONOT: "https://www.plusforward.net",
        plusfw.LABEL_QCHAMP: "https://www.plusforward.net",
        plusfw.LABEL_QCPMA: "https://www.plusforward.net",
    }

    calendar_path = {
        plusfw.LABEL_PFW: "/calendar/",
        plusfw.LABEL_QLIVE: "/calendar/",
        plusfw.LABEL_QIV: "/calendar/",
        plusfw.LABEL_QIII: "/calendar/",
        plusfw.LABEL_QII: "/calendar/",
        plusfw.LABEL_QWORLD: "/calendar/",
        plusfw.LABEL_DIABOT: "/calendar/",
        plusfw.LABEL_DOOM: "/calendar/",
        plusfw.LABEL_REFLEX: "/calendar/",
        plusfw.LABEL_OWATCH: "/calendar/",
        plusfw.LABEL_GG: "/calendar/",
        plusfw.LABEL_UNREAL: "/calendar/",
        plusfw.LABEL_WARSOW: "/calendar/",
        plusfw.LABEL_DBMB: "/calendar/",
        plusfw.LABEL_XONOT: "/calendar/",
        plusfw.LABEL_QCHAMP: "/calendar/",
        plusfw.LABEL_QCPMA: "/calendar/",
    }

    event_path = {
        plusfw.LABEL_PFW: "/calendar/manage/",
        plusfw.LABEL_QLIVE: "/calendar/manage/",
        plusfw.LABEL_QIV: "/calendar/manage/",
        plusfw.LABEL_QIII: "/calendar/manage/",
        plusfw.LABEL_QII: "/calendar/manage/",
        plusfw.LABEL_QWORLD: "/calendar/manage/",
        plusfw.LABEL_DIABOT: "/calendar/manage/",
        plusfw.LABEL_DOOM: "/calendar/manage/",
        plusfw.LABEL_REFLEX: "/calendar/manage/",
        plusfw.LABEL_OWATCH: "/calendar/manage/",
        plusfw.LABEL_GG: "/calendar/manage/",
        plusfw.LABEL_UNREAL: "/calendar/manage/",
        plusfw.LABEL_WARSOW: "/calendar/manage/",
        plusfw.LABEL_DBMB: "/calendar/manage/",
        plusfw.LABEL_XONOT: "/calendar/manage/",
        plusfw.LABEL_QCHAMP: "/calendar/manage/",
        plusfw.LABEL_QCPMA: "/calendar/manage/",
    }

    calendar_type = {
        plusfw.LABEL_QLIVE: 3,
        plusfw.LABEL_QIV: 4,
        plusfw.LABEL_QIII: 5,
        plusfw.LABEL_QII: 6,
        plusfw.LABEL_QWORLD: 7,
        plusfw.LABEL_DIABOT: 8,
        plusfw.LABEL_DOOM: 9,
        plusfw.LABEL_REFLEX: 10,
        plusfw.LABEL_OWATCH: 13,
        plusfw.LABEL_GG: 14,
        plusfw.LABEL_UNREAL: 15,
        plusfw.LABEL_WARSOW: 16,
        plusfw.LABEL_DBMB: 17,
        plusfw.LABEL_XONOT: 18,
        plusfw.LABEL_QCHAMP: 20,
        plusfw.LABEL_QCPMA: 21,
    }

    class UriBuilder:
        """
        """

        @staticmethod
        def get_uri(calendar=plusfw.LABEL_PFW):
            return Html.base_uris.get(calendar)

        @staticmethod
        def get_calendar_uri(calendar=plusfw.LABEL_PFW, by_week=False, date=None):
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
        def get_event_uri(calendar=plusfw.LABEL_PFW):
            return Html.base_uris[calendar] + Html.event_path[calendar]

    @staticmethod
    def get_calendar(calendar="+fw", by_week=False, date=None, debug=False):
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

        post_data = None
        if calendar in Html.calendar_type:
            post_data = {
                "cat": str(Html.calendar_type[calendar])
            }
        try:
            if post_data:
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
    def get_event(calendar=plusfw.LABEL_QCHAMP, event_id=None, debug=True):
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
