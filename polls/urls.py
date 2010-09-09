from django.conf.urls.defaults import *
from route import view

urlpatterns = patterns('mysite.polls.views',
    view('', 'index'),
    view('poll=<Poll.pk>/', 'detail'),
    view('poll=<Poll.pk>/results/', 'results'),
    view('poll=<Poll.pk>/vote/', 'vote'),
)

