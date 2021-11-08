#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test periods"""

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


class Test_Periods(TestCase):

    def setUp(self):
        self.schema_path = Path(
            'tests/../schema/periods.schema.json').resolve()
        with open(self.schema_path, 'r', encoding='utf-8') as fp:
            self.schema = ujson.load(fp)
        del fp
        self.resolver = get_resolver(self.schema_path, self.schema)

    def tearDown(self):
        """Change me"""
        pass

    def test_good(self):
        vals = [{
            "name": "Anglo-Saxon Period, 449-1066",
            "@id": "periodo:p06c6g3whtg"
        },
            {
            "name": "Anglo-Saxon (culture or style)",
            "@id": "http://chronontology.dainst.org/period/O5r960WKERYr"
        }
        ]
        for v in vals:
            jsonschema.validate([v], self.schema, resolver=self.resolver)
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_empty(self):
        vals = []
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_uri(self):
        vals = [{
            "name": "Anglo-Saxon Period, 449-1066",
            "@id": "Arlo Guthrie"
        }]
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_emtpy_uri(self):
        vals = [{
            "name": "Anglo-Saxon Period, 449-1066",
            "@id": ""
        }]
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @ raises(ValidationError)
    def test_bad_empty_name(self):
        vals = [{
            "name": "",
            "@id": "periodo:p06c6g3whtg"
        }]
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @ raises(ValidationError)
    def test_bad_whitespace_name(self):
        vals = [{
            "name": "    ",
            "@id": "periodo:p06c6g3whtg"
        }]
        jsonschema.validate(vals, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad_extraneous(self):
        vals = [{
            "name": "Anglo-Saxon Period, 449-1066",
            "@id": "periodo:p06c6g3whtg",
            "description": "Has nothing to do with King Arthur"
        }]
        jsonschema.validate(vals, self.schema, resolver=self.resolver)
