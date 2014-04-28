Campusrocks uses the Sun Grid Engine (http://gridscheduler.sourceforge.net/howto/GridEngineHowto.html) to submit jobs. The central idea is that you ssh into a control node and on control nodes you deploy work to any number of compute nodes. You check on the progress of computation from the control node, and consolidate your results there too.

In general, the intensive computing should be done on the compute nodes.

To do this, you use the shell command qsub, which puts a job on the compute queue. qsub only works with shell scripts, which means that one has to write a shell script for any useful program. In addition, remember that qsub puts one job on the queue, not all of your work. It is your responsibility for breaking your work up into distinct pieces and calling each of them. 

This means that one needs three programs:

* the actual `useful' program [explorer2.py]

* the shell script wrapper [putQ.sh]

* the program that splits up your task into several calls [qsubCall.py]

In brackets, I've given you pointers to scripts I have used on this data to extract usernames. The code in question is in explorer2.py, and you can see how I break things up by checking out the Work/LM/qsubScripts/ directory. Basically, it's about sending a set of forum thread ids to explorer2.py internal to each qsub call. qsubCall looks at what slice I want, breaks it down by some divisor, and farms out each block to the shell script, which reads the start and ends as command line args. These are then passed into explorer2, which enters then as offsets in the id parameter of examineAllPosts.

In short, you should just have to change the code to explorer2 and everything will work.

Two caveats:

1) Environment! The compute nodes are not the control nodes, so things might be a bit wonky. Always use full paths, including for normal programs. There are environment variables you may have to set (I don't think so, but whatever), and those can be done in a profile file (as I provided). Using -v with qsub says to run the login script.

2) Think about where your output is going. You'll need to have a bunch of output files. They have to go somewhere, and that directory has to be created.

You'll need the data there. Feel free to use /campusdata/panand/dialog/persuasion/data/fourforums.

Enjoy!

You can, if you want to do some sanity checking, use the SRI LM toolkit. A good tutorial on this is here:
http://www.cs.brandeis.edu/~cs114/CS114_docs/SRILM_Tutorial_20080512.pdf
