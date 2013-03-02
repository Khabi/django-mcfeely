from django.forms import ModelForm
from django import forms
from mcfeely.models import Unsubscribe, Queue

class UnsubscribeForm(ModelForm):
    class Meta:
        model = Unsubscribe

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(UnsubscribeForm, self).__init__(*args, **kwargs)
        self.fields['queue']=forms.ModelChoiceField(
            queryset=Queue.objects.filter(display_to_user=True),
            required=False,
            empty_label="All Mailings")

