#!/bin/bash
KEEP_FIGURES_OPEN=false MPLBACKEND=tkagg python2 exactRiemann.py
if [[ "$?" -eq "0" ]]; then
  echo "Test passed successfully"
else
  echo "Test failed"
  exit 1
fi
