#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test when"""

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


class Test_When(TestCase):

    def setUp(self):
        self.schema_path = Path(
            'tests/../schema/when.schema.json').resolve()
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
                "timespans": [{"start": {"in": "0676"}, "end": {"in": "1066"}}],
                "periods": [
                    {"name": "Anglo-Saxon Period, 449-1066",
                     "@id": "periodo:p06c6g3whtg"},
                    {"name": "Anglo-Saxon (culture or style)",
                     "@id": "http://chronontology.dainst.org/period/O5r960WKERYr"}
                ],
                "label": "sample 'when' w/timespans, periods, duration",
                "duration": "P100Y"
            },
            {"timespans": [{"start": {"in": "1600"}}]},
            {"timespans": [
                {"start": {"in": "1600"}, "end": {"in": "1699"}}]}
        ]
        for v in vals:
            jsonschema.validate(v, self.schema, resolver=self.resolver)

    @raises(ValidationError)
    def test_bad(self):
        jsonschema.validate("this friday", self.schema, resolver=self.resolver)
