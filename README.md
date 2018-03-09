# PyYamlSchema
PyYamlSchema 
## installation
`pip install pyyamlschema`
## Usage
### Python Module
```python
from pyyamlschema import YamlSchema

yml = YamlSchema()
yml.open("sample.yml")
print(yml.json)  # print converted json format
print(yml.schemas)  # print converted json-schema
print(yml.yaml)  # print source yaml data

# Or yml = YamlSchema("sample.yml")
# It doesn't need to use `open` method.
```

### Shell
```bash
$ yamlschema sample.yml # print converted json format
$ yamlschema sample.yml -j # print converted json format
$ yamlschema sample.yml -c # print json-schema of sample.yml
$ yamlschema sample.yml -e # print json-schema of sample.yml included extension comments
```

## Ex-YAML Comments
If you want to define `Validations of Json-Schema` to YAML file, You can just write like this.
```yaml

---
name : "John Doe"
cellphone: "010-1345-7764"
#! pattern: ^[01]{3}-[0-9]{4}-[0-9]{4}$
address: "Seoul, Korea"
age: 33
```

