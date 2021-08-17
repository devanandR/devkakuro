#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 15:31:19 2021

@author: dev
"""
import cplex

class OPT:
    varIndx = []
    ObjlistOfPair = []
    absVarsName = []
    def __init__(self, Vars, Rows, Column):
      
        self.totalvars = len(Vars)
        self.model = cplex.Cplex()
        self.varPosition = Vars
        self.Rows = Rows
        self.Column = Column
        
    def addVariableToModel(self, varPosition):
        
        self.model.variables.add(names =[r 
                                    for r in varPosition], types = 
                                        [self.model.variables.type.integer]* len(varPosition))
    
    
    def createModel(self,VarUb):
        
        if not VarUb:
            raise ValueError("Var Constraint list/dic/set is empty")
        ## Add variable
        tempVarName = ['int_'+str(r[0])+str(r[1]) for r in self.varPosition]
        self.addVariableToModel(tempVarName)
        
        
        ## Take care of bounds
        self.setLnUBnd(VarUb)
        
        ## Now start working on creating constraints
        self.addConst(self.Rows,'Row')
        
        ## For Column
        self.addConst(self.Column,'Column')
        
        
        ## For Objective Function
        self.addPairForObj(self.Rows)
        self.addPairForObj(self.Column)
        
        self.createObj()
        
    def setLnUBnd(self,VarUb):
        
        ## Lower bound update
        self.model.variables.set_lower_bounds([(i,1) for i in range(len(self.varPosition))])
        
        ## Upper Bound update
        self.model.variables.set_upper_bounds([(i,min(9,VarUb[v])) 
                        for i,v in zip(range(len(self.varPosition)),self.varPosition)])
    def addConst(self,ConsList,ConsType ='Horiz'):
        
        for l in ConsList:
            V = ConsList[l][0]
            ConsVars = ConsList[l][1]
            #print(ConsVars,"ConsVars")
            indList = ['int_'+str(r[0])+str(r[1]) for r in ConsVars]
            #print(indList,"indList")
            coefList = [1]*len(ConsVars)
            #print(coefList,"coefList")
            Name = ["ConsType"+"_"+str(l)]
            senseType = ["E"]
            Rhs = [float(V)]
            self.addconstraintToModel(indList,coefList, senseType, Name,Rhs)
            
    def addconstraintToModel(self,indList,coefList, senseType, Name,Rhs):
        
        self.model.linear_constraints.add(lin_expr = [cplex.SparsePair(ind = indList, 
                                                    val = coefList)],
                                                            senses =senseType, rhs=Rhs,
                                                            names=Name)
    
    def addPairForObj(self, ConsList):
        
        print("Now finding suitable constraints and vars for obj creation")
        for l in ConsList:
            ConsVars = ConsList[l][1]
            ## Add extra absolute constraints
            for r in ConsVars:
                for s in ConsVars:
                    if r !=s:
                        newvar = 'z'+str(r[0])+str(r[1])+"_"+str(s[0])+str(s[1])
                        
                        if newvar in self.absVarsName:
                            continue
                        self.absVarsName.append(newvar)
                        rname = 'int_'+str(r[0])+str(r[1])
                        sname = 'int_'+str(s[0])+str(s[1])
                        self.addVariableToModel([newvar])
                        indList = [newvar,rname,sname]
                        coefList = [1.,1.,-1.]
                        senseType = ["G"]
                        Name = ["ext"+str(l)]
                        Rhs =[0]
                        ##
                        #print(indList,"indList")
                        #print(coefList,"coefList")
                        #print(Name)
                        #print(Rhs)
                        self.addconstraintToModel(indList,coefList, senseType,Name,Rhs)            
                        
                        ### One more set
                        indList = [newvar,rname,sname]
                        coefList = [1.,-1.,1.]
                        senseType = ["G"]
                        Name = ["ext1"+str(l)]
                        Rhs =[0]
                        ##
                        self.addconstraintToModel(indList,coefList, senseType,Name,Rhs)            
                        
                        
                        
                        ## Update Pair for Objective creation
                        self.ObjlistOfPair.append((newvar,100)) ## Some high number
            ## Add extra absolute constraints
            
    def createObj(self):
        self.model.objective.set_linear(self.ObjlistOfPair)
        ## Change sense to maximize
        self.model.objective.set_sense(self.model.objective.sense.maximize)
        
        
        
    def solveModel(self):
        
        self.model.solve()
        self.model.write("KakuroIP.LP")
        
        solList =  self.model.solution.get_values()
        
        #print(solList,"solList")
        #print(self.nameToVarDict,"nameToVarDict")
        i=0
        SolutionDict ={}
        for v in self.varPosition:
            SolutionDict[v] = solList[i]
            i+=1
            
        return SolutionDict
        