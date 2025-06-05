import sys
import types
import math
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Provide a minimal geopy.distance.geodesic implementation
_distance_module = types.ModuleType("geopy.distance")

def _haversine(c1, c2):
    R = 6371000
    lat1, lon1 = c1
    lat2, lon2 = c2
    phi1, phi2 = map(math.radians, [lat1, lat2])
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def geodesic(c1, c2):
    return types.SimpleNamespace(meters=_haversine(c1, c2))

_distance_module.geodesic = geodesic
_geopy_module = types.ModuleType("geopy")
_geopy_module.distance = _distance_module
sys.modules.setdefault("geopy", _geopy_module)
sys.modules.setdefault("geopy.distance", _distance_module)

from utils.geo import find_nearest_office

import pytest

@pytest.fixture
def offices():
    return [
        {"name": "Office A", "lat": 47.0, "lon": 106.0},
    ]

def test_find_nearest_office_within_radius(offices):
    user_lat, user_lon = 47.0005, 106.0005
    is_inside, name, distance = find_nearest_office(user_lat, user_lon, offices, radius_meters=100)
    assert is_inside is True
    assert name == "Office A"
    assert distance <= 100

def test_find_nearest_office_outside_radius(offices):
    user_lat, user_lon = 47.01, 106.01
    result = find_nearest_office(user_lat, user_lon, offices, radius_meters=100)
    assert result == (False, None, None)
