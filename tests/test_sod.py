import pytest

import sodshock
import numpy as np
from numpy.testing import assert_almost_equal
_VALUES_KEYS = ('energy', 'p', 'u', 'rho', 'rho_total', 'x')


@pytest.fixture
def sod():
    gamma = 1.4
    dustFrac = 0.0
    npts = 500
    t = 0.2
    left_state = (1, 1, 0)
    right_state = (0.1, 0.125, 0.)

    positions, regions, values = sodshock.solve(
        left_state=left_state, right_state=right_state, geometry=(0., 1., 0.5), t=t,
        gamma=gamma, npts=npts, dustFrac=dustFrac
    )
    return positions, regions, values


def test_regions_agree(sod):
    regions = sod[1]
    r_true = {
        'Region 1': (1, 1, 0),
        'Region 2': 'RAREFACTION',
        'Region 3': (0.30313017805064707, 0.42631942817849544, 0.9274526200489506),
        'Region 4': (0.30313017805064707, 0.26557371170530725, 0.9274526200489506),
        'Region 5': (0.1, 0.125, 0.0)
    }
    assert set(regions.keys()) == set(r_true.keys())
    for k in ('Region 1', 'Region 3', 'Region 4', 'Region 5'):
        v1 = r_true[k]
        v2 = regions[k]
        assert len(v1) == len(v2)
        for item1, item2 in zip(v1, v2):
            assert_almost_equal(item1, item2)
    assert regions['Region 2'] == r_true['Region 2']


def test_positions_agree(sod):
    positions = sod[0]
    p_true = {
        'Contact Discontinuity': 0.6854905240097902,
        'Foot of Rarefaction': 0.4859454374877634,
        'Head of Rarefaction': 0.26335680867601535,
        'Shock': 0.8504311464060357
    }
    assert set(positions.keys()) == set(p_true.keys())
    for k, v in p_true.items():
        assert_almost_equal(v, positions[k])


def test_values_agree(sod):
    values = sod[2]
    v_true = _load_data()[2]
    assert set(values.keys()) == set(v_true.keys())
    for k, v1 in v_true.items():
        assert_almost_equal(v1, values[k])


def generate_validation_data():
    p, r, v = sod()
    _save_data(p, r, v)


def _save_data(positions, regions, values):
    import json
    json.dump(positions, open('test-data/positions.json', 'wt'))
    json.dump(regions, open('test-data/regions.json', 'wt'))
    for k in _VALUES_KEYS:
        np.savetxt('test-data/values-{}.txt'.format(k), values[k])


def _load_data():
    import json
    positions = json.load(open('test-data/positions.json', 'rt'))
    regions = json.load(open('test-data/regions.json', 'rt'))
    values = {}
    for k in _VALUES_KEYS:
        values[k] = np.loadtxt('test-data/values-{}.txt'.format(k))

    return positions, regions, values

