# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog and this project follows Semantic Versioning.

## [Unreleased]

### Added

- Detailed README focused on starter-template usage
- Module development guide: `docs/add-module.md`
- Module scaffold script: `scripts/scaffold_module.py`
- Environment validator tests and service/validator/schema tests
- Migration governance and release policy docs

### Changed

- Unified exception handling path
- Fixed auth service query logic
- Improved Docker dependency install behavior
- Added production secret requirements in compose
- Rate limit storage now supports `RATE_LIMIT_STORAGE_URI`
