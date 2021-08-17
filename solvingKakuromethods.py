#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 23:13:27 2021

@author: dev
"""
import random
import utility 
import copy
import time
import kakuroOptModel as cplexmodeling




def solveUsingLexicoGraphicBranch(VarInBoardToFill,KeyisFinallyUpdated,data): 
    
    global NewVar,depth,solvingFlag, GridToFill
    valueTriedSoFar ={}
    ## Choose vars one by one and randomly fill values
    #NewVar = copy.deepcopy(VarInBoardToFill)
    if solvingFlag =='m':
        GridToFill = utility.sortedKeyAsPerVal(VarInBoardToFill)
    if solvingFlag =='s':
        GridToFill = data.mapVarToWordLength
    if solvingFlag =='r':
        utility.shuffleElements(GridToFill)
    
    for key in GridToFill:   ### Always follow left to right
        if KeyisFinallyUpdated[key]:
            continue
        
        data.updateVarToFixVal(key, 0)
        i=1
        TempAccept = False
        breakFlag = False
        while not KeyisFinallyUpdated[key]: 
            
        
            if key in valueTriedSoFar:
                i = max(valueTriedSoFar[key])+1
                valueTriedSoFar[key].append(i)
            else:
                valueTriedSoFar[key] =[1]
        
            if min(9, data.Var[key]) < i:  ## Set upper bound 9
                return True
                #raise ValueError("Unable to assign some issue with code/problem...")
            TempAccept, NewVar = data.updateUB(key,i,VarInBoardToFill)
            
            if TempAccept:
                
                data.updateVarToFixVal(key, i)
                KeyisFinallyUpdated[key] = True
                VarInBoardToFill = NewVar
                depth = depth + 1 ## Going down the tree
                breakFlag = solveUsingLexicoGraphicBranch(VarInBoardToFill, KeyisFinallyUpdated,data)
                depth = depth - 1 ## Return back
                if not breakFlag:
                    KeyisFinallyUpdated[key] = True
                else:
                    KeyisFinallyUpdated[key] = False
                    data.updateVarToFixVal(key, 0)
            else:
                NewVar = copy.deepcopy(VarInBoardToFill)

    if depth == 0:    
        print("Final Solution is ",NewVar)
        
    

def solvingKakuro(file):
    
    global solvingFlag, NewVar, valueTriedSoFar, depth, GridToFill
    
    print("Plz select a solving Method: ")
    print("type r for random search based BnB method")
    print("     l for lexicographic search based BnB method")
    print("     m for most-constrained-grid-first search based BnB method")
    print("     s for smallest-sized-word-first search based BnB method")
    print("     o for optimization/mathematical-modeling based method")
    print("     c for constraint satisfaction problem based method")
    print()
    solvingFlag = input("Provide your input- ")
        
    # Initialize
    depth = 0
    NewVar ={}
    data = utility.DATA(file)
    
    
    data.XnYWisegridValLimit() ## Add constraints on input data as per parameter value
    data.initializedFixedVar() ## Initialize every empty grid with zero value
    
    if solvingFlag =='s':    
        data.mapTolenthOfTheWordToVar()
        GridToFill = data.mapVarToWordLength
    
    elif solvingFlag =='r':
        GridToFill = data.Emptygrid
    
    elif solvingFlag =='l':
        GridToFill = data.Var
    elif solvingFlag !='o' and solvingFlag !='c' and solvingFlag !='m':
        raise ValueError("Plz Provide correct input...")
    
    VarInBoardToFill = data.Var
    KeyisFinallyUpdated ={}
    valueTriedSoFar = {}
    
    for i in data.Var:
        KeyisFinallyUpdated[i] = False
        valueTriedSoFar[i] = []
    
    if solvingFlag =='o':
        
        Stime = time.time()
        opt = cplexmodeling.OPT(data.Emptygrid, data.HLinearCons, data.VLinearCons)
        ## Create model
        opt.createModel(data.Var)
        
        ## solve and get solution
        solVal = opt.solveModel()
        print("Final Solution is ", solVal)
        print("Time Taken in solving the problem instance (sec): ",(time.time() - Stime))
    else:
        Stime = time.time()
        solveUsingLexicoGraphicBranch(VarInBoardToFill,KeyisFinallyUpdated,data)
    
        print("Time Taken in solving the problem instance (sec): ",(time.time() - Stime))