# Streaming Base64 Encoder and Decoder

Chunk-safe binary Base64 encoding/decoding with strict validation and file-based CLI.

## Usage

Python 3.9+, standard library only. Run `python -m unittest -v test_tool.py` for tests. Run `python tool.py encode input.bin output.b64` or `python tool.py decode output.b64 recovered.bin`.

## Design and limitations

Uses bounded chunks, preserving Base64 3-byte/4-character boundaries. Encoding and decoding are O(n) time and O(chunk_size) memory. Decoder accepts strict Base64 with no whitespace. CLI writes destination directly; use a temporary output path when processing untrusted input to avoid leaving partial results.
