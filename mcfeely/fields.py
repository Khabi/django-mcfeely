import base64
from django.db import models
try:
    from django.utils.encoding import force_bytes
except:
    pass
from django.utils.encoding import smart_bytes, smart_text

class Base64Field(models.TextField):

    def to_python(self, value):
        if value is None:
            return None
        return base64.b64decode(smart_bytes(value))

    def get_prep_value(self, value):
        if value is None:
            return None
        return smart_text(base64.b64encode(smart_bytes(value)))

