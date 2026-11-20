# Reference Counting in CPython

COMP 211 Checkoff 3, Vivek Indlamuri

Topic: Garbage Collection, Reference Counting (Python)

Slides: [slides/reference-counting-cpython-slides.pdf](slides/reference-counting-cpython-slides.pdf) | Code: examples folder

## Overview

In C, every malloc needs a matching free, and getting the timing wrong breaks your program. Python never asks you to call free, yet the memory still gets released. I chose this topic because I wanted to know how CPython handles that, and since CPython is written in C, the answer builds directly on what we covered in COMP 211.

## What I Explored

Every CPython object is a C struct whose first field, `ob_refcnt`, counts how many pointers to it exist. Python variables are just pointers, so `b = a` copies the pointer rather than the object. The count goes up when a new reference appears and down when one goes away. Once it reaches zero, CPython frees the object immediately.

## What I Found Interesting

Freeing happens on the exact line where the count hits zero. I expected garbage collection to run at some later point, but `01_refcount_trace.py` shows the destructor running before the next line starts.

Moreover, `del` is not the same as free. It only removes one name, so the object survives if anything else still points to it (`02_del_is_not_free.py`).

However, reference counting cannot handle cycles. If A and B point to each other, both counts stay at 1 forever. The `gc` module exists mainly to clean these up, and `03_cycles_and_gc.py` shows a cycle staying in memory until `gc.collect()` runs.

Furthermore, an object that never gets freed usually has a reference you forgot about. A saved exception, for example, keeps its stack frames and their local variables alive (`04_hidden_references.py`).

Finally, this convenience has a cost. Updating counts on nearly every pointer copy adds overhead that C avoids, and making those updates thread-safe is a major reason Python has the GIL.

## Running the code

You need Python 3.12 or newer and gcc. Run these from the top folder of the repo:

```bash
python3 code/python/01_refcount_trace.py
python3 code/python/02_del_is_not_free.py
python3 code/python/03_cycles_and_gc.py
python3 code/python/04_hidden_references.py
python3 code/python/05_peek_at_ob_refcnt.py

gcc -Wall -Wextra -Wpedantic -fsanitize=address -g code/c/mini_refcount.c -o mini_refcount
./mini_refcount
```

`mini_refcount.c` is a small version of what CPython does internally. `incref` and `decref` change the count, and `decref` calls free once the count reaches 0. It follows the same steps as `01_refcount_trace.py`, so you can compare the output of the two. `05_peek_at_ob_refcnt.py` only works on regular CPython because it reads interpreter memory directly.

## Takeaway

Every object in CPython keeps a count, and it gets freed as soon as that count reaches zero. `del` only removes one reference, and the `gc` module is there to clean up cycles that counting misses.

## Resources

- Python C API, Reference Counting: https://docs.python.org/3/c-api/refcounting.html
- Python C API, Common Object Structures: https://docs.python.org/3/c-api/structures.html
- sys.getrefcount: https://docs.python.org/3/library/sys.html#sys.getrefcount
- gc module: https://docs.python.org/3/library/gc.html
- weakref module: https://docs.python.org/3/library/weakref.html
- The except clause: https://docs.python.org/3/reference/compound_stmts.html#except-clause
- CPython source, Include/object.h: https://github.com/python/cpython/blob/main/Include/object.h
- CPython garbage collector design notes: https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md
- PEP 683, Immortal Objects: https://peps.python.org/pep-0683/
- PEP 703, Making the GIL Optional: https://peps.python.org/pep-0703/
- Real Python, Memory Management in Python: https://realpython.com/python-memory-management/