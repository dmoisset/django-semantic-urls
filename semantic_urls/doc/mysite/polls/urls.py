from django.conf.urls.defaults import *
from route import smarturl 

urlpatterns = patterns('mysite.polls.views',
    smarturl('', 'index'),
    smarturl('<poll>=polls.Poll.pk/', 'detail'),
    smarturl('<poll>=polls.Poll.pk/results/', 'results'),
    smarturl('<poll>=polls.Poll.pk/vote/', 'vote'),
    smarturl('search/[search_results]=polls.Poll.question__icontains/', 'search'),
    smarturl('usearch/[search_results]=auth.USER.username__icontains/', 'usearch'),
)

