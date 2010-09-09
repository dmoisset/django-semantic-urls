from django.conf.urls.defaults import *
from route import url 

urlpatterns = patterns('mysite.polls.views',
    url('', 'index'),
    url('<poll>=polls.Poll.pk/', 'detail'),
    url('<poll>=polls.Poll.pk/results/', 'results'),
    url('<poll>=polls.Poll.pk/vote/', 'vote'),
    url('search/[search_results]=polls.Poll.question__icontains/', 'search'),
    url('usearch/[search_results]=auth.USER.username__icontains/', 'usearch'),
)

