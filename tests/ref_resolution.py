#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Local $ref resolution for jsonschema"""

import jsonschema
import ujson
base_uri = 'https://pleiades.stoa.org/linkedplaces/schema/'


def get_refs(schema):
    refs = list()
    if isinstance(schema, list):
        for item in schema:
            refs.extend(get_refs(item))
    elif isinstance(schema, dict):
        for k, item in schema.items():
            if k == '$ref':
                refs.append(item)
            else:
                refs.extend(get_refs(item))
    return refs


def get_resolver(schema_path, schema):
    refs = get_refs(schema)
    i = len(base_uri)
    refs = [r for r in refs if r[:i] == base_uri]
    print(refs)
    store = dict()
    for ref in refs:
        fn = ref[i:]
        with open(schema_path.parent / fn, 'r', encoding='utf-8') as fp:
            s = ujson(fp)
        del fp
        store[ref] = s
    print(store)
    resolver = jsonschema.RefResolver(
        base_uri=base_uri,
        referrer=schema,
        store=store)
    return resolver
