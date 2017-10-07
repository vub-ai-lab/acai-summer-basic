This is a simple reference implementation of Q-Learning and the ICE environment in Python.

The environment is a reimplementation of the one in code/, but much simpler and less feature-full, so that it is easier to understand.

HOW TO RUN:

Simply run "python3 main.py" and see that the agent learns.

In order to produce nice plots, do:

	python3 main.py > /tmp/out

Then, execute gnuplot:

	gnuplot
	> plot "/tmp/out" using 12 with lines
