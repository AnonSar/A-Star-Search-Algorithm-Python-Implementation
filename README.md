# A-Star-Search-Algorithm-Python-Implementation
This is the A Star Search Algorithm Python Implementation. 

Important Details:

 1. For the heuristic, Euclidean distance have been used to get an estimate from the given node to the goal node.
 
 2. In order to address the ties (nodes having the same F value in our (discovered) heap, then we prefer using that node whihc are closer to the goal node i.e. node having higher H value.)
 
 3. If the source/target node happens to be such a node which is not walkable, then the algorithm will return an empty path with a total cost of 0.
 
 4. This particular implementation will only work for 2D maps.
 
 5. In order to get more test cases, please refer to https://www.movingai.com/benchmarks/grids.html
