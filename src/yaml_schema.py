from genson import Schema
import yaml as Yaml
import json as Json
import copy

schemas = list()
stack = list()
cur = str()


def make_json_schema(v, value, buf=None):
    if buf is None:
        buf = dict()
    if not v:
        buf.update(value)
        return buf
    name = v.pop(0)
    buf.update({"properties": {name: dict()}})
    return make_json_schema(v, value, buf["properties"][name])


def yaml_extention_parser(v, depth=0):
    global cur
    global stack

    # 데이터 아님
    while True:
        if not v:
            return schemas
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
            stack.append(name)

        # 상위로 돌아감
        elif depth > len_current:
            depth = len_current
            stack.pop()
        # 같은 레벨
        else:
            pass
    # 확장 코드
    elif -1 < d.find("#! "):
        info = d.strip()[3:]
        name = info[:info.find(":")]
        value = info[info.find(":")+2:]
        value = {cur: {name: value}}
        buf = dict()
        cs = copy.deepcopy(stack)
        # if cs:
        #     cs.pop(0)
        # if not cs:
        buf.update({"properties": dict()})
        temp = buf['properties']
        # else:
        #     temp = buf
        make_json_schema(cs, value, temp)
        schemas.append(buf)
    else:
        d = d.strip()
        name = d[:d.find(":")]
        cur = name
    return yaml_extention_parser(v, depth)








class Yaml2JsonSchema:
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
        schema_list = yaml_extention_parser(v)
        for s in schema_list:
            print(s)
            self.__genson.add_schema(s)
        print(self.to_jsonschema())

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='This utility read YAML type of file, '
                    'Converts to JsonSchema.')
    parser.add_argument('source_file', help='source YAML file')
    parser.add_argument(
        '-y', '--yaml', help='print YAML format', action='store_true')
    parser.add_argument(
        '-j', '--json', help='convert a YAML file to Json format', action='store_true')
    parser.add_argument(
        '-c', '--convert',
        help='convert a YAML file to json-schema', action='store_true')
    parser.add_argument(
        '-e', '--extension',
        help='convert a extended YAML file to json-schema', action='store_true')

    args = parser.parse_args()

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
        # buf = yaml_extention_parser(dict_v)










