from django.conf.urls.defaults import *
from mcfeely.views import UnsubscribeView

urlpatterns = patterns('mcfeely.views',
    url(r'^unsubscribe/$', UnsubscribeView.as_view(), name='unsubscribe')
)
