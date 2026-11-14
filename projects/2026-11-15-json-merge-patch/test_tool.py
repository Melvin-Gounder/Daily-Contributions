import unittest
from tool import merge_patch, apply_json

class Tests(unittest.TestCase):
    def test_rfc_example(self):
        original={"title":"Goodbye!","author":{"givenName":"John","familyName":"Doe"},"tags":["example","sample"]}
        patch={"title":"Hello!","author":{"familyName":None},"tags":["example"]}
        output=merge_patch(original,patch)
        self.assertEqual(output["author"],{"givenName":"John"})
        self.assertEqual(original["author"]["familyName"],"Doe")
    def test_scalar_replacement(self):
        self.assertEqual(merge_patch({"x":1},[1,2]),[1,2])
        self.assertEqual(merge_patch([1],{"a":2}),{"a":2})
    def test_deletion(self):
        self.assertEqual(apply_json('{"a":1}', '{"a":null}'),"{}")
if __name__ == "__main__": unittest.main()
