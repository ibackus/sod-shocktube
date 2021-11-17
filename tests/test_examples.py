import runpy
import pytest
import os
import glob

_MYDIR = os.path.realpath(os.path.dirname(__file__))
_EXAMPLE_DIR = os.path.realpath(os.path.join(_MYDIR, '..', 'examples'))
scripts = sorted(glob.glob(os.path.join(_EXAMPLE_DIR, '*.py')))


@pytest.mark.parametrize('script', scripts)
def test_script_execution(script):
    runpy.run_path(script)
