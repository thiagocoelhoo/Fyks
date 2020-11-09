import os
from distutils.core import setup, Extension

module = Extension(
    name="graphicutils",
    sources=["src/graphicutils.cpp", "src/g_utils_functions.cpp"],
    include_dirs=[os.getcwd() + "/include/"],
    library_dirs=[os.getcwd() + "/lib"],
    libraries=["glut", "GL"],
)

setup(
    name="graphicutils",
    version="1.0",
    description="Utils functions",
    ext_modules=[module],
)
