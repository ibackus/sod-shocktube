#!/bin/bash
export PYTHONPATH="src/:tests/:$PYTHONPATH"

KEEP_FIGURES_OPEN=false MPLBACKEND=tkagg python2 tests/exactRiemann.py
if [[ "$?" -eq "0" ]]; then
  echo "Example script passed successfully"
else
  echo "Example script failed"
  exit 1
fi


python -c "import sodtest; sodtest.run_test()"
if [[ "$?" -eq "0" ]]; then
  echo "Tests passed"
else
  echo "Tests failed"
  exit 1
fi
