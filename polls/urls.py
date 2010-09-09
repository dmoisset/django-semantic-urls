from django.conf.urls.defaults import *
from route import view

urlpatterns = patterns('mysite.polls.views',
    view('', 'index'),
    view('<poll>=polls.Poll.pk/', 'detail'),
    view('<poll>=polls.Poll.pk/results/', 'results'),
    view('<poll>=polls.Poll.pk/vote/', 'vote'),
    view('search/[search_results]=polls.Poll.question__icontains/', 'search'),
    view('usearch/[search_results]=auth.USER.username__icontains/', 'usearch'),
)

