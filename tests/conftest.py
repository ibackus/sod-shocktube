import os
os.environ['KEEP_FIGURES_OPEN'] = 'false'
import sys
import platform
from packaging import version

if version.parse(platform.python_version()) < version.parse('3.6.0'):
    os.environ['MPLBACKEND'] = 'tkagg'


_MYDIR = os.path.realpath(os.path.dirname(__file__))
_SRC_DIR = os.path.realpath(os.path.join(_MYDIR, '..', 'src'))
_EXAMPLE_DIR = os.path.realpath(os.path.join(_MYDIR, '..', 'examples'))
sys.path.insert(0, _EXAMPLE_DIR)

os.chdir(_MYDIR)
