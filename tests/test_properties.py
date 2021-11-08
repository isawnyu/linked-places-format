#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test feature properties"""

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


class Test_Properties(TestCase):

    def setUp(self):
        self.schema_path = Path(
            'tests/../schema/properties.schema.json').resolve()
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
                'title': 'Shah Tepe',
            },
            {
                'title': 'Shah Tepe',
                'ccodes': ['AFG']
            }
        ]
        for p in vals:
            jsonschema.validate(p, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_no_title(self):
        jsonschema.validate({'ccodes': ['AFG']},
                            self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_title(self):
        d = {
            'title': 8675309,
            'ccodes': ['AFG']
        }
        jsonschema.validate(d, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_whitespace_title(self):
        d = {
            'title': '     ',
            'ccodes': ['AFG']
        }
        jsonschema.validate(d, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_empty_title(self):
        d = {
            'title': '',
            'ccodes': ['AFG']
        }
        jsonschema.validate(d, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_empty_ccodes(self):
        d = {
            'title': '',
            'ccodes': []
        }
        jsonschema.validate(d, self.schema, resolver=self.resolver)
