#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test timespans"""

from types import resolve_bases
from ref_resolution import get_resolver
import jsonschema
from jsonschema.exceptions import ValidationError
import ujson
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from pathlib import Path
from unittest import TestCase

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()


def teardown_module():
    """Change me"""
    pass


class Test_Timespans(TestCase):

    def setUp(self):
        self.schema_path = Path(
            'tests/../schema/timespans.schema.json').resolve()
        with open(self.schema_path, 'r', encoding='utf-8') as fp:
            self.schema = ujson.load(fp)
        del fp
        self.resolver = get_resolver(self.schema_path, self.schema)

    def tearDown(self):
        """Change me"""
        pass

    def test_good(self):
        vals = [
            {
                "start": {
                    "in": "0676"
                },
                "end": {
                    "in": "1066"
                }
            },
            {
                "start": {
                    "in": "1858"
                }
            },
            {
                "start": {
                    "earliest": "-0440-01-01",
                    "latest": "-0439-07-15"
                }
            },
            {
                "start": {
                    "in": "2020",
                    "earliest": "2020-03-01",
                    "latest": "2020-09-15"
                }
            }
        ]
        for v in vals:
            jsonschema.validate([v], self.schema, resolver=self.resolver)
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_no_start(self):
        vals = [
            {'end': {"in": "2021"}}
        ]
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_empty(self):
        vals = []
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_terminus_key(self):
        vals = [{'start': {'circa': '1848'}}]
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_date(self):
        vals = [{'start': {'in': 'spider monkey'}}]
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_emtpy_terminus(self):
        vals = [{'start': {}}]
        jsonschema.validate(vals, self.schema, resolver=self.resolver)
