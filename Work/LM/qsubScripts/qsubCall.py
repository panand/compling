import os

per = 118
max = 17500
num = max/per+2
for x in range(num):
    os.system("qsub -v start=%d,end=%d -e /campusdata/panand/dialog/persuasion/code/indepStudy/errors/ -o /campusdata/panand/dialog/persuasion/code/indepStudy/out /campusdata/panand/dialog/persuasion/code/indepStudy/putQ.sh" % (x*per, (x+1)*per-1))

