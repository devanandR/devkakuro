#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 14:19:37 2021

@author: jyoti
"""

import random
import utility 
import copy


def selectVarRandomly(aList):
    
    if not aList:
        raise ValueError("Provided non empty List/Set")
    return random.choice(aList)


def solveUsingLexicoGraphicBranch(VarInBoardToFill,KeyisFinallyUpdated,data): 
    
    global NewVar,breakFlag,root
    valueTriedSoFar ={}
    ## Choose vars one by one and randomly fill values
    #NewVar = copy.deepcopy(VarInBoardToFill)
    for key in VarInBoardToFill:
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
                root = root + 1 ## Going down the tree
                breakFlag = solveUsingLexicoGraphicBranch(VarInBoardToFill, KeyisFinallyUpdated,data)
                root = root - 1 ## Return back down the tree
                if not breakFlag:
                    KeyisFinallyUpdated[key] = True
                else:
                    KeyisFinallyUpdated[key] = False
                    data.updateVarToFixVal(key, 0)
            else:
                NewVar = copy.deepcopy(VarInBoardToFill)

    if root== 0:    
        print(NewVar,"Final Solution")
        
    
if __name__ =="__main__":
    
    # Read Data
    global NewVar
    global valueTriedSoFar
    global breakFlag
    global root
    root = 0
    NewVar ={}
    data = utility.DATA("testFile1.txt")
    #print(data.column)
    data.XnYWisegridValLimit() ## Add constraints on input data
    data.initializedFixedVar()
    print("Var",data.Var)
    print("VLinearCons",data.VLinearCons)
    print("VLinearCons",data.HLinearCons)
    print()
    
    VarInBoardToFill = data.Var
    KeyisFinallyUpdated ={}
    valueTriedSoFar = {}
    breakFlag = False
    for i in data.Var:
        KeyisFinallyUpdated[i] = False
        valueTriedSoFar[i] = []
    solveUsingLexicoGraphicBranch(VarInBoardToFill,KeyisFinallyUpdated,data)
    #print(NewVar,"NewVar")