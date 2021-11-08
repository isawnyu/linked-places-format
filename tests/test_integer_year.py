#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test integer years"""

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


class Test_IntegerYear(TestCase):

    def setUp(self):
        self.schema_path = Path(
            'tests/../schema/integer_year.schema.json').resolve()
        with open(self.schema_path, 'r', encoding='utf-8') as fp:
            self.schema = ujson.load(fp)
        del fp
        self.resolver = get_resolver(self.schema_path, self.schema)

    def tearDown(self):
        """Change me"""
        pass

    def test_good(self):
        values = [-1, 1, 1000, 1443, 2021, -1530]
        for v in values:
            jsonschema.validate(v, self.schema, resolver=self.resolver)

    @ raises(ValidationError)
    def test_bad_zero(self):
        jsonschema.validate(0, self.schema, resolver=self.resolver)

    @ raises(ValidationError)
    def test_bad_string(self):
        jsonschema.validate('foo', self.schema, resolver=self.resolver)
