from django.conf.urls.defaults import *
from route import view

urlpatterns = patterns('mysite.polls.views',
    view('', 'index'),
    view('poll_id:Poll.pk/', 'detail'),
    view('poll_id:Poll.pk/results/$', 'results'),
    view('poll_id:Poll.pk/vote/$', 'vote'),
)

