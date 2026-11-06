import unittest
from validator import validate, Problem

class ContractTests(unittest.TestCase):
    def test_nested_paths(self):
        schema={"type":"object","required":["users"],"properties":{
            "users":{"type":"array","items":{"type":"object","properties":{
                "age":{"type":"integer","min":0}}}}}}
        self.assertEqual(validate({"users":[{"age":-1},{"age":"bad"}]},schema),
                         [Problem("$.users[0].age","below minimum"),
                          Problem("$.users[1].age","expected integer")])
    def test_required_and_extra(self):
        schema={"type":"object","required":["id"],"properties":{"id":{"type":"integer"}},
                "additional":False}
        self.assertEqual(validate({"extra":1},schema),
                         [Problem("$.id","required"),Problem("$.extra","unexpected field")])
    def test_boolean_not_integer(self):
        self.assertEqual(validate(True,{"type":"integer"}),
                         [Problem("$","expected integer")])
    def test_string_and_array_bounds(self):
        self.assertEqual(len(validate(["x"],{"type":"array","min":2,
            "items":{"type":"string","min":2}})),2)
    def test_good(self):
        self.assertEqual(validate({"id":2},{"type":"object","required":["id"],
            "properties":{"id":{"type":"integer","min":1}}}),[])
    def test_invalid_schema(self):
        with self.assertRaises(ValueError):
            validate(1,{"type":"mystery"})

if __name__ == "__main__":
    unittest.main()
