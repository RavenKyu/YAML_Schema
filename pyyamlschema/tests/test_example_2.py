import unittest
import json
from pyyamlschema import YamlSchema
from apitools.datagenerator import DataGenerator

sample = """{
  "metadata": {
    "title": "Test Scenario",
    "data_type": "scenario",
    "email": "hong18s@gmail.com",
    "cellphone": "010-9508-1234",
    "age": 10,
    "related_dates": {
      "created": 1520413079,
      "last_modified": 1520413079
    },
    "related_people": {
      "author": "Raven,",
      "last_modified_by": "Jerry"
    },
    "comment": "Auto connection for LinkedIn http://www.linkedin.com"
  },
  "body": {
    "start": {
      "title": "TEST Block",
      "link": "TTT"
    }
  }
}
"""


class TestUnit (unittest.TestCase):
    def setUp(self):
        self.yamlschema = YamlSchema("example2.yaml")
        self.generator = DataGenerator()
        self.sample = json.loads(sample)

    def tearDown(self):
        pass

    def test001_init(self):
        return True

    def test002_property_json(self):
        # json 결과물 검사
        j = self.yamlschema.json
        self.assertTrue(json.loads(j), json.loads(sample))

    def test003_validation_with_sample(self):
        self.yamlschema.is_valid(self.sample)

    def test004_random_value_validation(self):
        schema = self.yamlschema.yaml_to_jsonschema()
        self.generator.not_required_probability = 1
        print(json.loads(schema))
        r = self.generator.random_value(json.loads(schema))
        print(r)
        print(json.loads(schema))
        print(self.yamlschema.is_valid(r))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUnit)
    unittest.TextTestRunner(verbosity=2).run(suite)
