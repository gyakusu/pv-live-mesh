"""data.make_sample のテスト。"""

from __future__ import annotations

from data.make_sample import (
    NX,
    NY,
    NZ,
    all_cells,
    all_points,
    build_vtk_text,
    point_index,
)


def test_point_index_is_sequential() -> None:
    assert point_index(0, 0, 0) == 0
    assert point_index(1, 0, 0) == 1
    assert point_index(0, 1, 0) == NX + 1


def test_all_points_count() -> None:
    assert len(all_points()) == (NX + 1) * (NY + 1) * (NZ + 1)


def test_all_cells_count_and_size() -> None:
    cells = all_cells()
    assert len(cells) == NX * NY * NZ
    assert all(len(c) == 8 for c in cells)


def test_hexahedron_indices_in_range() -> None:
    npoints = (NX + 1) * (NY + 1) * (NZ + 1)
    for cell in all_cells():
        assert all(0 <= idx < npoints for idx in cell)


def test_build_vtk_text_structure() -> None:
    text = build_vtk_text()
    lines = text.splitlines()
    assert lines[0] == "# vtk DataFile Version 3.0"
    assert lines[2] == "ASCII"
    assert f"POINTS {(NX + 1) * (NY + 1) * (NZ + 1)} float" in lines
    assert f"CELLS {NX * NY * NZ} {NX * NY * NZ * 9}" in lines
    assert f"CELL_TYPES {NX * NY * NZ}" in lines
    assert text.endswith("\n")
