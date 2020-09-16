import sys
import importlib

if sys.platform == "win32":
    import graphicutils
else:
    from .unix import graphicutils