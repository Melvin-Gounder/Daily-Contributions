"""Decode 4-byte big-endian length-prefixed binary frames incrementally."""
import struct

class FrameError(ValueError):
    pass

class Decoder:
    def __init__(self, max_payload=1024*1024):
        if not 0 <= max_payload <= 0xffffffff:
            raise ValueError("invalid max payload")
        self.max_payload = max_payload
        self.buffer = bytearray()
        self.expected = None

    def feed(self, chunk):
        self.buffer.extend(chunk)
        frames = []
        while True:
            if self.expected is None:
                if len(self.buffer) < 4:
                    break
                self.expected = struct.unpack(">I", self.buffer[:4])[0]
                del self.buffer[:4]
                if self.expected > self.max_payload:
                    self.buffer.clear()
                    self.expected = None
                    raise FrameError("declared frame exceeds configured maximum")
            if len(self.buffer) < self.expected:
                break
            frames.append(bytes(self.buffer[:self.expected]))
            del self.buffer[:self.expected]
            self.expected = None
        return frames

    def finish(self):
        if self.expected is not None or self.buffer:
            raise FrameError("truncated frame at EOF")

def encode(payload):
    if len(payload) > 0xffffffff:
        raise ValueError("payload too large")
    return struct.pack(">I", len(payload)) + payload

if __name__ == "__main__":
    decoder = Decoder()
    print(decoder.feed(encode(b"hello") + encode(b"world")))
