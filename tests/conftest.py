import os
import sys

_MYDIR = os.path.realpath(os.path.dirname(__file__))
_SRC_DIR = os.path.realpath(os.path.join(_MYDIR, '..', 'src'))
_EXAMPLE_DIR = os.path.realpath(os.path.join(_MYDIR, '..', 'examples'))
sys.path.insert(0, _SRC_DIR)
sys.path.insert(0, _EXAMPLE_DIR)

os.chdir(_MYDIR)
