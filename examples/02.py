# del removes a name, not the object. The object is only freed
# when the last reference is gone.
# 

import sys


class Big:
    def __init__(self, label):
        self.label = label

    def __del__(self):
        print(f"  -> {self.label} freed")


print("Case 1: two names, del one of them")
a = Big("obj1")
b = a
print(f"  refcount before del = {sys.getrefcount(a) - 1}")
del a
print(f"  after del a, refcount = {sys.getrefcount(b) - 1}  (still alive, b points to it)")
print(f"  b.label is still readable: {b.label}")
del b  
print()

print("Case 2: the object is also inside a list")
c = Big("obj2")
holder = [c]
del c
print("  del c done, but nothing was freed because holder[0] still points to it")
holder.pop()  
print()

print("Case 3: del on the only name frees immediately")
d = Big("obj3")
del d
print("  this line prints after obj3 was freed")