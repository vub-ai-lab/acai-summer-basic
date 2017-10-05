This is a simple reference implementation of Q-Learning and the ICE environment in Java.

HOW TO COMPILE AND CREATE JAR:
You can open the files in Eclipse, Eclipse project files are provided.

You can compile + create a Jar with Ant:
ant jar

HOW TO RUN:
From Eclipse, 

Or using your Ant-built Jar:
java -jar dist/QLearning.jar > out.csv

HOW TO PLOT THE DATA:
The program runs Q-learning for 10000 episodes and prints statistics for 
each episode to CSV format, which you can pipe to a file, as show above.
The contents of this CSV can be visualized ...
    -> TODO
