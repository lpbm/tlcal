from datetime import datetime
from requests import get, codes


class Html:
    """
    """

    uris = {
        "sc2": "http://www.teamliquid.net/calendar/",
        "hrt": "http://www.liquidhearth.com/calendar/",
        "dot": "http://www.liquiddota.com/calendar/",
        "lol": "http://www.liquidlegends.net/calendar/"
    }

    class UriBuilder:
        """
        """
        @staticmethod
        def get_uri(calendar="sc2", by_week=True, by_month=False, date=None):
            if by_week:
                view_by = "week"
            if by_month:
                view_by = "month"

            if date is None:
                date = datetime.now()

            fmt = date.strftime
            return Html.uris[calendar] + "?view=%s&year=%s&month=%s&day=%s" % (view_by, fmt("%Y"), fmt("%m"), fmt("%d"))

    @staticmethod
    def get_calendar(calendar="sc2", by_week=True, by_month=False, date=None, debug=False):
        """
        :return: str
        """

        calendar_uri = Html.UriBuilder.get_uri(calendar, by_week, by_month, date)
        if debug:
            print("Loading calendar from: %s" % calendar_uri)

        tl_response = get(calendar_uri)
        if tl_response.status_code == codes.ok:
            return tl_response.content
        else:
            return ""
