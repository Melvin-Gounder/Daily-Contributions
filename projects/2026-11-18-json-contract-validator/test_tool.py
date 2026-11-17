import unittest
from tool import validate

class Tests(unittest.TestCase):
    def test_valid_nested(self):
        s = {"type":"object","required":["items"],"properties":{"items":{"type":"array","items":{"type":"integer"}}}}
        self.assertEqual(validate({"items":[1,2]},s), [])
    def test_paths(self):
        s = {"type":"array","items":{"type":"integer","minimum":0}}
        self.assertEqual(validate([1,-1,"x"],s), ["$[1]: below minimum","$[2]: expected integer"])
    def test_bool_not_int(self):
        self.assertEqual(validate(True,{"type":"integer"}), ["$: expected integer"])
    def test_unknown_key(self):
        s = {"type":"object","properties":{},"additionalProperties":False}
        self.assertEqual(validate({"x":1},s), ["$.x: unexpected property"])
    def test_required(self):
        self.assertEqual(validate({},{"type":"object","required":["id"]}), ["$.id: required"])
    def test_invalid_schema(self):
        with self.assertRaises(ValueError):
            validate(1,{"type":"imaginary"})

if __name__ == "__main__":
    unittest.main()
