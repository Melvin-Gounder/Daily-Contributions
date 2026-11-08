from ipaddress import IPv4Address, IPv4Network
class Policy:
    """First-match ordered IPv4 allow/deny rules; default deny."""
    def __init__(self, rules, default="deny"):
        if default not in ("allow","deny"): raise ValueError("invalid default")
        self.rules=[]
        for action,cidr in rules:
            if action not in ("allow","deny"): raise ValueError("invalid action")
            self.rules.append((action,IPv4Network(cidr,strict=True)))
        self.default=default
    def check(self,address):
        ip=IPv4Address(address)
        for index,(action,network) in enumerate(self.rules,1):
            if ip in network: return action=="allow",f"rule {index}: {action} {network}"
        return self.default=="allow",f"default: {self.default}"
if __name__=="__main__":
    p=Policy([("deny","10.0.0.0/24"),("allow","10.0.0.0/8")])
    for ip in ("10.0.0.5","10.2.3.4","8.8.8.8"): print(ip,p.check(ip))
