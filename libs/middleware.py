from django.utils import timezone

import pytz


class TimezoneMiddleware(object):

    def process_request(self, request):
        try:
            tzname = request.META.get('HTTP_USER_TIMEZONE', None)
            if tzname:
                timezone.activate(pytz.timezone(tzname))
                request.timezone = pytz.timezone(tzname)
            else:
                timezone.deactivate()
        except pytz.UnknownTimeZoneError:
            timezone.deactivate()
            pass
