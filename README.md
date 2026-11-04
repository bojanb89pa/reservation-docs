# reservation-docs

Public documentation of the Reserva API, published at <https://reserva-docs.bojanlab.com>.

Everything in this repository is in **English**: pages, changelog, commit messages, pull requests and issues.

## Layout

| Path | What | Who changes it |
| --- | --- | --- |
| `docs/openapi/*.json` | Public OpenAPI documents from staging | Only the `Sync OpenAPI` workflow |
| `docs/reference/` | Scalar pages that render those documents | Rarely, by hand |
| `docs/guides/`, `docs/changelog.md` | Integration guides and changelog | By hand, or by the docs agent |
| `docs/*.md` | Introduction, getting started, authentication | By hand |

Endpoint descriptions, parameters and examples come from the backend code. Fix them there, not here.

## Workflows

- **PR check** (`pr-check.yml`): `mkdocs build --strict`, `scripts/check-endpoints.py` (every
  `` `METHOD /api/...` `` or `` `METHOD /auth/...` `` named in the docs must exist in the OpenAPI documents),
  and a check for Serbian letters.
- **Pages** (`pages.yml`): builds and deploys the site on every push to `main`.
- **Sync OpenAPI** (`sync-openapi.yml`): downloads the public documents from staging after each backend
  deploy (`repository_dispatch` `be-deployed`), every 6 hours, or on demand, and commits them when they change.

## Local preview

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```
