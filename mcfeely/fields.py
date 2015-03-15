import base64
from django.db import models
try:
    from django.utils.encoding import force_bytes
except:
    pass


class Base64Field(models.TextField):

    def contribute_to_class(self, cls, name):
        if self.db_column is None:
            self.db_column = name
        self.field_name = name + '_base64'
        super(Base64Field, self).contribute_to_class(cls, self.field_name)
        setattr(cls, name, property(self.get_data, self.set_data))

    def get_data(self, obj):
        try:
            content = base64.b64decode(
                force_bytes(
                    getattr(
                        obj,
                        self.field_name)))
            if isinstance(content, bytes):
                return content.decode("utf-8")
            else:
                return content
        except NameError:
            return base64.b64decode(getattr(obj, self.field_name))

    def set_data(self, obj, data):
        try:
            setattr(
                obj,
                self.field_name,
                base64.b64encode(force_bytes(data)))
        except NameError:
            setattr(obj, self.field_name, base64.b64encode(data))
