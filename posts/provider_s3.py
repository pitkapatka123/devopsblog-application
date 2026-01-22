from __future__ import annotations

import os
from typing import List, Optional
import boto3

from .models import Page
from .markdown_utils import parse_front_matter_and_body, markdown_to_html


class S3ContentProvider:
    """
    S3-only provider.

    Expected keys under prefix:
      <prefix>about.md
      <prefix>contact.md
      <prefix>posts/<slug>.md

    Reads from S3 on every request (no caching).
    """

    def __init__(self) -> None:
        bucket = os.getenv("POSTS_S3_BUCKET", "").strip()
        prefix = os.getenv("POSTS_S3_PREFIX", "").strip()

        if not bucket:
            raise RuntimeError("POSTS_S3_BUCKET env var is required")

        if prefix and not prefix.endswith("/"):
            prefix = prefix + "/"

        self.bucket = bucket
        self.prefix = prefix
        self.s3 = boto3.client("s3")

    def _get_text(self, key: str) -> Optional[str]:
        try:
            obj = self.s3.get_object(Bucket=self.bucket, Key=key)
            data = obj["Body"].read()
            return data.decode("utf-8")
        except self.s3.exceptions.NoSuchKey:
            return None

    def _page_from_key(self, slug: str, kind: str, key: str) -> Optional[Page]:
        raw = self._get_text(key)
        if raw is None:
            return None

        meta, body = parse_front_matter_and_body(raw)
        html = markdown_to_html(body)

        if "title" not in meta:
            meta["title"] = slug.replace("-", " ").title()

        return Page(slug=slug, kind=kind, meta=meta, html=html, key=key)

    def list_posts(self) -> List[Page]:
        base = f"{self.prefix}posts/"
        posts: List[Page] = []

        paginator = self.s3.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self.bucket, Prefix=base):
            for item in page.get("Contents", []):
                key = item["Key"]
                if not key.endswith(".md"):
                    continue

                filename = key.split("/")[-1]  # hello-world.md
                slug = filename[:-3]           # hello-world

                p = self._page_from_key(slug=slug, kind="post", key=key)
                if p:
                    posts.append(p)

        return posts

    def get_post(self, slug: str) -> Optional[Page]:
        key = f"{self.prefix}posts/{slug}.md"
        return self._page_from_key(slug=slug, kind="post", key=key)

    def get_page(self, slug: str) -> Optional[Page]:
        key = f"{self.prefix}{slug}.md"
        return self._page_from_key(slug=slug, kind="page", key=key)
