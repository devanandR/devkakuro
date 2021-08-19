# About: 
Playing Kakuro game is addictive and satisfying. 
Computationally this problem is not easy-belongs to the NP class. 

I am enjoying writing some tricky solving techniques for Kakuro
 
I have started with the branch-and-bound-based (BnB) method with some basic branching rules. 
The branching rules used are from my intuition. There could be many (similar and different) 
branching (or search) strategies used to solve Kakuro, which I am yet to explore.    


# devkakuro
# 1) To solve a given Kakuro problem: 
     just hit "python devkakuro.py problem file"
     
     Even if you just hit "python devkakuro.py" 
     it will take a default problem file, "testFile1.txt" available in the repository.
     After that, you will be provided with choices of solving methods to select. 
     Your appropriate input will result in the solution of the problem and 
     the time it takes to solve using the selected method.
  # NOTE: 
      Plz comment "import kakuroOptModel as cplexmodeling" in solvingKakuromethods.py if you do not have cplex optimization engine installed
  
# 2) Pattern example in the input file: here is the example input : 
     "#,5\#,19\#,#"
     "#\13,0,0,4\#"
     "#\12,0,0,0"
     "#,#\3,0,0"        
     
    In the pattern 0 is the block which is required to be filled,
    "#\13" for example, says that the horizontal word just right to this block should add up to 13
    "19\#" for example, says that the vertical word just  below this block should add up to 19

# 3) Methods used: There are three generic methods are being tried in the algo 
      1) branch and bound
           - there are different types of techniques used to solve kakuro using the concept of 
            branch and bound method as per the branching selection rule (that is search method).
             1) lexicographic: At each node from root to leaf in the branch and bound tree, we 
                select the block to branch in a lexicographic manner. For the sample example shown above, 
                first, the block position at (1,1) (just right to the block "#\13") will be chosen to 
                fill first, then (1,2) then (2,2) so on and so forth
             2) random: At each node, the selection of block to fill the appropriate values 
                 is random. For sample example, we can start from any empty 
                 block and after filling an appropriate value, we can again choose the block randomly 
             3) most-constrained grid (or block) first: This branching rule prefers block with the most 
                 constrained value to fill. For the above sample example, branching starts from (3,3) 
                 as it has the most constrained values to fill (i.e., 1,2,3) 
             4) smallest-sized word first: This branching rule prefers blocks filling lexicographically that
                belong to the least sized word. In the example sample shown above, branching starts from (3,3) 
                as it belongs to the word with size 2,2 (vertical word size:2 and the corresponding horizontal word size:2)   
      
      2) integer programming mathematical formulation based
           - It is under progress, One of the methods is implemented but currently it is not handling 
             uniqueness property of kakuro game
      
      3) constrained-satisfaction-problem-based (CSP) method
           -CSP techniques are highly used for solving the Kakuro game as Kakuro game is formally a CSP problem.
           -I am in progress to use one of the CSPs. Yet to complete, yet to push the codes to Github
      
       ##### python version: Python 3.8 #####
   ### Branch and Bound procedure used: 
     "Kakuro Solving Process": The solving process is generic for any branching-specific branch and bound methods summarized above. 
     It starts with the given initial problem. It is called the root of the tree. At the root node, we have many empty blocks 
     to fill with their specific possible values. We can pick one of them to start solving the problem. Because we have multiple 
     choices for this block, we choose them one by one. The selection of block (or grid) is called a branching procedure. 
     The state of the problem after updating the block is now called a new node.  
     We keep following the same procedure until we reach the leaf of the tree. Note that for the Kakuro problem we have 
     a single feasible solution, so the branch and bound generated will have only one leaf with maximum depth. 
     The remaining leaves are placed with depths less than the maximum depth as their respective state becomes infeasible 
      and, B&B has to traverse back to find the other feasible paths.    
