"""``vtkmodules.util.numpy_support`` の最小スタブ。"""

from typing import Any

import numpy.typing as npt

from vtkmodules.vtkCommonCore import vtkDataArray

def numpy_to_vtk(num_array: Any, deep: bool = ...) -> vtkDataArray: ...
def vtk_to_numpy(vtk_array: Any) -> npt.NDArray[Any]: ...
