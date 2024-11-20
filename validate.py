import json
import sys
import os

from jsonschema import Draft4Validator
from referencing import Registry
from referencing.jsonschema import DRAFT4

# ensure three parameters
if len(sys.argv) != 3:
    print(f"The validator needs two arguments: mode (dataset/scenario), filename")
    sys.exit()

# ensure mode valid
if sys.argv[1] != "dataset" and sys.argv[1] != "scenario":
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
    registry = Registry()
    for file in files:
        with open(os.path.join("schema", file)) as fs:
            schema = DRAFT4.create_resource(json.loads(fs.read()))
            registry = registry.with_resource(uri=file, resource=schema)
    return registry


validator = None
if sys.argv[1] == "dataset":
    # process dataset validation
    print(f"Processing dataset validation for file {sys.argv[2]}")
    with open(os.path.join("schema", "dataset.json")) as fs:
        schema = json.loads(fs.read())
        validator = Draft4Validator(schema=schema)
elif sys.argv[1] == "scenario":
    # process scenario validation
    print(f"Processing scenario validation for file {sys.argv[2]}")
    with open(os.path.join("schema", "scenario.json")) as fs:
        schema = json.loads(fs.read())
        validator = Draft4Validator(
            schema=schema, registry=registry_with_files(["dataset.json", "scenario.json"])
        )

# validate schema
if validator != None:
    print(f"Validation results (no results equals pass):")
    validator.validate(payload)
