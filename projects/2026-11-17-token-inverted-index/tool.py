"""Small positional inverted index for Unicode word search."""
import re
from collections import defaultdict

def tokenize(text):
    return re.findall(r"[^\\W_]+", text.casefold(), flags=re.UNICODE)

class Index:
    def __init__(self):
        self.docs = {}
        self.postings = defaultdict(dict)

    def remove(self, doc_id):
        if doc_id not in self.docs:
            raise KeyError(doc_id)
        del self.docs[doc_id]
        for term in list(self.postings):
            self.postings[term].pop(doc_id, None)
            if not self.postings[term]:
                del self.postings[term]

    def put(self, doc_id, text):
        if doc_id in self.docs:
            self.remove(doc_id)
        tokens = tokenize(text)
        self.docs[doc_id] = tokens
        positions = defaultdict(list)
        for i, token in enumerate(tokens):
            positions[token].append(i)
        for term, indices in positions.items():
            self.postings[term][doc_id] = indices

    def search_all(self, query):
        terms = tokenize(query)
        if not terms:
            return []
        matches = set(self.postings.get(terms[0], {}))
        for term in terms[1:]:
            matches &= set(self.postings.get(term, {}))
        return sorted(matches, key=str)

    def phrase(self, query):
        terms = tokenize(query)
        if not terms:
            return []
        result = []
        for doc in self.search_all(query):
            first = self.postings[terms[0]][doc]
            if any(all(start + offset in self.postings[term][doc]
                       for offset, term in enumerate(terms[1:], 1))
                   for start in first):
                result.append(doc)
        return result

if __name__ == "__main__":
    idx = Index()
    idx.put("a", "Blue ocean blue sky")
    idx.put("b", "Ocean blue")
    print(idx.phrase("blue ocean"))
