def is_aldecimal(s: str) -> bool:
    return all(c.isdecimal() or c.isalpha() for c in s)
