#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 23:01:49 2021

@author: Dev
"""
import sys
from solvingKakuromethods import solvingKakuro



if __name__ =="__main__":
    
    
    if len(sys.argv) != 2:
        print("You can provide input file : python kakuro.py inputFile")
        print()
        print("Start solving textFile1.txt available in pwd...")
        print()
        solvingKakuro("testFile1.txt")
    
    elif len(sys.argv) == 2:
        solvingKakuro(sys.argv[1])
    if len(sys.argv) >2:
        raise ValueError("Can not provide more than 2 argument: Try python kakuro.py any_inputFile")
    
