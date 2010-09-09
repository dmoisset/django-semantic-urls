from django.core import urlresolvers
from django.conf.urls.defaults import url
from django.db.models.loading import get_model
from django.db.models import fields
from django.shortcuts import get_object_or_404
from django.db.models.sql.constants import LOOKUP_SEP, QUERY_TERMS

import functools, re

def mapping_str(value):
    return value

def mapping_int(value):
    return int(value)
    # This might raise an exception in unusual cases, ideally the framework will ensure the regex catches invalid data

TYPE_MAP = {
    fields.AutoField: (r'(?P<%s>\d+)', mapping_int),
    fields.CharField: (r'(?P<%s>[^/]*)', mapping_str),
}

def query_type(model, query):
    parts = query.split(LOOKUP_SEP)
    # Normalize query operator:
    if parts[-1] not in QUERY_TERMS:
        parts.append('exact')
    # Lookup field    
    opts = model._meta
    for name in parts[:-2]:
        model = opts.get_field_by_name(name)[0].rel.to
        opts = model._meta
    name = parts[-2]
    if name == 'pk':
        name = opts.pk.name
    field, model, _, _ = opts.get_field_by_name(name)
    return TYPE_MAP[type(field)]

def object_mapper(model, query):
    # find mapping for query
    regex, mapping = query_type(model, query)
    return regex, lambda value: get_object_or_404(model, **{query: mapping(value)})

def queryset_mapper(model, query):
    # find mapping for query
    regex, mapping = query_type(model, query)
    return regex, lambda value: model._default_manager.filter(**{query: mapping(value)})

def parse_object(item):
    name, value = item.split('=', 1)
    app, model, query = value.split('.')
    model_class = get_model(app, model)
    if name[0]=='<' and name[-1]=='>': # Single object mapping
        name = name[1:-1]
        regex, mapping = object_mapper(model_class, query)
    elif name[0]=='[' and name[-1]==']':# Queryset mapping
        name = name[1:-1]
        regex, mapping = queryset_mapper(model_class, query)
    else: # Value mapping
        regex, mapping = query_type(model_class, query)
    assert name.replace('_', '').isalnum() # FIXME: check more cleanly here
    # lookup
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

