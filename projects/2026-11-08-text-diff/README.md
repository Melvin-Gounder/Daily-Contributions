# LCS Line Diff

A line-oriented diff based on longest common subsequence (LCS). Emits ` ` for unchanged lines, `-` for deletions, and `+` for insertions. `apply` checks and replays an edit script against its original input.

Run `python line_diff.py before.txt after.txt`; test with `python -m unittest -v test_line_diff.py`. Python standard library only.

The dynamic-programming table stores the LCS length for each pair of suffixes. Equal-score alternatives prefer deletions, making the result deterministic. Time and memory are O(nm) for n and m input lines. This teaching implementation is not unified-diff compatible and is unsuitable for huge files; Myers' algorithm is preferable there.
