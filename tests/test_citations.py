#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test citations"""

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


class Test_Citations(TestCase):

    def setUp(self):
        self.schema_path = Path(
            'tests/../schema/citations.schema.json').resolve()
        with open(self.schema_path, 'r', encoding='utf-8') as fp:
            self.schema = ujson.load(fp)
        del fp
        self.resolver = get_resolver(self.schema_path, self.schema)

    def tearDown(self):
        """Change me"""
        pass

    def test_good_linkedplaces(self):
        vals = [
            [{
                "label": "Ye Olde Gazetteer (1635)",
                "year": 1635,
                "@id": "http://archive.org/details/yeoldegazetteer"}],
            [{
                "label": "Getty TGN (retrieved 4 May 2018)",
                "@id": "tgn:7011944"}],
            [{
                "label": "Harrumph (1923)",
                "year": 1923,
                "@id": "doi:10.1109/5.771073"}],
            [{
                "label": "Hookland Travels (1635)",
                "year": 1635,
                "@id": "http://somearchive.org/hookland_travels"}]
        ]
        for v in vals:
            jsonschema.validate(v, self.schema, resolver=self.resolver)

    def test_good_pleiades(self):
        vals = [
            [{
                "pleiades_short_title": "Wikipedia (English)",
                "pleiades_citation_detail": "Dharmaraja Ratha",
                "pleiades_bibliographic_uri": "https://www.zotero.org/groups/pleiades/items/CI6F6W7W",
                "pleiades_access_uri": "https://en.wikipedia.org/wiki/Dharmaraja_Ratha"}]
        ]
        for v in vals:
            jsonschema.validate(v, self.schema, resolver=self.resolver)
