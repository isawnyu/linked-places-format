#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test durations"""

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


class Test_Durations(TestCase):

    def setUp(self):
        self.schema_path = Path(
            'tests/../schema/durations.schema.json').resolve()
        with open(self.schema_path, 'r', encoding='utf-8') as fp:
            self.schema = ujson.load(fp)
        del fp
        self.resolver = get_resolver(self.schema_path, self.schema)

    def tearDown(self):
        """Change me"""
        pass

    def test_good(self):
        vals = [
            'P100Y',
            'P1Y',
            'P10M',
            'P51W',
            'P17D'
        ]
        for v in vals:
            jsonschema.validate(v, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_empty(self):
        jsonschema.validate('', self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_whitespace(self):
        jsonschema.validate('\t', self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_initial(self):
        jsonschema.validate('Q100Y', self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_final(self):
        jsonschema.validate('P100S', self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_integer(self):
        jsonschema.validate('P1o0Y', self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_missing_integer(self):
        jsonschema.validate('PY', self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_missing_initial(self):
        jsonschema.validate('100Y', self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_missing_final(self):
        jsonschema.validate('P100', self.schema, resolver=self.resolver)
