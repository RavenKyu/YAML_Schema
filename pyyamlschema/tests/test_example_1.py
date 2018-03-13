import unittest
import json
from pyyamlschema import YamlSchema
from apitools.datagenerator import DataGenerator

sample = """{
  "name": "John Doe",
  "cellphone": "010-1345-7764",
  "address": "Seoul, Korea",
  "age": 33
}
"""


class TestUnit (unittest.TestCase):
    def setUp(self):
        self.yamlschema = YamlSchema("example.yaml")
        self.sample = json.loads(sample)
        self.generator = DataGenerator()

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
        schema = self.yamlschema.to_jsonschema()
        for _ in range(3):
            r = self.generator.random_value(json.loads(schema))
            self.yamlschema.is_valid(r)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUnit)
    unittest.TextTestRunner(verbosity=2).run(suite)
