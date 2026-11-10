import unittest
from patch import apply,PatchError,parts
class TestPatch(unittest.TestCase):
    def test_array(self):
        original={"a":[1,3]}
        result=apply(original,[{"op":"add","path":"/a/1","value":2}])
        self.assertEqual(result,{"a":[1,2,3]})
        self.assertEqual(original,{"a":[1,3]})
    def test_escape(self): self.assertEqual(parts("/a~1b/~0"),["a/b","~"])
    def test_test_failure_atomic(self):
        original={"x":1}
        with self.assertRaises(PatchError):
            apply(original,[{"op":"replace","path":"/x","value":2},{"op":"test","path":"/x","value":1}])
        self.assertEqual(original,{"x":1})
    def test_remove(self):
        self.assertEqual(apply({"x":1},[{"op":"remove","path":"/x"}]),{})
    def test_invalid(self):
        with self.assertRaises(PatchError): parts("/~3")
if __name__=="__main__": unittest.main()
