#!/usr/bin/env python3
"""Generate a new business module skeleton.

Usage:
  python scripts/scaffold_module.py --name comment
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _snake_to_title(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def _write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        print(f"skip: {path.relative_to(ROOT)} already exists")
        return
    path.write_text(content, encoding="utf-8")
    print(f"create: {path.relative_to(ROOT)}")


def generate(module_name: str) -> None:
    title_name = _snake_to_title(module_name)

    controller_file = ROOT / "app" / "controller" / f"{module_name}.py"
    service_file = ROOT / "app" / "services" / f"{module_name}.py"
    model_file = ROOT / "app" / "models" / f"{module_name}.py"
    schema_file = ROOT / "app" / "schemas" / f"{module_name}.py"
    test_file = ROOT / "tests" / f"test_{module_name}.py"

    controller_tpl = f'''"""Example module: {module_name}."""

from flask import g

from app.controller import {module_name}_bp
from app.utils import success
from app.utils.validators import validate_json_content_type, validate_request
from app.schemas.{module_name} import Create{title_name}
from app.services.{module_name} import create_{module_name}


@{module_name}_bp.route("/add", methods=["POST"])
@validate_json_content_type()
@validate_request(Create{title_name})
def add_{module_name}():
    data = g.validated_data
    return success(create_{module_name}(data))
'''

    service_tpl = f'''"""Service layer for {module_name}."""


def create_{module_name}(data):
    return {{"module": "{module_name}", "payload": data.model_dump()}}
'''

    model_tpl = f'''"""SQLAlchemy model for {module_name}."""

from app.extensions.extensions import db


class {title_name}(db.Model):
    __tablename__ = "{module_name}s"

    id = db.Column(db.Integer, primary_key=True)
'''

    schema_tpl = f'''"""Pydantic schema for {module_name}."""

from pydantic import BaseModel, Field


class Create{title_name}(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
'''

    test_tpl = f"""def test_{module_name}_placeholder():
    assert True
"""

    _write_if_missing(controller_file, controller_tpl)
    _write_if_missing(service_file, service_tpl)
    _write_if_missing(model_file, model_tpl)
    _write_if_missing(schema_file, schema_tpl)
    _write_if_missing(test_file, test_tpl)

    print("\nNext steps:")
    print(f"1. Register blueprint `{module_name}_bp` in app/controller/__init__.py")
    print("2. Register blueprint in app/__init__.py")
    print("3. Add model export in app/models/__init__.py if needed")
    print("4. Replace placeholder test with endpoint/service assertions")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a new module")
    parser.add_argument("--name", required=True, help="module name in snake_case")
    args = parser.parse_args()

    module_name = args.name.strip().lower()
    if not module_name.replace("_", "").isalnum():
        raise SystemExit("module name must be snake_case alphanumeric")

    generate(module_name)


if __name__ == "__main__":
    main()
