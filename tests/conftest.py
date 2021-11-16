import os
import sys

_MYDIR = os.path.realpath(os.path.dirname(__file__))
_SRC_DIR = os.path.realpath(os.path.join(_MYDIR, '..', 'src'))
sys.path.insert(0, _SRC_DIR)

os.chdir(_MYDIR)
