from genson import Schema
import yaml as Yaml
import json as Json
import copy

import sys
import argparse


def main():
    args = parse_args()

    conv = Yaml2JsonSchema(args.source_file)
    if args.yaml:
        sys.stdout.write(conv.yaml + '\n')
    if args.json:
        sys.stdout.write(conv.json + '\n')
    if args.convert:
        sys.stdout.write(conv.to_jsonschema() + '\n')
    if args.extension:
        dict_v = conv.yaml.split('\n')
        conv.ex_yaml(dict_v)


def parse_args():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='This utility reads YAML file, '
                    'Converts to JSON-Schema.')
    parser.add_argument('source_file', help='source YAML file')
    parser.add_argument(
        '-y', '--yaml', help='print YAML format', action='store_true')
    parser.add_argument(
        '-j', '--json', help='convert a YAML file to Json format',
        action='store_true')
    parser.add_argument(
        '-c', '--convert',
        help='convert a YAML file to json-schema', action='store_true')
    parser.add_argument(
        '-e', '--extension',
        help='convert a extended YAML file to json-schema', action='store_true')

    args = parser.parse_args()

    if not args.source_file:
        sys.stderr.write("No Source File.")
        exit(1)
    return args


class Yaml2JsonSchema:
    schemas = list()
    stack = list()
    cur = str()

    def __init__(self, filename=None):
        self.__yaml = ""
        self.__json = ""
        self.__genson = Schema()
        if filename:
            self.open(filename)

    def to_jsonschema(self):
        return self.__genson.to_json(indent=2)

    @property
    def json(self):
        return self.__json

    @property
    def yaml(self):
        return self.__yaml

    @yaml.setter
    def yaml(self, yaml):
        self.__yaml = yaml
        json = Yaml.load(self.yaml)
        self.__json = Json.dumps(json, indent=2)
        self.__genson.add_object(json)

    def open(self, filename):
        with open(filename, 'r') as f:
            data = f.read()
            self.yaml = data

    def ex_yaml(self, v):
        schema_list = Yaml2JsonSchema.yaml_extention_parser(v)
        for s in schema_list:
            self.__genson.add_schema(s)
        print(self.to_jsonschema())

    @staticmethod
    def make_json_schema(v, value, buf=None):
        if buf is None:
            buf = dict()
        if not v:
            buf.update({"properties": value})
            return buf
        name = v.pop(0)
        buf.update({"properties": {name: dict()}})

        return Yaml2JsonSchema.make_json_schema(
            v, value, buf["properties"][name])

    @staticmethod
    def yaml_extention_parser(v, depth=0):
        # 데이터 아님
        while True:
            if not v:
                return Yaml2JsonSchema.schemas
            d = v.pop(0)
            if -1 == d.find(":"):
                continue
            break

        # 하위 아이템 존재
        if ":" == d[-1]:
            len_current = len(d) - len(d.lstrip())
            # 하위 아이템
            if depth <= len_current:
                depth = len_current
                name = d[:-1].strip()
                Yaml2JsonSchema.stack.append(name)

            # 상위로 돌아감
            elif depth > len_current:
                depth = len_current
                Yaml2JsonSchema.stack.pop()
            # 같은 레벨
            else:
                pass
        # 확장 코드
        elif -1 < d.find("#! "):
            info = d.strip()[3:]
            name = info[:info.find(":")]
            value = info[info.find(":") + 2:]
            value = {Yaml2JsonSchema.cur: {name: value}}
            buf = dict()
            cs = copy.deepcopy(Yaml2JsonSchema.stack)
            temp = buf
            Yaml2JsonSchema.make_json_schema(cs, value, temp)
            Yaml2JsonSchema.schemas.append(buf)
        else:
            d = d.strip()
            name = d[:d.find(":")]
            Yaml2JsonSchema.cur = name
        return Yaml2JsonSchema.yaml_extention_parser(v, depth)











