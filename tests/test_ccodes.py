#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test ccodes (county codes)"""

from ref_resolution import get_resolver
import jsonschema
from jsonschema.exceptions import ValidationError
import ujson
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from pathlib import Path
from unittest import TestCase

logger = logging.getLogger(__name__)
test_data_path = Path('tests/data').resolve()

country_codes = dict()


def setup_module():
    global county_codes
    with open(test_data_path / 'county-codes.json') as fp:
        datahub_codes = ujson.load(fp)
    del fp
    for code_key in ['ISO3166-1-Alpha-2', 'ISO3166-1-Alpha-3', 'ISO3166-1-numeric']:
        test_key = code_key[10:].lower()
        country_codes[test_key] = [country[code_key]
                                   for country in datahub_codes if country[code_key] is not None]


def teardown_module():
    """Change me"""
    pass


class Test_CCodes(TestCase):

    def setUp(self):
        self.schema_path = Path('tests/../schema/ccodes.schema.json').resolve()
        with open(self.schema_path, 'r', encoding='utf-8') as fp:
            self.schema = ujson.load(fp)
        del fp
        self.resolver = get_resolver(self.schema_path, self.schema)

    def tearDown(self):
        """Change me"""
        pass

    def test_good(self):
        code_keys = ['alpha-2', 'alpha-3', 'numeric']
        good_values = list()
        for k in code_keys:
            test_list = country_codes[k]
            jsonschema.validate(test_list, self.schema)
            test_list = [country_codes[k][0], ]
            jsonschema.validate(test_list, self.schema)

    @ raises(ValidationError)
    def test_bad_list(self):
        test_list = ['', None, 'A', 1, '1', 'banana', '0009']
        jsonschema.validate(test_list, self.schema)

    @ raises(ValidationError)
    def test_empty_list(self):
        test_list = []
        jsonschema.validate(test_list, self.schema)
