# Add a Business Module

This guide defines the standard way to add a new module so the project remains consistent and reusable.

## 1. Create Schema

Add request/query schema in `app/schemas/<module>.py` with Pydantic models.

Example responsibilities:

- input shape
- field constraints
- default values

## 2. Create Model (if needed)

Add SQLAlchemy model in `app/models/<module>.py`.

Rules:

- explicit table name
- proper indexes for query paths
- `to_dict()` for stable output mapping

## 3. Create Service

Add business logic in `app/services/<module>.py`.

Rules:

- service layer should not depend on HTTP request objects
- raise `BusinessError` subclasses for expected failures
- rollback DB session on persistence errors

## 4. Create Controller

Add endpoint file in `app/controller/<module>.py`.

Rules:

- keep controller thin
- validate request with decorators from `app/utils/validators.py`
- call service functions
- return data via `success()`

## 5. Register Blueprint

In `app/controller/__init__.py`:

- add `Blueprint` instance
- import module file at bottom

In `app/__init__.py`:

- import blueprint
- register blueprint with explicit `url_prefix`

## 6. Add Tests

Add API tests in `tests/test_<module>.py`.

Minimum cases:

- success path
- validation error
- unauthorized/forbidden case (if protected)
- not found/conflict case (if applicable)
- paging/filter boundary cases

## 7. Keep Contracts Consistent

- response envelope format must stay consistent
- errors should include stable `code` and `request_id`
- logs and metrics should work without module-specific instrumentation

## 8. Update Docs

Update README if the new module is intended as part of the public example set.

If it is product-specific logic, keep it out of README and document it in a dedicated internal doc.
