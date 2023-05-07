#@+leo-ver=5-thin
#@+node:tom.20230203183434.1: * @file test_dataset.py
if __name__ == '__main__':
    import os.path
    import sys
    dir_ = os.path.dirname(__file__)
    dir_ = os.path.dirname(dir_)
    sys.path.insert(0, dir_)

import pytest
from Dataset import Dataset

NUMPTS = 10
PRECISION = (1e-3, 1e-5)  # (relative, absolute)

#@+others
#@+node:tom.20230203185010.1: ** test_normalize
def test_normalize():
    """The y data should be normalized to 1.0."""
    x = range(NUMPTS)
    y = [50. - z ** 2 for z in x]
    ds = Dataset(x, y)

    ds.normalize()
    normed = max(ds.ydata)
    requirement = 1.0

    assert normed == pytest.approx(requirement, *PRECISION)
#@+node:tom.20230203223101.1: ** test_set_ascii_data

def test_get_ascii_data():
# setAsciiData(self, lines, filename='', root = None)
    DATALINES = ['0  0', '1 1', '2   4', '3   9', '4   16']
    ds = Dataset()
    result = ds.setAsciiData(DATALINES)

    actual_x, actual_y = ds.xdata, ds.ydata
    expected_x = [float(x.split()[0]) for x in DATALINES]
    expected_y = [float(x.split()[1]) for x in DATALINES]

    assert bool(result) is False
    assert actual_x == pytest.approx(expected_x, *PRECISION)
    assert actual_y == pytest.approx(expected_y, *PRECISION)

#@+node:tom.20230203231108.1: ** test set_ascii_data_bad
def test_get_ascii_data_bad():
    """Data ingest should skip bad rows."""
    DATALINES = ['0  0', '1 1', '2x   4', '3   9.xz', '4   16']
    ds = Dataset()
    result = ds.setAsciiData(DATALINES)
    actual_x, actual_y = ds.xdata, ds.ydata
    # expected_x = [float(x.split()[0]) for x in DATALINES]
    splits = [z.split() for z in DATALINES]
    sx, sy = zip(*splits)
    expected_x, expected_y = [], []
    for i, s in enumerate(sx):
        try:
            x_ = float(s)
            y_ = float(sy[i])
        except ValueError:
            continue
        else:
            expected_x.append(x_)
            expected_y.append(y_)
    assert result != ''
    assert actual_x == pytest.approx(expected_x, *PRECISION)
    assert actual_y == pytest.approx(expected_y, *PRECISION)
#@-others

test_normalize()
test_get_ascii_data()
test_get_ascii_data_bad()
#@-leo
