from django.core import urlresolvers
from django.conf.urls.defaults import url
from django.db.models.loading import get_model

import functools, re

def mapping_str(value):
    return value

def mapping_int(value):
    return int(value)
    # This might raise an exception in unusual cases, ideally the framework will ensure the regex catches invalid data

def object_mapper(model, query):
    # get model by name
    model_class = get_model('polls', model) # FIXME: use right app
    # find mapping for query
    mapping = mapping_str # FIXME: find right mapping from query
    # FIXME: probably we want get_object_or_404 here
    return lambda value: model_class._default_manager.get(**{query: mapping(value)})

def queryset_mapper(model, query):
    # get model by name
    model_class = get_model('polls', model) # FIXME: use right app
    # find mapping for query
    mapping = mapping_str # FIXME: find right mapping
    return lambda value: model_class._default_manager.filter(**{query: mapping(value)})

def parse_object(item):
    name, value = item.split('=', 1)
    regex = r'(?P<%s>[^/]*)'
    if name[0]=='<' and name[-1]=='>': # Single object mapping
        name = name[1:-1]
        model, query = value.split('.')
        mapping = object_mapper(model, query)
    elif name[0]=='[' and name[-1]==']':# Queryset mapping
        name = name[1:-1]
        model, query = value.split('.')
        mapping = queryset_mapper(model, query)
    else: # Value mapping
        mapping = mapping_str
    assert name.replace('_', '').isalnum() # FIXME: check more cleanly here
    # lookup
    return regex, name, mapping

def parse_value(item):
    name, value = item.split(':', 1)
    assert name.replace('_', '').isalnum() # FIXME: check more cleanly here
    regex = r'(?P<%s>[^/]*)'
    mapping = mapping_str # lookup the right mapping function
    return regex, name, mapping    

class NewURLPattern(urlresolvers.RegexURLPattern):
    def __init__(self, path, callback, default_args=None, name=None):
        # FIXME: handle include URLs
        regex = []
        self.mapping = {}
        # Build regex, and dict of "mappers"
        for item in path.split('/'):
            if '=' in item:
                item_regex, name, item_mapping = parse_object(item)
                regex.append(item_regex % name)
                self.mapping[name] = item_mapping
            else: 
                regex.append(re.escape(item))
        regex = '^'+'/'.join(regex)+'$'
        super(NewURLPattern, self).__init__(regex, callback, default_args, name)

    def resolve(self, path):
        match = super(NewURLPattern, self).resolve(path)
        if match:
            callback, args, kwargs = match
            # FIXME: Yes, I'm wrapping the function each time, this is inefficient
            # Build function
            def inner(request, *innerargs, **innerkw):
                for name in self.mapping:
                    innerkw[name] = self.mapping[name](innerkw[name])
                return callback(request, *innerargs, **innerkw)
            return functools.update_wrapper(inner, callback), args, kwargs

def view(path, viewname, kwargs=None, name=None):
    # FIXME: handle include URLs
    return NewURLPattern(path, viewname, kwargs, name)

