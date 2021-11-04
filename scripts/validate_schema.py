#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate the schema
"""

from airtight.cli import configure_commandline
from jschon import create_catalog, JSON, JSONSchema
import json
import logging
import pathlib

logger = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    ['-l', '--loglevel', 'NOTSET',
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR',
        False],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)',
        False],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)', False],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
]


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    create_catalog('2020-12')
    p = pathlib.Path(__file__)
    p = p.parent / '..' / 'schema' / 'linkedplaces-schema.json'
    p = p.resolve()
    with open(p, 'r') as fp:
        j = json.load(fp)
    del fp
    lpf_schema = JSONSchema(j)
    prefix = 'in'
    msg = f'JSON schema {p} is '
    if lpf_schema.validate().valid:
        msg += 'valid.'
    else:
        msg += 'INVALID.'
    print(msg)


if __name__ == "__main__":
    main(**configure_commandline(
        OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
