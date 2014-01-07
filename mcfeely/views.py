from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from mcfeely.forms import UnsubscribeForm


class UnsubscribeView(CreateView):
    form_class = UnsubscribeForm
    template_name = 'unsubscribe.html'


class SuccessView(TemplateView):
    template_name = 'success.html'
