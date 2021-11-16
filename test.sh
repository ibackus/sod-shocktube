#!/bin/bash
export PYTHONPATH="src/:tests/:$PYTHONPATH"

KEEP_FIGURES_OPEN=false MPLBACKEND=tkagg python2 examples/exactRiemann.py
if [[ "$?" -eq "0" ]]; then
  echo "Example script passed successfully"
else
  echo "Example script failed"
  exit 1
fi

pytest -vvs tests/
