#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test the pleiades.datasets geojson module"""

import functools
import geojson
import logging
from nose.tools import assert_equal, assert_false, assert_true, raises
from pathlib import Path
from pleiades.datasets.geojson import Maker, buffer_shape
from pprint import pprint
from shapely.geometry import Point, shape
import sys
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


def logme(f):
    logger = logging.getLogger(sys._getframe().f_back.f_code.co_name)
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        logger.debug(f.__name__)
        return f(*args, **kwargs)
    return wrapped


class Test_GeoJSON(TestCase):

    def setUp(self):
        """Change me"""
        pass

    def tearDown(self):
        """Change me"""
        pass

    def test_maker_default_context(self):
        Maker()

    @logme
    def test_make_feature(self):
        #m = Maker(test_data_path)
        #s = m.make_feature('275740')
        pass

    @logme
    def test_make_feature_collection(self):
        m = Maker(test_data_path)
        gj = m.make_feature_collection('275740')
        print(gj)

    @logme
    @raises(NotImplementedError)
    def test_walk_feature_collection(self):
        m = Maker()
        m.walk_feature_collection()

    
class Test_Buffer(TestCase):

    @logme
    def test_point_buffer(self):
        s = Point(0.0, 0.0)
        g = buffer_shape(s, 1000.0)  # 1km
        s = shape(g)
        c = s.representative_point()
        assert_equal(0, int(c.x))
        assert_equal(0, int(c.y))
        assert_equal()


        
