#!/usr/local/bin/bash

script_path=$(realpath $0)
tests_dir_path=$(dirname $script_path)
schema_dir_path=$(dirname $tests_dir_path)
test_data_dir_path="$schema_dir_path/test_data"

component='ccodes'

echo $component
jsonschema -o pretty --instance "$test_data_dir_path/$component.json" "$schema_dir_path/$component.json"
