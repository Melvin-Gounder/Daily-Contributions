"""Internet checksum (RFC 1071), network byte order."""
def checksum(data):
    if not isinstance(data,(bytes,bytearray)): raise TypeError("bytes required")
    if len(data)%2: data=bytes(data)+b"\x00"
    total=sum((data[i]<<8)|data[i+1] for i in range(0,len(data),2))
    while total>>16: total=(total&0xffff)+(total>>16)
    return (~total)&0xffff
def verify(data): return checksum(data)==0
if __name__=="__main__":
    print(hex(checksum(b"hello world")))
