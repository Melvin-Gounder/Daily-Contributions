import os
import re

PATTERN=re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::-([^}]*))?\}")

class ConfigurationError(ValueError): pass

def resolve(template,environment=None):
    """Resolve variable references without invoking a shell."""
    env=dict(os.environ if environment is None else environment)
    def expand(value,stack):
        if not isinstance(value,str): raise TypeError("values must be strings")
        def replace(match):
            key,default=match.groups()
            if key in stack: raise ConfigurationError("cycle: "+" -> ".join(stack+(key,)))
            raw=env.get(key)
            if raw is None or raw=="":
                if default is None: raise ConfigurationError("missing: "+key)
                raw=default
            return expand(raw,stack+(key,))
        return PATTERN.sub(replace,value)
    return expand(template,())

if __name__=="__main__":
    print(resolve("http://${HOST:-localhost}:${PORT:-8080}",{}))
