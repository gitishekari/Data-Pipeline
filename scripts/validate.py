from pathlib import Path
import sys
import xmlschema

ROOT = Path(__file__).resolve().parent.parent

VALIDATIONS = [
    (ROOT / "schemas" / "cyclingtour.xsd", ROOT / "data" / "cyclingtour.xml"),
    (ROOT / "schemas" / "tourPackages.xsd", ROOT / "data" / "tourPackages.xml"),
]


def main() -> int:
    has_errors = False
    for xsd_path, xml_path in VALIDATIONS:
        schema = xmlschema.XMLSchema(xsd_path)
        try:
            schema.validate(xml_path)
            print(f"[PASS] {xml_path.name} is valid against {xsd_path.name}")
        except xmlschema.XMLSchemaValidationError as exc:
            has_errors = True
            print(f"[FAIL] {xml_path.name} failed validation against {xsd_path.name}:")
            print(exc)
    return 1 if has_errors else 0


if __name__ == "__main__":
    sys.exit(main())
