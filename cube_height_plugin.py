"""Cube Height Filter -- ParaView Python plugin.

読み込んだ vtkUnstructuredGrid に対して、Height スライダーで Z 方向の高さを動的に
変更し、ユーザ定義関数によるスカラー (SurfaceAreaLike) を計算して付与する。

Tools > Manage Plugins/Extensions から本ファイルを読み込んで使用する。数値変換ロジックは
``cube_height_core`` に分離してある（テスト・型検査の対象）。
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np

# ParaView は本ファイルをパス指定で読み込むため、隣接モジュールを import 可能にする。
sys.path.insert(0, str(Path(__file__).resolve().parent))

from paraview.util.vtkAlgorithm import smdomain, smproperty, smproxy
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid

from cube_height_core import scaled_points, surface_area_like

if TYPE_CHECKING:
    from typing import Any

    import numpy.typing as npt
    from vtkmodules.vtkCommonCore import vtkDataArray


# ---- VTK の手続き的境界（副作用はここだけ） ----
def to_vtk_points(np_points: npt.NDArray[np.float64]) -> vtkPoints:
    """numpy 点群を vtkPoints に変換する。"""
    pts = vtkPoints()
    pts.SetData(numpy_to_vtk(np.ascontiguousarray(np_points), deep=True))
    return pts


def named_array(values: npt.NDArray[np.float64], name: str) -> vtkDataArray:
    """名前付きの vtkDataArray を生成する。"""
    arr = numpy_to_vtk(np.ascontiguousarray(values), deep=True)
    arr.SetName(name)
    return arr


@smproxy.filter(name="CubeHeightFilter", label="Cube Height Filter")
@smproperty.input(name="Input")
class CubeHeightFilter(VTKPythonAlgorithmBase):
    """Height スライダーでメッシュを変形し、スカラーを付与するフィルタ。"""

    def __init__(self) -> None:
        super().__init__(nInputPorts=1, nOutputPorts=1, outputType="vtkUnstructuredGrid")
        self._height: float = 1.0  # 枠組みが要求する唯一の状態

    @smproperty.doublevector(name="Height", default_values=1.0)
    @smdomain.doublerange(min=0.1, max=10.0)  # <- これでスライダーになる
    def SetHeight(self, value: float) -> None:
        """Height スライダーの値を保持し、再計算をトリガする。"""
        self._height = value
        self.Modified()

    def RequestData(self, request: Any, inInfo: Any, outInfo: Any) -> int:
        """入力グリッドを変形し、スカラーを付与して出力する。"""
        src = vtkUnstructuredGrid.GetData(inInfo[0])
        dst = vtkUnstructuredGrid.GetData(outInfo)
        dst.ShallowCopy(src)  # トポロジは共有

        old_pts = vtk_to_numpy(src.GetPoints().GetData())
        new_pts = scaled_points(old_pts, self._height)
        scalars = surface_area_like(old_pts, self._height)

        dst.SetPoints(to_vtk_points(new_pts))
        dst.GetPointData().AddArray(named_array(scalars, "SurfaceAreaLike"))
        return 1
