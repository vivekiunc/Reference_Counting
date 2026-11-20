/*
 * Simple reference counting in C, similar to Py_INCREF / Py_DECREF.
 * Same steps as 01_refcount_trace.py.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    long refcnt;      
    char name[16];      
} Obj;

Obj *obj_new(const char *name) {
    Obj *o = malloc(sizeof(Obj));
    if (o == NULL) {
        perror("malloc");
        exit(1);
    }
    o->refcnt = 1;     
    strncpy(o->name, name, sizeof(o->name) - 1);
    o->name[sizeof(o->name) - 1] = '\0';
    return o;
}

void incref(Obj *o) {
    o->refcnt++;
}

void decref(Obj *o) {
    o->refcnt--;
    if (o->refcnt == 0) {
        printf("  -> %s freed\n", o->name);
        free(o);      
    }
}

void peek(Obj *n) {
    incref(n);          
    printf("%-16s refcount = %ld\n", "inside peek(x)", n->refcnt);
    decref(n);        
}

int main(void) {
    Obj *x = obj_new("A");
    printf("%-16s refcount = %ld\n", "x = new(\"A\")", x->refcnt);

    Obj *y = x;  incref(y);
    printf("%-16s refcount = %ld\n", "y = x", x->refcnt);

    Obj *box[1] = { x };  incref(box[0]);
    printf("%-16s refcount = %ld\n", "box = [x]", x->refcnt);

    peek(x);
    printf("%-16s refcount = %ld\n", "peek returns", x->refcnt);

    decref(y);  y = NULL;
    printf("%-16s refcount = %ld\n", "del y", x->refcnt);

    decref(box[0]);  box[0] = NULL;
    printf("%-16s refcount = %ld\n", "box.clear()", x->refcnt);

    printf("x = None         (count drops to 0)\n");
    decref(x);  x = NULL;

    printf("no leaks, no double free: run with -fsanitize=address to check\n");
    return 0;
}