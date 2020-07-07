#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create GeoJSON versions of Pleiades gazetteer data
"""

from copy import deepcopy
import geojson
import json
import logging
from pathlib import Path
from pprint import pformat
import pyproj
from pyproj.crs import ProjectedCRS
from pyproj.crs.coordinate_operation import AzumuthalEquidistantConversion
from pyproj import Transformer
from shapely.geometry import box, MultiPolygon, Polygon, polygon, shape
from shapely.ops import transform
import sys

logger = logging.getLogger(__name__)

DEFAULT_CONTEXT = Path(__file__).parent.parent / 'data' / 'json'
GEO_KEYS = {
    'type': '',
    'geometry': '',
    'properties': ''
}
WGS84 = pyproj.CRS('EPSG:4326')


def get_aeqd(x, y):
    proj_str = ' '.join(
        [
            '+proj=aeqd',
            '+lat_0={}'.format(y),
            '+lon_0={}'.format(x)
        ]
    )
    aeqd = pyproj.CRS(proj_str)
    return aeqd


def t_from_wgs84(projection):
    return pyproj.Transformer.from_crs(
        WGS84, projection, always_xy=True).transform


def t_to_wgs84(projection):
    return pyproj.Transformer.from_crs(
        projection, WGS84, always_xy=True).transform


def buffer_shape(s, distance):
    """Buffer shape by distance in meters
    Returns a geojson polygon geometry
    """

    # transform s to an azimuthal equidistant projection
    # with origin at the centroid of the shape
    c = s.centroid
    aeqd = get_aeqd(c.x, c.y)
    tformer = t_from_wgs84(aeqd)
    s_aeqd = transform(tformer, s)

    # calculate the buffer points and transform back to WGS84
    # tolerance is used in simplification below, but we calculate it here
    # roughly based on an average number of meters/degree and scaled
    # against the overall distance so that we can add it to the buffer
    # so that when simplified the convex hull likely covers all possible
    # area where the feature is to be found
    tolerance = 1.0 / (98821.0 / round(distance/10, 1))
    b_aeqd = s_aeqd.buffer(distance + tolerance)
    tformer = t_to_wgs84(aeqd)
    b = transform(tformer, b_aeqd)

    # construct a simplified polygon based on a convex hull
    # around the buffer points
    h = b.convex_hull
    h_simple = h.simplify(tolerance, preserve_topology=True)
    clean_ring = [(float(c[0]), float(c[1])) for c in h_simple.exterior.coords]

    # return the polygon in geojson format
    g = geojson.Polygon([clean_ring])
    if not g.is_valid:
        msg = (
            'Invalid geojson Polygon while making buffer: {}\n{}'.format(
                g.errors(), pformat(g.coordinates, indent=4)))
        raise RuntimeError(msg)
    return g


class Maker(object):
    """Make GeoJSON from Pleiades idiosyncratic JSON"""

    def __init__(self, context=DEFAULT_CONTEXT):
        logger.debug(context)
        if not isinstance(context, Path):
            msg = (
                'Maker instantiated with a context of type {}. Only Path '
                'is currently supported.'.format(
                    type(context)))
            raise NotImplementedError(msg)
        self.context = context

    def make_feature(self, PID=None):
        """Create a GeoJSON feature from Pleiades JSON for PID"""
        if PID is None:
            msg = 'Expected Pleiades ID for PID argument. Got None.'
            raise ValueError(msg)
        if isinstance(self.context, Path):
            with open(
                self.context / '{}.json'.format(PID), encoding='utf-8'
            ) as f:
                j = json.load(f)
            del f
            properties = {}
            geometries = self._make_geometries(j)
            geo_feature = geojson.Feature(
                id=j['id'],
                title=j['title'],
                description=j['description'],
                properties=properties,
                geometry=geometries
            )
            if not geo_feature.is_valid:
                msg = 'Invalid Feature'
                raise RuntimeError(msg)
            return geojson.dumps(geo_feature, sort_keys=True, indent=4)
        else:
            raise NotImplementedError(type(self.context))

    def make_feature_collection(self, PID=None):
        """Create a GeoJSON FeatureCollection from Pleiades JSON for PID"""
        if PID is None:
            msg = 'Expected Pleiades ID for PID argument. Got None.'
            raise ValueError(msg)
        if isinstance(self.context, Path):
            with open(
                self.context / '{}.json'.format(PID), encoding='utf-8'
            ) as f:
                pleiades_json = json.load(f)
            del f
            locations = pleiades_json['locations']
            features = self._make_features(locations, pleiades_json)
            creator_names = [c['name'] for c in pleiades_json['creators']]
            contributor_names = [
                c['name'] for c in pleiades_json['contributors']
                if c['name'] not in creator_names]
            fc = geojson.FeatureCollection(
                bbox=self._make_bbox(features),
                contributors=contributor_names,
                creators=creator_names,
                description=pleiades_json['description'],
                features=features,
                id=pleiades_json['id'],
                rights=pleiades_json['rights'],
                title=pleiades_json['title'],
                uri=pleiades_json['uri'])
            if not fc.is_valid:
                msg = 'Invalid FeatureCollection'
                raise RuntimeError(msg)
            return geojson.dumps(
                fc, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            raise NotImplementedError(type(self.context))

    def walk_feature_collection(self):
        raise NotImplementedError(sys._getframe().f_code.co_name)

    def _make_bbox(self, features):
        """Create a bounding box containing all features"""
        shapes = [shape(f.geometry) for f in features]
        bounds = [(s.bounds) for s in shapes]
        boxes = [box(*b) for b in bounds]
        return MultiPolygon(boxes).bounds

    def _make_buffer(self, feature):
        """Create an accuracy buffer for a given feature"""

        s = shape(feature.geometry)
        g = buffer_shape(s, feature.properties['positional_accuracy'])
        buffer = geojson.Feature(
            geometry=g,
            properties={
                'title': 'Accuracy buffer for {}'.format(
                    feature.properties['title']),
                'description': (
                    'Generated using the python Shapely package '
                    '(https://github.com/Toblerity/Shapely), '
                    'this convex hull delineates a region of space '
                    'roughly corresponding to a {} meter buffer '
                    'around the feature geometry; i.e., the '
                    '"positional accuracy" recorded in the Pleiades '
                    'gazetteer for this location.'.format(
                        feature.properties['positional_accuracy']))
            }
        )
        if not buffer.is_valid:
            msg = 'Invalid Buffer: {}'.format(buffer.errors())
            raise RuntimeError(msg)
        logger.debug(
            'Valid buffer: \n{}'.format(
                pformat(buffer, indent=4)
            )
        )
        return buffer

    def _make_centroid(self, features):
        return None

    def _make_feature(self, location, place: dict):
        """Make geojson feature reflecting the precise location geometry"""
        creator_names = [c['name'] for c in location['creators']]
        contributor_names = [
            c['name'] for c in location['contributors']
            if c['name'] not in creator_names]
        feature = geojson.Feature(
            geometry=self._make_geometry(location),
            properties={
                'positional_accuracy': location['accuracy_value'],
                'archaeological_remains': location['archaeologicalRemains'],
                'association_certainty': location['associationCertainty'],
                'contributors': contributor_names,
                'creators': creator_names,
                'description': location['description'],
                'end': location['end'],
                'feature_type': [
                    ft.strip() for ft in location['featureType'] if ft.strip()
                    != ''],
                'location_type': location['locationType'],
                'rights': place['rights'],
                'start': location['start'],
                'title': location['title'],
                'uri': location['uri']
            }
        )
        if not feature.is_valid:
            msg = 'Invalid Feature'
            raise RuntimeError(msg)
        return feature

    def _make_features(self, locations: list, place: dict):
        """Make features and accuracy buffers for all locations"""
        features = [self._make_feature(l, place) for l in locations]
        logger.debug('len features: {}'.format(len(features)))
        buffers = [self._make_buffer(f) for f in features]
        logger.debug('len buffers: {}'.format(len(buffers)))
        all_features = features + buffers
        logger.debug('features and buffers:\n{}'.format(pformat(all_features, indent=4)))
        return all_features

    def _make_hull(self, features):
        return None

    def _make_geometries(self, j: dict):
        geo_collection = geojson.GeometryCollection(
            [self._make_geometry(location) for location in j['locations']])
        if not geo_collection.is_valid:
            msg = 'Invalid GeometryCollection'
            raise RuntimeError(msg)
        return geo_collection

    def _make_geometry(self, location: dict):
        return getattr(
            geojson,
            location['geometry']['type'])(
                location['geometry']['coordinates'])


