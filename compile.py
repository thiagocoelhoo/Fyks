from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("main",  ["src/main.py"]),
]

setup(
    name = 'Fyks',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)