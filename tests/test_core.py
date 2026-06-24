"""cube_height_core の純粋関数のテスト。"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from cube_height_core import scaled_points, surface_area_like

if TYPE_CHECKING:
    import numpy.typing as npt


def _grid() -> npt.NDArray[np.float64]:
    return np.array(
        [[1.0, 0.0, 2.0], [0.0, 3.0, 4.0], [-1.0, -1.0, 5.0]],
        dtype=np.float64,
    )


def test_scaled_points_scales_z_only() -> None:
    pts = _grid()
    out = scaled_points(pts, 3.0)
    np.testing.assert_allclose(out[:, 0], pts[:, 0])
    np.testing.assert_allclose(out[:, 1], pts[:, 1])
    np.testing.assert_allclose(out[:, 2], pts[:, 2] * 3.0)


def test_scaled_points_identity_at_unit_height() -> None:
    pts = _grid()
    np.testing.assert_allclose(scaled_points(pts, 1.0), pts)


def test_scaled_points_dtype_and_shape() -> None:
    out = scaled_points(_grid(), 2.0)
    assert out.dtype == np.float64
    assert out.shape == (3, 3)


def test_scaled_points_does_not_mutate_input() -> None:
    pts = _grid()
    before = pts.copy()
    scaled_points(pts, 9.0)
    np.testing.assert_array_equal(pts, before)


def test_surface_area_like_matches_hypot() -> None:
    pts = _grid()
    out = surface_area_like(pts, 2.0)
    expected = np.hypot(pts[:, 0], pts[:, 1]) * 2.0
    np.testing.assert_allclose(out, expected)


def test_surface_area_like_shape() -> None:
    out = surface_area_like(_grid(), 1.0)
    assert out.shape == (3,)
