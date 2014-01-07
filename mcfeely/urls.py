try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

try:
    from django.core.urlresolvers import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse
    from django.utils.functional import lazy
    reverse_lazy = lambda *args, **kwargs: lazy(reverse, str)(*args, **kwargs)
from mcfeely.views import UnsubscribeView
from mcfeely.views import SuccessView

urlpatterns = patterns('mcfeely.views',
                       url(r'^success/$',
                           SuccessView.as_view(), name='success'),
                       url(r'^unsubscribe/$',
                           UnsubscribeView.as_view(
                           success_url=reverse_lazy(
                           'success')), name='unsubscribe', )
                       )
