from django.views.generic.edit import CreateView
from mcfeely.forms import UnsubscribeForm

class UnsubscribeView(CreateView):
    form_class = UnsubscribeForm
    template_name = 'unsubscribe.html'


