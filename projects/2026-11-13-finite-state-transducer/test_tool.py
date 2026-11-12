import unittest
from tool import Normalizer,normalize
class Tests(unittest.TestCase):
    def test_spaces(self): self.assertEqual(normalize("  hello   world  "),"hello world")
    def test_punctuation(self): self.assertEqual(normalize("Hello  , world !"),"Hello, world!")
    def test_chunks(self):
        text="  hello \n world  ,  again  "
        n=Normalizer();output="".join(n.feed(text[i:i+2]) for i in range(0,len(text),2))+n.finish()
        self.assertEqual(output,normalize(text))
    def test_empty(self): self.assertEqual(normalize(" \n "),"")
if __name__=="__main__": unittest.main()
