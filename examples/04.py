# A saved exception keeps its traceback, which keeps the stack frames,
# which keep their local variables alive.

import sys
import gc


class Big:
    def __init__(self, label):
        self.label = label

    def __del__(self):
        print(f"  -> {self.label} freed")


def fails():
    local_big = Big("local_big")  # a local variable in this frame
    raise ValueError("boom")


gc.disable()  # make sure only refcounting is at work

print("1) Saving the exception keeps every local in the failing frame alive")
try:
    fails()
except ValueError as e:
    saved = e  # e.__traceback__ -> frame -> local_big
print("  left the except block, but local_big was NOT freed yet")
print("  dropping the saved exception and breaking the frame cycle:")
saved.__traceback__ = None
saved = None
print()

print("2) Python deletes the 'as e' name for you after the except block")
try:
    fails()
except ValueError as e:
    pass
print(f"  is 'e' still defined? {'e' in dir()}")
print("  (CPython does this on purpose so the frame does not stay alive)")

gc.enable()
gc.collect()