# Tracks one object's reference count as references are added and removed.
# sys.getrefcount shows one extra (the argument itself), so I subtract 1.

import sys


class Node:
    def __init__(self, name):
        self.name = name

    def __del__(self):
        print(f"  -> {self.name} freed")


def peek(n):
    print(f"{'inside peek(x)':<16} refcount = {sys.getrefcount(n) - 1}")


x = Node("A")
print(f"{'x = Node(\"A\")':<16} refcount = {sys.getrefcount(x) - 1}")

y = x
print(f"{'y = x':<16} refcount = {sys.getrefcount(x) - 1}")

box = [x]
print(f"{'box = [x]':<16} refcount = {sys.getrefcount(x) - 1}")

peek(x)
print(f"{'peek returns':<16} refcount = {sys.getrefcount(x) - 1}")

del y
print(f"{'del y':<16} refcount = {sys.getrefcount(x) - 1}")

box.clear()
print(f"{'box.clear()':<16} refcount = {sys.getrefcount(x) - 1}")

print("x = None         (count drops to 0)")
x = None
print("this prints after A is freed")