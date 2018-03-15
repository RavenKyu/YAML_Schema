# PyYamlSchema

## 목적
데이터를 서비스끼리 주고 받을 때 JSON 형태를 많이 이용합니다. 데이터를 생성 또는 수정시 우리는 정의된 유효 값과 형태 유지에 대한 방법이 필요합니다. 자료를 주고 받는 두 클라이언트와 서버는 각자의 방법으로 값의 무결점을 확인해왔습니다. 이 방법은 각자의 방식대로 검사를 해왔습니다.

JSON은 유효 값 범위가 정의된 JSON-Schema 를 작성하여 처리할 데이터를 검증할 수 있었습니다. 아래의 순서를 거쳐서 자동으로 Schema를 생성하는 모듈도 존재합니다.

1. 더미 Json 데이터 생성
2. genson 을 이용하여 Json-Schema 자동 생성
3. 필요에 따라 생성된 Schema에 유효값 추가

JSON은 각종 개발 언어 입장에서 다루기 적합한 형태를 가지고 있지만 아래의 문제점을 가지고 있습니다.

* 내용이 길어질수록 데이터를 확인하기 어려움
* 주석(Comment)를 남길 수 없으므로 해당 데이터의 정의 문서를 보지 않으면 구분하기 힘듬

이런 문제점을 해결하면서 JSON과 1:1로 대응되는 것으로 YAML이 있습니다. YAML 형태로 정의한 데이터는 내부 주석을 확인 할 수 있으며 형태가 간단하여 판단을 쉽게 할 수 있습니다. 개발시 JSON으로 변환 모듈을 이용하여 접근도 용의 합니다.

Json 더미 데이터를 YAML 형태로 작성하여 변환 과정에 추가해 줍니다.

1. 더미 YAML 데이터 생성
2. 더미 데이터를 JSON 형태로 변환
3. genson 을 이용하여 Json-Schema 자동 생성
4. 필요에 따라 생성된 Schema에 유효값 추가

이것으로 데이터를 쉽게 검증하고 스키마를 유지할 수 있을 거 같지만, 한 가지 문제점이 존재합니다. 3번과 4번 사이에 사람이 또다시 개입하는 점, 더미 데이터가 바뀔때 마다 4번 작업을 다시 해줘야 하는 것이 문제입니다.

**이것을 해결하기 위해 만든 것이 `PyYamlSchema`입니다.**

PyYamlSchema는 YAML 더미 데이터 작성시 Schema에 추가적으로 들어갈 유효 값을 함께 작성함으로서 더미 데이터를 보는 것 만으로도 데이터에 대한 정의를 파악할 수 있습니다.

`PyYamlShema`는 명시된 유효 값은 `genson`이 요구하는 형태로 바꾸어 Schema 생성시 사용자가 명시한 유효 값 범위를 자동으로 추가합니다.

사용자는 한 번의 YAML 데이터 작성으로 JSON 값과 Schema 생성 및 유효 값 검사까지 처리할 수 있습니다.

## 설치
`pip install pyyamlschema`

or

`pip install git+https://github.com/RavenKyu/YAML_Schema.git
`
## 사용법
### Python에서 모듈로 사용하기
```python
from pyyamlschema import YamlSchema

yml = YamlSchema()
yml.open("sample.yml")
print(yml.json)  # yaml을 json 형태로 변환한 것을 보여줍니다.
print(yml.schemas)  # 기본 형태의 Json Schema를 생성합니다.
print(yml.yaml)  # yaml 데이터를 보여줍니다.

# Or yml = YamlSchema("sample.yml")
# It doesn't need to use `open` method.
```

### Shell
```bash
$ pyyamlschema sample.yml # yaml을 json 형태로 변환한 것을 보여줍니다.
$ pyyamlschema sample.yml -j # yaml을 json 형태로 변환한 것을 보여줍니다.
$ pyyamlschema sample.yml -c # 기본 형태의 Json Schema를 생성합니다.
$ pyyamlschema sample.yml -e # 확장 YAML 코멘트를 추가하여 Json Schema를 생성합니다.
```

## 확장 YAML 주석
YAML에서 사용하는 주석으로 `유효 값 범위 지정` 및 `확장 코드`를 생성할 수 있습니다.
```yaml

---
name : John Doe
cellphone: 010-1345-7764
#! pattern: ^[01]{3}-[0-9]{4}-[0-9]{4}$
address: Seoul, Korea
age: 33
#! maximum: 100
#! minimum: 0
```

