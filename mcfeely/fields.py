from __future__ import unicode_literals
import base64
from django.db import models
try:
    from django.utils.encoding import force_bytes
except:
    pass
from django.utils.encoding import smart_bytes, smart_text
from django.utils.encoding import DjangoUnicodeDecodeError



class Base64Field(models.TextField):

    def to_python(self, value):
        if value is None:
            return None

        decoded = base64.b64decode(value)
        return smart_text(decoded)

    def get_prep_value(self, value):
        if value is None:
            return None
        value = smart_text(base64.b64encode(smart_bytes(value)))
        return self.to_python(value)


