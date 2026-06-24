"""``paraview.util.vtkAlgorithm`` の最小スタブ（本プラグインが使う範囲のみ）。"""

from collections.abc import Callable
from typing import TypeVar

_C = TypeVar("_C", bound=type)
_F = TypeVar("_F")

class smproxy:
    @staticmethod
    def filter(*, name: str, label: str) -> Callable[[_C], _C]: ...

class smproperty:
    @staticmethod
    def input(*, name: str) -> Callable[[_C], _C]: ...
    @staticmethod
    def doublevector(*, name: str, default_values: float) -> Callable[[_F], _F]: ...

class smdomain:
    @staticmethod
    def doublerange(*, min: float, max: float) -> Callable[[_F], _F]: ...
