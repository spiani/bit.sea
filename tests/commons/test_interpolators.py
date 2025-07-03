from pathlib import Path

import numpy as np
import pytest

from bitsea.commons import netcdf4
from bitsea.commons.dataextractor import DataExtractor
from bitsea.commons.interpolators import _find_interval_overlapping
from bitsea.commons.interpolators import compose_methods
from bitsea.commons.interpolators import Fine2Coarse2dInterpolator
from bitsea.commons.interpolators import regular
from bitsea.commons.interpolators import space_interpolator_griddata
from bitsea.commons.mask import Mask


@pytest.mark.uses_test_data
def test_interpolator(tmp_path: Path, test_data_dir: Path):
    masks_dir = test_data_dir / "masks"
    Mask1 = Mask.from_file(masks_dir / "mask_006_014_reduced.nc")
    Mask2 = Mask.from_file(masks_dir / "interpolator_mask.nc")

    filename = test_data_dir / "ave.20241027-12:00:00.N1p.nc"

    VAR = DataExtractor(Mask1, filename, "N1p").values

    A = space_interpolator_griddata(Mask2, Mask1, VAR)
    B = regular(Mask1, Mask2, VAR, method="nearest")
    C = compose_methods(Mask1, Mask2, VAR)
    A[~Mask2] = 1.0e20

    netcdf4.write_3d_file(
        A, "N1p", tmp_path / "griddata.nc", Mask2, fillValue=1e20
    )
    netcdf4.write_3d_file(
        B, "N1p", tmp_path / "regular.nc", Mask2, fillValue=1e20
    )
    netcdf4.write_3d_file(
        C, "N1p", tmp_path / "composed.nc", Mask2, fillValue=1e20
    )


def test_find_interval_overlapping_01():
    v1 = np.array([0, 2, 5, 10], dtype=np.float32)
    v2 = np.array([1, 3, 7, 9], dtype=np.float32)

    overlaps = _find_interval_overlapping(v1, v2)

    assert overlaps.shape[1] == 2
    assert overlaps.shape[0] == v2.size - 1

    assert overlaps[0][0] == 0
    assert overlaps[0][1] == 2
    assert overlaps[1][0] == 1
    assert overlaps[1][1] == 3
    assert overlaps[2][0] == 2
    assert overlaps[2][1] == 3


def test_find_interval_overlapping_outside_right():
    v1 = np.array([0, 2, 5, 10], dtype=np.float32)
    v2 = np.array([1, 3, 7, 11], dtype=np.float32)

    overlaps = _find_interval_overlapping(v1, v2)

    assert overlaps.shape[1] == 2
    assert overlaps.shape[0] == v2.size - 1

    assert overlaps[0][0] == 0
    assert overlaps[0][1] == 2
    assert overlaps[1][0] == 1
    assert overlaps[1][1] == 3
    assert overlaps[2][0] == 2
    assert overlaps[2][1] == 3


def test_find_interval_overlapping_outside_left():
    v1 = np.array([0, 2, 5, 10], dtype=np.float32)
    v2 = np.array([-3, -1, 7, 11], dtype=np.float32)

    overlaps = _find_interval_overlapping(v1, v2)

    assert overlaps.shape[1] == 2
    assert overlaps.shape[0] == v2.size - 1

    assert overlaps[0][0] == 0
    assert overlaps[0][1] == 0
    assert overlaps[1][0] == 0
    assert overlaps[1][1] == 3
    assert overlaps[2][0] == 2
    assert overlaps[2][1] == 3


def test_find_interval_overlapping_all_outside_left():
    v1 = np.array([0, 2, 5, 10], dtype=np.float32)
    v2 = np.array([-5, -3, -2, -1], dtype=np.float32)

    overlaps = _find_interval_overlapping(v1, v2)

    assert overlaps.shape[1] == 2
    assert overlaps.shape[0] == v2.size - 1

    assert np.all(overlaps == 0)


def test_find_interval_overlapping_all_outside_right():
    v1 = np.array([0, 2, 5, 10], dtype=np.float32)
    v2 = np.array([11, 12, 13, 14], dtype=np.float32)

    overlaps = _find_interval_overlapping(v1, v2)

    assert overlaps.shape[1] == 2
    assert overlaps.shape[0] == v2.size - 1

    assert np.all(overlaps == 3)


def test_fine_to_coarse_interpolator_01():
    v1_lat = np.linspace(0, 1, 11)
    v1_lon = np.linspace(10, 11, 21)

    v2_lat = np.linspace(0.2, 0.9, 4)
    v2_lat *= v2_lat
    v2_lon = np.linspace(10.2, 10.9, 5)
    Fine2Coarse2dInterpolator(
        fine_lats=v1_lat,
        fine_lons=v1_lon,
        coarse_lats=v2_lat,
        coarse_lons=v2_lon,
    )
