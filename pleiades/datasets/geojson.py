#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 3 script template (changeme)
"""

import logging
from pathlib import Path

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

    def make_feature(self, PID=None):
        """Create a GeoJSON feature dictionary from Pleiades JSON for PID"""
        pass

    def make_feature_collection(self, PIDS=[]):
        """Create a GeoJSON feature collection for each PID in PIDS"""
        pass


