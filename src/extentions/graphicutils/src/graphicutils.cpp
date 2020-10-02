#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "g_utils_functions.h"

/*
 * Implements an example function.
 */
PyDoc_STRVAR(graphicutils_draw_circle_doc, "draw_circle(x, y, r, vertices, mode)");
PyDoc_STRVAR(graphicutils_draw_grid_doc, "draw_grid(width, height, cam_x, cam_y, size");
PyDoc_STRVAR(graphicutils_draw_arrow_doc, "draw_arrow(x, y, w, h)");
PyDoc_STRVAR(graphicutils_draw_rounded_rect_doc, "draw_rounded_rect(x, y, w, h, border_radius, mode)");
PyDoc_STRVAR(graphicutils_draw_rect_doc, "draw_rect(x, y, w, h, mode)");

PyObject* graphicutils_draw_circle(PyObject *self, PyObject *args) {
    int x;
    int y;
    int r;
    int vertices;
    int mode;
 
    if (!PyArg_ParseTuple(args, "iiiii", &x, &y, &r, &vertices, &mode)) {
        return NULL;
    }
    
    draw_circle(x, y, r, vertices, mode);
    Py_RETURN_NONE;
}

PyObject* graphicutils_draw_grid(PyObject* self, PyObject* args) {
    int width;
    int height;
    int cam_x;
    int cam_y;
    int size;
    int pos_x;
    int pos_y;

    if (!PyArg_ParseTuple(args, "iiiiiii", &width, &height, &cam_x, &cam_y, &size, &pos_x, &pos_y)) {
        return NULL;
    }

    draw_grid(width, height, cam_x, cam_y, size, pos_x, pos_y);
    Py_RETURN_NONE;
}

PyObject* graphicutils_draw_arrow(PyObject* self, PyObject* args) {
    int x;
    int y;
    int w;
    int h;
    
    if (!PyArg_ParseTuple(args, "iiii", &x, &y, &w, &h)) {
        return NULL;
    }
    
    draw_arrow(x, y, w, h);
    Py_RETURN_NONE;
}

PyObject* graphicutils_draw_rounded_rect(PyObject* self, PyObject* args) {
    int x;
    int y;
    int w;
    int h;
    int border_radius;
    int mode;

    if (!PyArg_ParseTuple(args, "iiiiii", &x, &y, &w, &h, &border_radius, &mode)) {
        return NULL;
    }
    
    draw_rounded_rect(x, y, w, h, border_radius, mode);
    Py_RETURN_NONE;
}

PyObject* graphicutils_draw_rect(PyObject* self, PyObject* args) {
    int x;
    int y;
    int w;
    int h;
    int mode;

    if (!PyArg_ParseTuple(args, "iiiii", &x, &y, &w, &h, &mode)) {
        return NULL;
    }

    draw_rect(x, y, w, h, mode);
    Py_RETURN_NONE;
}

/*
 * List of functions to add to graphicutils in exec_graphicutils().
 */
static PyMethodDef graphicutils_functions[] = {
    { "draw_circle", (PyCFunction)graphicutils_draw_circle, METH_VARARGS, graphicutils_draw_circle_doc },
    { "draw_grid", (PyCFunction)graphicutils_draw_grid, METH_VARARGS, graphicutils_draw_grid_doc},
    { "draw_arrow", (PyCFunction)graphicutils_draw_arrow, METH_VARARGS, graphicutils_draw_arrow_doc},
    { "draw_rounded_rect", (PyCFunction)graphicutils_draw_rounded_rect, METH_VARARGS, graphicutils_draw_rounded_rect_doc},
    { "draw_rect", (PyCFunction)graphicutils_draw_rect, METH_VARARGS, graphicutils_draw_rect_doc},
    { NULL, NULL, 0, NULL } /* marks end of array */
};


/*
 * Initialize graphicutils. May be called multiple times, so avoid
 * using static state.
 */
int exec_graphicutils(PyObject *module) {
    PyModule_AddFunctions(module, graphicutils_functions);
    PyModule_AddStringConstant(module, "__author__", "Thiago");
    PyModule_AddStringConstant(module, "__version__", "1.0.0");

    return 0; /* success */
}

/*
 * Documentation for graphicutils.
 */

PyDoc_STRVAR(graphicutils_doc, "The graphicutils module");

/*
static PyModuleDef graphicutils_slots[] = {
    { Py_mod_exec, exec_graphicutils },
    { 0, NULL }
};
*/

/*

// Module definition
// The arguments of this structure tell Python what to call your extension,
// what it's methods are and where to look for it's method definitions
static struct PyModuleDef hello_definition = { 
    PyModuleDef_HEAD_INIT,
    "hello",
    "A Python module that prints 'hello world' from C code.",
    -1, 
    hello_methods
};
*/

static struct PyModuleDef graphicutils_def = {
    PyModuleDef_HEAD_INIT,
    "graphicutils",
    graphicutils_doc,
    0,              /* m_size */
    graphicutils_functions,           /* m_methods */
    NULL,           // graphicutils_slots,
    NULL,           /* m_traverse */
    NULL,           /* m_clear */
    NULL,           /* m_free */
};

PyMODINIT_FUNC PyInit_graphicutils() {
    return PyModuleDef_Init(&graphicutils_def);
}
