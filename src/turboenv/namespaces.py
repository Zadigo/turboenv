import pathlib
from collections import defaultdict
from typing import Any, Optional

from pydantic import BaseModel, Field


class NamespaceModel(BaseModel):
    name: str | None = Field(default=None)
    cache: dict[str, str] = Field(default_factory=dict)


class NamespaceValues:
    _cache: defaultdict[str, NamespaceModel] = defaultdict(lambda: NamespaceModel())

    def __init__(self, name: str, values: dict[str, Any]):
        self.name = name

        ns = self._cache[name]
        ns.name = name
        ns.cache.update(values)

        # ".env" file that was used to load the values
        # for this namespace, if any
        self.file: Optional[pathlib.Path] = None
