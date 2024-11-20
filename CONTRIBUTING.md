# Contributing to PEAR
Details on how to contribute a dataset or scenario into PEAR to follow.

## Object Validation
Before creating a pull request to include your dataset or scenario, please validate your PEAR objects (JSON files) using the validation tool included within this repo.

To validate your PEAR objects, run the following command where `object_type` is either `dataset` or `scenario` depending on the desired object to be included within PEAR, and `path_to_json_file` is the path to your PEAR object file (JSON file).

```
python validate.py object_type path_to_json_file
```