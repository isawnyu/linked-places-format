#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test strings containing URIs"""

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


class Test_URI(TestCase):

    def setUp(self):
        self.schema_path = Path(
            'tests/../schema/uri.schema.json').resolve()
        with open(self.schema_path, 'r', encoding='utf-8') as fp:
            self.schema = ujson.load(fp)
        del fp
        self.resolver = get_resolver(self.schema_path, self.schema)

    def tearDown(self):
        """Change me"""
        pass

    def test_good(self):
        values = ['https://pleiades.stoa.org/places/570662',
                  'http://www.geonames.org/148730/zanzibar.html',
                  'http://n2t.net/ark:/99152/p086kj9dcst',
                  'periodo:p086kj9dcst']
        for v in values:
            jsonschema.validate(v, self.schema, resolver=self.resolver)

    @ raises(ValidationError)
    def test_bad_string(self):
        jsonschema.validate('foo', self.schema, resolver=self.resolver)

    @ raises(ValidationError)
    def test_bad_whitespace(self):
        jsonschema.validate('\t    ', self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_integer(self):
        jsonschema.validate(8675309, self.schema, resolver=self.resolver)
