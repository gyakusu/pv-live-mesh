"""Cube Height Filter の純粋な数値変換ロジック。

ParaView / VTK に依存しないため単体テストと型検査が可能で、プラグイン本体
(``cube_height_plugin.py``) はここから関数を取り込む。すべて副作用のない純粋関数で、
入力は不変として扱う。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    import numpy.typing as npt


def scaled_points(
    points: npt.NDArray[np.float64],
    height: float,
) -> npt.NDArray[np.float64]:
    """Z 座標だけを ``height`` 倍した新しい点群を返す。"""
    stacked = np.column_stack((points[:, 0], points[:, 1], points[:, 2] * height))
    return np.asarray(stacked, dtype=np.float64)


def surface_area_like(
    points: npt.NDArray[np.float64],
    height: float,
) -> npt.NDArray[np.float64]:
    """ユーザ定義関数の例。実際の表面積計算に差し替え可能。"""
    radius = np.hypot(points[:, 0], points[:, 1])
    return np.asarray(radius * height, dtype=np.float64)
