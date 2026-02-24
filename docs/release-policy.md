# Release Policy

## Versioning

Use semantic versioning:

- MAJOR: breaking API or behavior changes
- MINOR: backward-compatible features
- PATCH: backward-compatible bug fixes

## Tagging

- release tags: `vX.Y.Z`
- each release must update `CHANGELOG.md`

## Entry Requirements

- CI green
- tests for behavior changes
- migration review completed (if schema changed)
- README/docs updated for user-facing changes
