#python navig.py

Algorithm implemented: Q-Learning



Summary:

The code is divided into 3 sections:

1. Environment
2. Navigation
3. GUI

Environment: Contains the environment variables, and functions to mutate them. The main function setup_env() sets up the road map for RL to initiate.

Navigation: This is the main section of the code where the map traversal and reinforcement takes place. A free agent traverses the map, while updating the Q-matrix, following the updation policy.

GUI: The GUI implementation of the road map using Tkinter. The GUI is also animated manually to show the learning process.




Input: The Source, Destination and the 'To Avoid' nodes/junctions.
	(Optional) Input the traffic values.

Output: The optimal path, given the input conditions.


Note: The map is immutable in this version.


