from django.conf.urls import patterns, url
from mcfeely.views import UnsubscribeView

urlpatterns = patterns('mcfeely.views',
                       url(r'^unsubscribe/$',
                           UnsubscribeView.as_view(success_url='/unsubscribe/'), name='unsubscribe', )
                       )
