import datetime
from datetime import timedelta
from string import Template

import tzlocal


def get_datetime_string(timestamp_utc: float, date_format: str) -> str:
    local_timezone = tzlocal.get_localzone()
    date_datetime = datetime.datetime.fromtimestamp(timestamp_utc, tz=local_timezone)
    return date_datetime.strftime(date_format)


def get_local_offset_delta() -> timedelta:
    local_timezone = tzlocal.get_localzone()
    now = datetime.datetime.now(tz=local_timezone)
    utc_offset = now.utcoffset()
    if utc_offset is None:
        raise Exception("Could not determine local UTC offset")
    return utc_offset


class _DeltaTemplate(Template):
    delimiter = "%"


def string_format_time_delta(td: timedelta, date_format: str):
    # based on a SO answer by Jens: https://stackoverflow.com/a/49226644

    # Get the timedelta’s sign and absolute number of seconds.
    sign = "-" if td.days < 0 else "+"
    secs = abs(td).total_seconds()

    # Break the seconds into more readable quantities.
    days, rem = divmod(secs, 86400)  # Seconds per day: 24 * 60 * 60
    hours, rem = divmod(rem, 3600)  # Seconds per hour: 60 * 60
    mins, secs = divmod(rem, 60)

    # Format (as per above answers) and return the result string.
    t = _DeltaTemplate(date_format)
    return t.substitute(
        s=sign,
        D="{:d}".format(int(days)),
        H="{:02d}".format(int(hours)),
        M="{:02d}".format(int(mins)),
        S="{:02d}".format(int(secs)),
    )
