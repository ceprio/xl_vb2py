import os
import sys

# << Utilities >>
def rootPath():
    """Return the root path"""
    return os.path.split(os.path.abspath(__file__))[0]


def relativePath(*paths):
    """Return the path to a file"""
    return os.path.join(rootPath(), *paths)
# -- end -- << Utilities >>
