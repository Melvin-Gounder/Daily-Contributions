import hashlib,hmac,time
class WebhookError(ValueError):pass
def signature(secret,timestamp,body):
    if not isinstance(secret,bytes) or not secret or not isinstance(body,bytes) or type(timestamp)!=int:raise ValueError("invalid signature input")
    return "sha256="+hmac.new(secret,str(timestamp).encode()+b"."+body,hashlib.sha256).hexdigest()
class Verifier:
    def __init__(self,secret,tolerance=300,clock=time.time):
        if not isinstance(secret,bytes) or not secret or type(tolerance)!=int or tolerance<0:raise ValueError("invalid settings")
        self.secret=secret;self.tolerance=tolerance;self.clock=clock;self.seen={}
    def verify(self,timestamp,body,supplied):
        if type(timestamp)!=int or not isinstance(body,bytes) or not isinstance(supplied,str):raise WebhookError("invalid fields")
        now=self.clock()
        if abs(now-timestamp)>self.tolerance:raise WebhookError("expired")
        if len(supplied)!=71 or not supplied.startswith("sha256="):raise WebhookError("invalid format")
        if not hmac.compare_digest(signature(self.secret,timestamp,body),supplied):raise WebhookError("invalid signature")
        self.seen={k:v for k,v in self.seen.items() if v>=now}
        if supplied in self.seen:raise WebhookError("replay")
        self.seen[supplied]=timestamp+self.tolerance
        return True
if __name__=="__main__":
    s=b"demo-only";b=b'{"event":"created"}';v=Verifier(s,clock=lambda:1000)
    print(v.verify(1000,b,signature(s,1000,b)))
