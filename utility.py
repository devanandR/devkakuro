#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 21:41:50 2021

@author: jyoti
"""
import copy

class DATA:
    
    horizontalParam  = {}
    verticalParam  = {}
    Emptygrid = []
    Var = {}
    HLinearCons = {}
    VLinearCons = {}
    FixedVal ={}
    def __init__(self, kakuroProblemFile):
        
        
        tempcolumn = 0
        linenumber = 0
        with open(kakuroProblemFile, 'r') as Grid:
            Grid = Grid.readlines()
            self.rows = len(Grid) ## Number of rows
            for line in Grid:
                line = line.strip('\n')
                if not line:
                    raise ValueError("Do not leave space between lines!")
                line = line.split(",")
                if len(line) == tempcolumn or tempcolumn ==0:
                    tempcolumn = len(line)
                else:
                    raise ValueError("Number of grids in rows of GridBoard mismatch, plz check")
                
                ## Line with only # does no have value and empty grid
                #print(line)
                #if "\\" in line or "0" in line: 
                self.fetchParamsAndVars(line,linenumber)
                linenumber+=1
                
            self.column = tempcolumn 
            #print(Grid)
            #print(self.horizontalParam,"horizontalParam")
            #print(self.verticalParam,"verticalParam")
            #print(self.Emptygrid,"Emptygrid")
    
    
    def fetchParamsAndVars(self, line,linenumber):
        
        gridnumber = 0
            
        for grid in line:
            if "\\" in grid:
                grid = grid.split("\\")
                if grid[1] !='#':
                    self.horizontalParam[linenumber, gridnumber] = int(grid[1])
                if grid[0] !='#':
                    self.verticalParam[linenumber, gridnumber] = int(grid[0])
            if "0" in grid:
                self.Emptygrid.append((linenumber, gridnumber))
            gridnumber+=1   
            #print(grid)
    
    def horizontalParamVal(self,x):
        
        if x in self.horizontalParam:
            return self.horizontalParam[x]
        else:
            raise ValueError("Provide proper coordinate point")
    
    def verticalParamVal(self, x):
        if x in self.verticalParam:
            return self.verticalParam[x]
        else:
            raise ValueError("Provide proper coordinate point")
    
    def isCoordinateForVar(self,x):
        if x in self.Emptygrid:
            return True
        else:
            return False

    def XnYWisegridValLimit(self):
        
        counter =0
        for grid in self.horizontalParam:
            
            x_axis = grid[0]
            y_axis = grid[1]
            
            ## Now started looking right ward for a given row 
            #(x_axis) and assign the maximum possible value a variable can take
            y_axis = y_axis + 1
            
            lCoefIndices = []
            while self.isCoordinateForVar((x_axis,y_axis)):
                
                lCoefIndices.append((x_axis,y_axis))
                if (x_axis,y_axis) in self.Var: 
                    self.Var[x_axis,y_axis] = min(self.horizontalParam[grid], self.Var[x_axis,y_axis])
                else:
                    self.Var[x_axis,y_axis] = self.horizontalParam[grid]
                y_axis = y_axis + 1 ## increment by 1
            self.HLinearCons[counter] =(self.horizontalParam[grid],lCoefIndices)
            counter+=1
        ### Now add more constraints on grid value using vertical paramter information
        counter =0
        for grid in self.verticalParam:
            
            x_axis = grid[0]
            y_axis = grid[1]
            
            ## Now started looking right ward for a given row 
            #(x_axis) and assign the maximum possible value a variable can take
            x_axis = x_axis + 1
            lCoefIndices = []
            while self.isCoordinateForVar((x_axis,y_axis)):
                
                lCoefIndices.append((x_axis,y_axis))
                if (x_axis,y_axis) in self.Var: 
                    self.Var[x_axis,y_axis] = min(self.verticalParam[grid],self.Var[x_axis,y_axis])
                else:
                    self.Var[x_axis,y_axis] = self.verticalParam[grid]
                x_axis = x_axis + 1 ## increment by 1
            self.VLinearCons[counter] =(self.verticalParam[grid],lCoefIndices)
            counter+=1
    def initializedFixedVar(self):
        
        for i in self.Var:
            self.FixedVal[i] = 0
        
    def updateVarToFixVal(self, k, v):
        self.FixedVal[k] = v
        
        
    
    def updateHnUUB(self, newVars,key,value,Vars, LinearCons):    
        
        ### do reduction in the corresponding gid alligned horizontally to the (key,value)
        for l in LinearCons:
            if key in LinearCons[l][1]:
                keyList = LinearCons[l][1] ## Associated key list
                ## This row contains (key,value). Lets do the reduction
                #first check reduction is possible:
                sumTemp = LinearCons[l][0] - value ### The affective rhs of Equation value
                newVars[key] = value 
                
                allVarsettofix = True
                for i in keyList:
                    if i !=key:
                        if self.FixedVal[i] ==0:
                            allVarsettofix = False            
                            if Vars[i] >= sumTemp:
                                newVars[i] = sumTemp
                            #    return False,newVars
                            else:
                                newVars[i] = sumTemp - Vars[i]
                        else:## Modify Upper Bound
                            sumTemp = sumTemp - self.FixedVal[i]
                if sumTemp < 0 or (allVarsettofix and sumTemp!=0):
                    return False,newVars ### Sum of effective upper bound is more than the given limit
                    
        
        return True, newVars
            
        
    def updateUB(self,key,value, Vars):
        
        newVars = copy.deepcopy(Vars)
        Possible, newVars =  self.updateHnUUB(newVars,key,value,Vars, self.HLinearCons)
        
        if not Possible:
            return Possible, newVars
        else:
            return self.updateHnUUB(newVars,key,value,Vars, self.VLinearCons)
        
        
        