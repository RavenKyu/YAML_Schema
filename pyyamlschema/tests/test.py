#!/usr/bin/env python
# coding=utf-8

import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from pyyamlschema import YamlSchema

data = [
    {
        "name": "홍길동",
        "cellphone": "010-1345-7764",
        "address": "이상국 행복리 234",
        "age": 33
    },
    {
        "name": "홍길동",
        "age": 33
    },
    {
        "name": "홍길동",
        "address": "이상국 행복리 234",
    },
    {
        "name": "홍길동",
        "cellphone": "012-1345-7764",
        "age": 33
    }
]

print("Validating the input data using jsonschema:")

schema = YamlSchema("example.yaml")
import json
for idx, item in enumerate(data):
    try:
        validate(item, json.loads(schema.json))
        sys.stdout.write("Record #{}: OK\n".format(idx))
    except ValidationError as ve:
        sys.stderr.write("Record #{}: ERROR\n".format(idx))
        sys.stderr.write(str(ve) + "\n")


