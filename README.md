# Unidirectional-&-Bidirectional-A-Star-Search-Algorithm-Python-Implementation

This is the Unidirectional and Bidirectional A Star Search Algorithm Python Implementation. 

Important Details (Unidirectional A star search Algorithm):

 1. For the heuristic, Euclidean distance/octile have been used to get an estimate from the given node to the goal node.
 
 2. In order to address the ties (nodes having the same F value in our (discovered) heap, then we prefer using that node whihc are closer to the goal node i.e. node having higher H value.)
 
 Important Details (Bidirectional A star search Algorithm):
 
  1. For the heuristic, Euclidean distance/octile have been used to get an estimate from the given node to the goal node.
  
  2. The node selction policy that is being used here is : we select that frontier which offers us the node with minimum f-value.
  
  3. The stopping condition that is being used here is: we stop as soon as we come across such a node from either of the frontiers, that happens to be in the closed list of the opposite frontier.
  
  
 NOTE: 
 
 1. If the source/target node happens to be such a node which is not walkable, then the algorithm will return an empty path with a total cost of 0.
 
 2. This particular implementation will only work for 2D maps.
 
 3. In order to get more test cases, please refer to https://www.movingai.com/benchmarks/grids.html
 
