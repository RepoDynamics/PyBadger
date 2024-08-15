from typing import Protocol as _Protocol, runtime_checkable as _runtime_checkable


AttrDict = dict[str, str | bool] | None


@_runtime_checkable
class Stringable(_Protocol):
    def __str__(self) -> str:
        ...
