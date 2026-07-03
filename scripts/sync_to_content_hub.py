"""velog → content-hub 역방향 동기화 (설계서 3.2).

velog에 직접 작성한 글 중 content-hub에 없는 글을 감지해
content-hub 클론의 posts/에 frontmatter 스키마(설계서 4장)로 생성한다.
git 커밋/PR 생성은 워크플로(content-hub-sync.yml)가 담당한다.

사용법:
    python scripts/sync_to_content_hub.py --content-hub ./content-hub [--dry-run]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import frontmatter
import requests

USERNAME = "kik328288"
GRAPHQL_URL = "https://v2cdn.velog.io/graphql"

POSTS_QUERY = """
query Posts($username: String!, $cursor: ID) {
  posts(username: $username, cursor: $cursor, limit: 50) {
    id
    title
    body
    released_at
    url_slug
    tags
    series {
      name
    }
  }
}
"""


def fetch_velog_posts() -> list[dict]:
    """공개 글 전체를 커서 페이지네이션으로 수집."""
    posts: list[dict] = []
    cursor = None
    while True:
        resp = requests.post(
            GRAPHQL_URL,
            json={"query": POSTS_QUERY, "variables": {"username": USERNAME, "cursor": cursor}},
            timeout=30,
        )
        resp.raise_for_status()
        page = (resp.json().get("data") or {}).get("posts") or []
        if not page:
            break
        posts.extend(page)
        cursor = page[-1]["id"]
    return posts


def collect_known_slugs(content_hub: Path) -> set[str]:
    """content-hub이 이미 알고 있는 slug 집합 (파일명 + velog_url + aliases)."""
    known: set[str] = set()
    for folder in ("posts", "drafts", "velog_ready"):
        base = content_hub / folder
        if not base.exists():
            continue
        for md in base.rglob("*.md"):
            known.add(md.stem)
            try:
                meta = frontmatter.load(md).metadata
            except Exception:
                continue
            url = meta.get("velog_url") or ""
            if url:
                known.add(url.rstrip("/").split("/")[-1])
            for alias in meta.get("aliases") or []:
                known.add(str(alias))
    return known


def sanitize_filename(slug: str) -> str:
    """Windows/Git에서 안전한 파일명으로 정리."""
    return re.sub(r'[\\/:*?"<>|]', "-", slug).strip()


def to_markdown(post: dict) -> str:
    """velog 글을 content-hub frontmatter 스키마로 변환."""
    fm = frontmatter.Post(post["body"] or "")
    fm.metadata = {
        "title": post["title"],
        "slug": post["url_slug"],
        "type": "post",
        "date": (post.get("released_at") or "")[:10],
        "tags": post.get("tags") or [],
        "series": (post.get("series") or {}).get("name", "") or "",
        "source": "velog",
        "status": "published",  # 이미 velog에 존재하는 글
        "velog_url": f"https://velog.io/@{USERNAME}/{post['url_slug']}",
        "visibility": "public",
    }
    return frontmatter.dumps(fm)


def write_github_output(**kwargs: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    with open(output_file, "a", encoding="utf-8") as f:
        for key, value in kwargs.items():
            f.write(f"{key}={value}\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--content-hub", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    content_hub: Path = args.content_hub
    if not (content_hub / "posts").exists():
        print(f"::error::content-hub 경로가 올바르지 않습니다: {content_hub}")
        return 1

    velog_posts = fetch_velog_posts()
    known = collect_known_slugs(content_hub)
    missing = [p for p in velog_posts if p["url_slug"] not in known]
    print(f"[scan] velog 공개 글 {len(velog_posts)}건 / content-hub 미보유 {len(missing)}건")

    created: list[str] = []
    for post in missing:
        slug = post["url_slug"]
        dest = content_hub / "posts" / f"{sanitize_filename(slug)}.md"
        if args.dry_run:
            print(f"  [dry] {slug}")
            continue
        dest.write_text(to_markdown(post), encoding="utf-8")
        created.append(slug)
        print(f"  [new] {dest.name}")

    write_github_output(created=str(len(created)), created_slugs=",".join(created[:20]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
