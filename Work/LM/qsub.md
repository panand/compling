Campusrocks uses the Sun Grid Engine (http://gridscheduler.sourceforge.net/howto/GridEngineHowto.html) to submit jobs. The central idea is that you ssh into a control node and on control nodes you deploy work to any number of compute nodes. You check on the progress of computation from the control node, and consolidate your results there too.

In general, the intensive computing should be done on the compute nodes.

To do this, you use the shell command qsub, which 