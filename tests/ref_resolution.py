#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Local $ref resolution for jsonschema"""

import jsonschema
import logging
from pprint import pformat
import ujson

base_uri = 'https://pleiades.stoa.org/linkedplaces/schema/'
logger = logging.getLogger(__name__)
cache = dict()


def get_refs(base_path, schema, depth=1):
    global cache
    refs = set()
    i = len(base_uri)

    if isinstance(schema, list):
        for item in schema:
            refs.update(get_refs(base_path, item, depth=depth + 1))
    elif isinstance(schema, dict):
        for k, val in schema.items():
            if k == '$ref':
                if val[:i] == base_uri:
                    refs.add(val)
                    try:
                        s = cache[val]
                    except KeyError:
                        fn = val[i:]
                        with open(base_path / fn, 'r', encoding='utf-8') as fp:
                            s = ujson.load(fp)
                        del fp
                        cache[val] = s
                    refs.update(get_refs(base_path, s, depth=depth + 1))
            else:
                refs.update(get_refs(base_path, val, depth=depth + 1))
    return refs


def get_resolver(schema_path, schema):
    base_path = schema_path.parent
    refs = get_refs(base_path, schema)
    store = dict()
    for ref in list(refs):
        try:
            s = cache[ref]
        except KeyError:
            logger.debug(f'Cache miss: {ref}')
        else:
            store[ref] = s
    resolver = jsonschema.RefResolver(
        base_uri=base_uri,
        referrer=schema,
        store=store)
    return resolver
