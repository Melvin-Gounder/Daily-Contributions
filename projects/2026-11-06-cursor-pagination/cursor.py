"""HMAC-SHA256 signed keyset pagination cursors."""
import base64,hashlib,hmac,json
class InvalidCursor(ValueError): pass
def b64(raw): return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
def unb64(text): return base64.b64decode(text+"="*(-len(text)%4),altchars=b"-_",validate=True)
def encode(last,secret):
 if type(last)!=int or last<0: raise ValueError("nonnegative integer ID required")
 if not isinstance(secret,bytes) or len(secret)<16: raise ValueError("secret too short")
 payload=json.dumps({"v":1,"after":last},separators=(",",":"),sort_keys=True).encode()
 return b64(payload)+"."+b64(hmac.new(secret,payload,hashlib.sha256).digest())
def decode(token,secret):
 try:
  if not isinstance(token,str) or len(token)>1024: raise InvalidCursor("invalid token")
  data,mac=token.split("."); payload=unb64(data); signature=unb64(mac)
  if not hmac.compare_digest(hmac.new(secret,payload,hashlib.sha256).digest(),signature): raise InvalidCursor("bad signature")
  obj=json.loads(payload)
  if type(obj)!=dict or obj.get("v")!=1 or type(obj.get("after"))!=int or obj["after"]<0: raise InvalidCursor("bad payload")
  return obj["after"]
 except (TypeError,ValueError,UnicodeDecodeError) as e: raise InvalidCursor("invalid cursor") from e
def page(items,size,secret,cursor=None):
 if type(size)!=int or not 1<=size<=100: raise ValueError("size must be 1..100")
 if any(type(k)!=int or k<0 for k,v in items): raise ValueError("invalid ID")
 if any(items[i][0]>=items[i+1][0] for i in range(len(items)-1)): raise ValueError("unsorted IDs")
 after=decode(cursor,secret) if cursor is not None else -1
 remaining=[item for item in items if item[0]>after]
 batch=remaining[:size]
 return batch,encode(batch[-1][0],secret) if len(remaining)>size else None
if __name__=="__main__":
 secret=b"example-only-not-production-key"
 items=[(i,str(i)) for i in range(9)]
 cursor=None
 while True:
  batch,cursor=page(items,3,secret,cursor); print(batch)
  if cursor is None: break
