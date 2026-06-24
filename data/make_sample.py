#!/usr/bin/env python3
"""``data/sample_grid.vtk`` を生成する（外部ライブラリ不要・標準ライブラリのみ）。

Cube Height Filter のデモ用に、Z=0..1 の平板状の六面体メッシュを書き出す。
すべて純粋関数・再代入なしで構成している。
"""

from __future__ import annotations

from pathlib import Path

NX, NY, NZ = 5, 5, 1  # セル数（X, Y, Z 方向）。解像度を変えたい場合はここを編集。


def point_index(i: int, j: int, k: int) -> int:
    """格子点 (i, j, k) の通し番号を返す。"""
    return i + (NX + 1) * (j + (NY + 1) * k)


def point_coord(i: int, j: int, k: int) -> tuple[float, float, float]:
    """格子点 (i, j, k) の座標を返す。x, y は [-1, 1]、z は [0, 1] に正規化。"""
    return (-1.0 + 2.0 * i / NX, -1.0 + 2.0 * j / NY, k / NZ)


def all_points() -> tuple[tuple[float, float, float], ...]:
    """全格子点の座標を返す。"""
    return tuple(
        point_coord(i, j, k) for k in range(NZ + 1) for j in range(NY + 1) for i in range(NX + 1)
    )


def hexahedron(ci: int, cj: int, ck: int) -> tuple[int, ...]:
    """セル (ci, cj, ck) を構成する 8 点の通し番号を VTK_HEXAHEDRON 順で返す。"""
    corners = (
        (ci, cj, ck),
        (ci + 1, cj, ck),
        (ci + 1, cj + 1, ck),
        (ci, cj + 1, ck),
        (ci, cj, ck + 1),
        (ci + 1, cj, ck + 1),
        (ci + 1, cj + 1, ck + 1),
        (ci, cj + 1, ck + 1),
    )
    return tuple(point_index(*c) for c in corners)


def all_cells() -> tuple[tuple[int, ...], ...]:
    """全六面体セルを返す。"""
    return tuple(hexahedron(ci, cj, ck) for ck in range(NZ) for cj in range(NY) for ci in range(NX))


def build_vtk_text() -> str:
    """レガシー VTK 形式（ASCII / UNSTRUCTURED_GRID）のテキストを生成する。"""
    points = all_points()
    cells = all_cells()

    header = (
        "# vtk DataFile Version 3.0",
        "Cube Height Filter sample (hexahedral plate)",
        "ASCII",
        "DATASET UNSTRUCTURED_GRID",
        f"POINTS {len(points)} float",
    )
    point_lines = (f"{x:.6f} {y:.6f} {z:.6f}" for (x, y, z) in points)
    cell_header = (f"CELLS {len(cells)} {len(cells) * 9}",)
    cell_lines = ("8 " + " ".join(str(idx) for idx in cell) for cell in cells)
    type_header = (f"CELL_TYPES {len(cells)}",)
    type_lines = ("12" for _ in cells)  # 12 = VTK_HEXAHEDRON

    return "\n".join(
        (
            *header,
            *point_lines,
            *cell_header,
            *cell_lines,
            *type_header,
            *type_lines,
            "",
        ),
    )


def main() -> None:
    """サンプルファイルを生成して保存する。"""
    out = Path(__file__).resolve().parent / "sample_grid.vtk"
    out.write_text(build_vtk_text(), encoding="ascii")
    print(f"wrote {out}")  # noqa: T201


if __name__ == "__main__":
    main()
