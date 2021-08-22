import re

from django.core.exceptions import ValidationError


def validate_field(value):
    """ Field validator to validate the content of letters only """
    s = re.compile('^[a-zA-Z]+$')
    if not bool(s.match(value)):
        raise ValidationError('%(value)s should be contain letters!', params={'value': value})
