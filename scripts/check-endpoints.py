#!/usr/bin/env python3
"""Check that every endpoint named in the guides exists in the published OpenAPI documents.

An endpoint is named in Markdown as inline code: `METHOD /prefix/path`, for example
`GET /api/resources/{resourceId}/slots` or `POST /auth/oauth2/token`. The prefix picks the document:
/api -> docs/openapi/resource.json, /auth -> docs/openapi/auth.json. Path parameter names do not have
to match; only their positions do.

A guide that describes an endpoint which is not deployed yet fails this check. That is intended: the
docs pull request stays red until the backend change reaches staging and the sync workflow refreshes
the documents.

OPENAPI_DIR overrides the directory with resource.json and auth.json. The PR check points it at the
documents on the tip of main, so a re-run after a sync sees the new endpoints.
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SPEC_DIR = Path(os.environ.get("OPENAPI_DIR") or DOCS / "openapi")
SPECS = {"/api": SPEC_DIR / "resource.json", "/auth": SPEC_DIR / "auth.json"}
METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")
MENTION = re.compile(r"`(" + "|".join(METHODS) + r") (/[^`\s?#]*)`")
PARAM = re.compile(r"\{[^}/]+\}")


def normalize(path: str) -> str:
    return PARAM.sub("{}", path.rstrip("/") or "/")


def load_operations() -> dict[str, set[tuple[str, str]]]:
    operations = {}
    for prefix, spec_path in SPECS.items():
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        operations[prefix] = {
            (method.upper(), normalize(path))
            for path, item in spec.get("paths", {}).items()
            for method in item
            if method.upper() in METHODS
        }
    return operations


def main() -> int:
    operations = load_operations()
    errors = []
    checked = 0
    for md in sorted(DOCS.rglob("*.md")):
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            for method, full_path in MENTION.findall(line):
                checked += 1
                where = f"{md.relative_to(ROOT)}:{lineno}"
                prefix = next((p for p in SPECS if full_path == p or full_path.startswith(p + "/")), None)
                if prefix is None:
                    errors.append(f"{where}: `{method} {full_path}` must start with one of {', '.join(SPECS)}")
                    continue
                path = normalize(full_path[len(prefix):] or "/")
                if (method, path) not in operations[prefix]:
                    errors.append(f"{where}: `{method} {full_path}` is not in {SPECS[prefix].name}")
    for error in errors:
        print(error, file=sys.stderr)
    print(f"check-endpoints: {checked} endpoint mentions, {len(errors)} not found")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
