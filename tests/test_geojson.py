#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the pleiades.datasets geojson module"""

import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from pathlib import Path
from pleiades.datasets.geojson import Maker
from unittest import TestCase

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
test_data_path = Path('tests/data')


def setup_module():
    """Change me"""
    pass


def teardown_module():
    """Change me"""
    pass


class Test_GeoJSON(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_maker_default_context(self):
        Maker()

    @raises(NotImplementedError)
    def test_make_feature(self):
        m = Maker()
        m.make_feature()

    @raises(NotImplementedError)
    def test_make_feature_collection(self):
        m = Maker()
        m.make_feature_collection()

    @raises(NotImplementedError)
    def test_walk_feature_collection(self):
        m = Maker()
        m.make_feature_collection()

    

