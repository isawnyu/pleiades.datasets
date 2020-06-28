#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create GeoJSON versions of Pleiades gazetteer data
"""

import logging
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

DEFAULT_CONTEXT = Path(__file__).parent.parent / 'data' / 'json'
TEMPLATES = {
    'feature_collection': {
        'type': 'FeatureCollection',
        'features': []
    },
    'feature': {
        'type': 'Feature',
        'geometry': {},
        'properties': {},
    }
}


class Maker(object):
    """Make GeoJSON from Pleiades idiosyncratic JSON"""

    def __init__(self, context=DEFAULT_CONTEXT):
        logger.debug(context)
        self.context = context

    def make_feature(self, PID=None):
        """Create a GeoJSON feature dictionary from Pleiades JSON for PID"""
        raise NotImplementedError(sys._getframe().f_code.co_name)

    def make_feature_collection(self, PIDS=[]):
        """Create a GeoJSON feature collection for each PID in PIDS"""
        raise NotImplementedError(sys._getframe().f_code.co_name)

    def walk_feature_collection(self):
        raise NotImplementedError(sys._getframe().f_code.co_name)


