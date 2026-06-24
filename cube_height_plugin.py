"""Cube Height Filter -- ParaView Python plugin sample.

読み込んだ vtkUnstructuredGrid に対して、
  * Height スライダーで Z 方向の高さを動的に変更し、
  * ユーザ定義関数によるスカラー (SurfaceAreaLike) を計算して付与する。

Tools > Manage Plugins/Extensions から読み込んで使用する。
"""
from paraview.util.vtkAlgorithm import smproxy, smproperty, smdomain
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy
import numpy as np


# ---- 純粋関数（副作用なし・入力不変） ----
def scaled_points(points, height):
    """Z 座標だけを height 倍した新しい点群を返す。"""
    return np.column_stack((points[:, 0], points[:, 1], points[:, 2] * height))


def surface_area_like(points, height):
    """ユーザ定義関数の例。実際の表面積計算に差し替え可能。"""
    return np.hypot(points[:, 0], points[:, 1]) * height


def to_vtk_points(np_points):
    pts = vtkPoints()
    pts.SetData(numpy_to_vtk(np.ascontiguousarray(np_points), deep=True))
    return pts


def named_array(values, name):
    arr = numpy_to_vtk(np.ascontiguousarray(values), deep=True)
    arr.SetName(name)
    return arr


@smproxy.filter(name="CubeHeightFilter", label="Cube Height Filter")
@smproperty.input(name="Input")
class CubeHeightFilter(VTKPythonAlgorithmBase):
    def __init__(self):
        super().__init__(nInputPorts=1, nOutputPorts=1,
                         outputType="vtkUnstructuredGrid")
        self._height = 1.0  # 枠組みが要求する唯一の状態

    @smproperty.doublevector(name="Height", default_values=1.0)
    @smdomain.doublerange(min=0.1, max=10.0)  # <- これでスライダーになる
    def SetHeight(self, value):
        self._height = value
        self.Modified()

    def RequestData(self, request, inInfo, outInfo):
        src = vtkUnstructuredGrid.GetData(inInfo[0])
        dst = vtkUnstructuredGrid.GetData(outInfo)
        dst.ShallowCopy(src)  # トポロジは共有

        old_pts = vtk_to_numpy(src.GetPoints().GetData())
        new_pts = scaled_points(old_pts, self._height)
        scalars = surface_area_like(old_pts, self._height)

        # ---- VTK の手続き的境界（副作用はここだけ） ----
        dst.SetPoints(to_vtk_points(new_pts))
        dst.GetPointData().AddArray(named_array(scalars, "SurfaceAreaLike"))
        return 1
