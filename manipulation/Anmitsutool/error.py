# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:47:49 2020

@author: Transcendence
"""

class fileerror(Exception):
    def __init__(self):
        print(1)

class bpmerror(Exception):
    def __init__(self):
        print(2)

class modeerror(Exception):
    def __init__(self):
        print(3)