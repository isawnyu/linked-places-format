#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test non-empty string"""

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


def setup_module():
    pass


def teardown_module():
    """Change me"""
    pass


class Test_StringNonempty(TestCase):

    def setUp(self):
        self.schema_path = Path(
            'tests/../schema/string_nonempty.schema.json').resolve()
        with open(self.schema_path, 'r', encoding='utf-8') as fp:
            self.schema = ujson.load(fp)
        del fp
        self.resolver = get_resolver(self.schema_path, self.schema)

    def tearDown(self):
        """Change me"""
        pass

    def test_good(self):
        values = ['a', 'beta', 'the quick brown fox jumped over the lazy dog',
                  '\tsongs of chickens    ']
        for v in values:
            jsonschema.validate(v, self.schema, resolver=self.resolver)

    @ raises(ValidationError)
    def test_bad_empty(self):
        jsonschema.validate('', self.schema, resolver=self.resolver)

    @ raises(ValidationError)
    def test_bad_whitespace(self):
        jsonschema.validate('\t    ', self.schema, resolver=self.resolver)
