#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 23:01:49 2021

@author: dev
"""
import sys
from solvingKakuromethods import solvingKakuro



if __name__ =="__main__":
    
    if len(sys.argv) >2:
        raise ValueError("You can not provide more than 2 arguments: Try python kakuro.py any_inputFile")
    
    if len(sys.argv) != 2:
        print("Expecting input patten as : python kakuro.py inputFile")
        print()
        print("Going to start solving a problem textFile1.txt available in pwd...")
        print()
        solvingKakuro("testFile1.txt")
    
    elif len(sys.argv) == 2:
        solvingKakuro(sys.argv[1])
    
