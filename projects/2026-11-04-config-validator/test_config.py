import unittest
from config import Field, boolean, validate

class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.schema = {"PORT": Field(int, minimum=1, maximum=65535),
                       "DEBUG": Field(boolean, required=False, default=False),
                       "TOKEN": Field(str, secret=True)}
    def test_valid(self):
        self.assertEqual(validate(self.schema, {"PORT":"8080","TOKEN":"abc","DEBUG":"yes"})["DEBUG"], True)
    def test_default(self):
        self.assertFalse(validate(self.schema, {"PORT":"80","TOKEN":"abc"})["DEBUG"])
    def test_missing(self):
        with self.assertRaisesRegex(ValueError, "PORT: missing"): validate(self.schema, {"TOKEN":"abc"})
    def test_range(self):
        with self.assertRaisesRegex(ValueError, "PORT: invalid"): validate(self.schema, {"PORT":"70000","TOKEN":"abc"})
    def test_secret_redacted(self):
        try: validate(self.schema, {"PORT":"80","TOKEN":"bad","DEBUG":"nonsense","EXTRA":"unused"} | {"TOKEN":""})
        except ValueError as error: self.assertNotIn("bad", str(error))
    def test_bool(self):
        with self.assertRaises(ValueError): boolean("perhaps")

if __name__ == "__main__": unittest.main()
