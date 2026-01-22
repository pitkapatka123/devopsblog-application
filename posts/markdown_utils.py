from __future__ import annotations

from typing import Any, Dict, Tuple
import yaml
import markdown as md


def parse_front_matter_and_body(raw: str) -> Tuple[Dict[str, Any], str]:
    if raw.startswith("---\n"):
        parts = raw.split("\n---\n", 1)
        if len(parts) == 2:
            fm_block = parts[0][4:]  # strip leading ---\n
            body = parts[1]
            meta = yaml.safe_load(fm_block) or {}
            return meta, body
    return {}, raw


def markdown_to_html(body: str) -> str:
    return md.markdown(body, extensions=["fenced_code", "tables"])
