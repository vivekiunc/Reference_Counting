# Reference counting can't free a cycle (A -> B -> A).
# The gc module cleans these up, and weakref avoids making the cycle.

import gc
import weakref


class Node:
    def __init__(self, name):
        self.name = name
        self.other = None

    def __del__(self):
        print(f"  -> {self.name} freed")


gc.disable()  

print("1) No cycle, gc disabled: still freed immediately by refcounting")
solo = Node("solo")
solo = None
print()

print("2) Cycle A <-> B, gc disabled")
a, b = Node("A"), Node("B")
a.other, b.other = b, a
probe = weakref.ref(a)  
a = b = None
print(f"  names dropped. Is A still alive? {probe() is not None}  (leaked)")
print()

print("3) Run the cycle collector manually")
found = gc.collect()
print(f"  gc.collect() found {found} unreachable objects (A, B and internal objects they own)")
print(f"  Is A still alive? {probe() is not None}")
print()

print("4) The fix: make the back-pointer a weak reference")
parent = Node("parent")
child = Node("child")
parent.other = child                
child.other = weakref.ref(parent)    
parent = child = None              
print("  (no gc.collect needed)")

gc.enable()