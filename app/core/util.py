import re

_underscorer1 = re.compile(r"(.)([A-Z][a-z]+)")
_underscorer2 = re.compile("([a-z0-9])([A-Z])")


def camelize(s: str) -> str:
    words = s.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def camel_to_snake(s):
    subbed = _underscorer1.sub(r"\1_\2", s)
    return _underscorer2.sub(r"\1_\2", subbed).lower()
