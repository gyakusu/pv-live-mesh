"""``vtkmodules.util.vtkAlgorithm`` の最小スタブ。"""

class VTKPythonAlgorithmBase:
    def __init__(
        self,
        *,
        nInputPorts: int = ...,
        nOutputPorts: int = ...,
        outputType: str = ...,
    ) -> None: ...
    def Modified(self) -> None: ...
