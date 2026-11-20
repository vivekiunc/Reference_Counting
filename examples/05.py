# id(obj) is the object's address in CPython, and ob_refcnt is the first
# field of the struct, so ctypes can read it like *(ssize_t *)addr in C.
# Only works on CPython.

import ctypes
import sys

if sys.implementation.name != "cpython":
    sys.exit("This demo only works on CPython.")
if hasattr(sys, "_is_gil_enabled") and not sys._is_gil_enabled():
    sys.exit("Free-threaded builds use a split refcount; run on a normal build.")


def raw_refcnt(address):
    return ctypes.c_ssize_t.from_address(address).value


data = [1, 2, 3]
addr = id(data)
print(f"list lives at address {hex(addr)}")
print(f"ob_refcnt read from memory: {raw_refcnt(addr)}")

alias = data
print(f"after alias = data:         {raw_refcnt(addr)}")

container = [data, data]
print(f"after container = [data, data]: {raw_refcnt(addr)}")

del alias, container
print(f"after del alias, container: {raw_refcnt(addr)}")

print()
print("Immortal objects (Python 3.12+): small ints, None, True never get freed")
print(f"ob_refcnt of None looks like: {raw_refcnt(id(None))}")
print("That huge number is a marker meaning 'never free this', not a real count.")