import json
import sys
import os

from jsonschema import Draft4Validator
from referencing import Registry
from referencing.jsonschema import DRAFT4

# ensure three parameters
if len(sys.argv) != 3:
    print(f"The validator needs two arguments: mode (repository/dataset/state/scenario), filename")
    sys.exit()

# ensure mode valid
if (
    sys.argv[1] != "repository"
    and sys.argv[1] != "dataset"
    and sys.argv[1] != "state"
    and sys.argv[1] != "scenario"
):
    print(f"Invalid mode: {sys.argv[1]}")
    sys.exit()

# ensure file exists
payload = {}
if os.path.isfile(sys.argv[2]):
    with open(sys.argv[2]) as fs:
        payload = json.loads(fs.read())
else:
    print(f"Invalid file location: {sys.argv[2]}")
    sys.exit()


# create registry of referenced files
def registry_with_files(files: list[str]) -> Registry:
    base_uri = "https://dsbrennan.github.io/pear/schemas/"
    registry = Registry()
    for file in files:
        local_file = file.removeprefix(base_uri) if file.startswith(base_uri) else file
        with open(os.path.join("schemas", local_file)) as fs:
            schema = DRAFT4.create_resource(json.loads(fs.read()))
            registry = registry.with_resource(uri=file, resource=schema)
    return registry

# create a schema validator
def create_schema_validator(schema: str, register_files: list[str]) -> Draft4Validator:
    # process validation
    print(f"Processing {schema} validation for file {sys.argv[2]}")
    with open(os.path.join("schemas", schema)) as fs:
        schema = json.loads(fs.read())
        return Draft4Validator(
            schema=schema,
            registry=registry_with_files(register_files),
        )


validator = None
if sys.argv[1] == "repository":
    validator = create_schema_validator(
        "repository.json",
        [
            "https://dsbrennan.github.io/pear/schemas/entity.json",
            "https://dsbrennan.github.io/pear/schemas/link.json",
            "https://dsbrennan.github.io/pear/schemas/dataset.json",
        ],
    )

elif sys.argv[1] == "dataset":
    validator = create_schema_validator(
        "dataset.json",
        [
            "https://dsbrennan.github.io/pear/schemas/entity.json",
            "https://dsbrennan.github.io/pear/schemas/link.json",
            "https://dsbrennan.github.io/pear/schemas/state.json",
        ],
    )
elif sys.argv[1] == "state":
    validator = create_schema_validator(
        "state.json",
        [
            "https://dsbrennan.github.io/pear/schemas/entity.json",
            "https://dsbrennan.github.io/pear/schemas/link.json",
            "https://dsbrennan.github.io/pear/schemas/software.json",
            "https://dsbrennan.github.io/pear/schemas/file.json",
            "https://dsbrennan.github.io/pear/schemas/scenario.json",
        ],
    )
elif sys.argv[1] == "scenario":
    validator = create_schema_validator(
        "scenario.json",
        [
            "https://dsbrennan.github.io/pear/schemas/entity.json",
            "https://dsbrennan.github.io/pear/schemas/software.json",
            "https://dsbrennan.github.io/pear/schemas/file.json",
        ],
    )

# validate schema
if validator != None:
    print(f"Validation results (no results equals pass):")
    validator.validate(payload)
