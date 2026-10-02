from django.conf import settings
from middlewares.exception_request import _CURRENT_REQUEST as _current_request

import logging, os, traceback


class ErrorContextFilter(logging.Filter):
    def filter(self, record):
        """
            Adds user email, business code, and error location to log records.
            If the user is not authenticated, sets user_email to 'anonymous' and business_code to '-'.
        """
        user = getattr(_current_request.get(), "user", None)
        authed = bool(user and user.is_authenticated)

        record.user_email = user.email if authed else "anonymous" #type: ignore
        record.business_code = self._business_code(user) if authed else "-"
        record.error_loc = self._location(record)
        return True

    @staticmethod
    def _business_code(user):
        """
            Attempts to retrieve the business code for the given user.
            Returns "no-business" if the user has no associated business,
            and "unavailable" if an error occurs during retrieval.
        """
        try:
            business = getattr(user, "my_business", None)
            return business.code if business else "no-business"
        except Exception:
            return "unavailable"

    @staticmethod
    def _location(record):
        """
            Extracts the file name, line number, and function name from the traceback
            of the log record's exception info. If no exception info is available,
            returns "-".
        """
        if not record.exc_info or not record.exc_info[2]:
            return "-"
        frames = traceback.extract_tb(record.exc_info[2])
        base = str(settings.BASE_DIR)
        own = [
            f for f in frames
            if f.filename.startswith(base) and "site-packages" not in f.filename
        ]
        frame = (own or frames)[-1]
        return f"{os.path.relpath(frame.filename, base)}:{frame.lineno} in {frame.name}"
    