import re
import time
import pytz

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def only_numbers(s):
    if not s:
        return s
    return re.sub('[^0-9]', '', s)


def only_alphanum(s):
    if not s:
        return s
    return re.sub('[^0-9A-Za-z]', '', s)


def is_only_alpha(s):
    return all(c.isalpha() or c == ' ' for c in s)


def error_str(ex):
    if isinstance(ex, ValidationError):
        return '; '.join(ex.messages)
    else:
        return str(ex)


def to_tz(d, tz):
    if d is None:
        return None
    ptz = pytz.timezone(tz)
    return d.astimezone(ptz) if timezone.is_aware(d) else ptz.localize(d)
