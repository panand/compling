#!/bin/tcsh
# use:
# qsub -v start=n,end=m [-e /path/to/stderrs | -o /path/to/stdouts] putQ.sh

/share/apps/epd/bin/python2.7 /campusdata/panand/dialog/persuasion/code/indepStudy/explorer2.py $start $end
