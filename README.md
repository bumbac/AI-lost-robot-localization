# Robot localization problem 
##BI-ZUM semestral project on CTU FIT Prague

This projects demonstrates localization of robot lost in 2D space.
Map of location is known for robot and he tries to locate himself by recognizing his surroundings. 
Robot has wall detectors in four directions and moves by one tile in four directions.

**Starting**

    python3 localize.py <map name> <print option> <# of iterations>
*Printing option* is optional and on by default, type *-np* to suppress additional text output.

*Maps* are stored in ./dataset

After all iterations are completed program provides basic statistics (mean, median).


This algorithm is based on Hidden Markov model of probability.
In each step robot senses his surroundings and evaluates all tiles on map according to their surroundings.

After that a tile with highest probability is chosed and robot moves to (random) free adjacent tile (v2).
This prevents the robot from moving to wall and wasting one step and still providing random movement.
     
