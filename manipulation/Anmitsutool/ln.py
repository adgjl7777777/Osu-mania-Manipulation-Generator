# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:52:57 2020

@author: Transcendence
"""
import re

def LNcompress(lff,maxlnmash,rfn,copy,dummy,rp,rn,rf,mashfile,mk):

    if int(lff.group(5))-int(lff.group(3)) <= maxlnmash:
        dummy=re.match(r"(\d+,\d+,\d+,)128,(\d+,)\d+:(\d+:\d+:\d+:\d+:.*\n)$",copy)
        rfn[mk]=re.match(r"(\d+),(\d+),(\d+)(,1,\d+,\d+:\d+:\d+:\d+:[^:]*)\n$",dummy.group(1)+"1,"+dummy.group(2)+dummy.group(3))
        dummy = None

    else:
        rp[mk]=int(lff.group(5))
        mashfile.write(copy)
        if mk in rn.keys():
            del rn[mk]
        if mk in rf.keys():
            del rf[mk]
        if mk in rfn.keys():
            del rfn[mk]
