from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Page:
    slug: str
    kind: str          # "page" or "post"
    meta: Dict[str, Any]
    html: str
    key: str           # S3 key (debug)
