# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 03:26:39 2020

@author: Transcendence
"""
from Anmitsutool.error import *
from Anmitsutool.core import *
from Anmitsutool.ln import *
import re
import copy as cp

def Mashgenerator(matching,matching2,desired,snap,mashmode,origin):
    if matching:
        mashfile = open(matching.group(1) + "_mash].osu","w",encoding="UTF8")
    elif matching2:
        mashfile =  open(matching2.group(1) + "_mash.osu","w",encoding="UTF8")
    
    copy = "\n"
    TFfinder = False
    invfile = 0
    while copy != "[Metadata]\n":
        copy = origin.readline()
        if copy == "Mode: 3\n":
            TFfinder = True        
        mashfile.write(copy)
        invfile +=1
        if invfile > 10000:
            raise fileerror()
    
    if not TFfinder:
        raise modeerror()    
    for i in range(5):
        copy = origin.readline()
        mashfile.write(copy)
        
    copy = origin.readline()
    mashfile.write(copy[:-1] + "_mash\n") 
    while copy != "[Difficulty]\n":
        copy = origin.readline()
        mashfile.write(copy)
    copy = origin.readline()
    mashfile.write(copy)
     
    copy = origin.readline()
    maniakey = int(re.match(r".*:(\d*)\n",copy).group(1))
    mashfile.write(copy)
    
    while copy != "[TimingPoints]\n":
        copy = origin.readline()
        mashfile.write(copy)
    bpm = {}
    
    while copy != "[HitObjects]\n":
        copy = origin.readline()
        mashfile.write(copy)
        bpmget=re.match(r"(\d+),([\.0-9]+),\d+,\d+,\d+,\d+,1,\d+\n$",copy)
        if bpmget:
            bpm[int(bpmget.group(1))] = 60000/float(bpmget.group(2))
    
    if not bpm:
        raise bpmerror() #if there is no bpm set in map
    bpmdummy = sorted(list(bpm.keys()))[0]
    while bpmdummy<0:
        bpmdummy -= 60000/bpm[sorted(list(bpm.keys()))[0]]
    bpmdummy += 60000/bpm[sorted(list(bpm.keys()))[0]]
    bpm[bpmdummy]=bpm[sorted(list(bpm.keys()))[0]]
    
    gap = {list(bpm.keys())[i] : 60000/list(bpm.values())[i] for i in range(len(bpm))}
    rp = {}
    rn = {}
    rf = {}    
    rfn = {}
    lff = None
    rff = None
    dummy = None    
    maxlnmash = 35
    Error192 = False
    TFfinder = False    
    closegap = 0
    desiring = 0   
    mk = 0
    
    while copy != "":
        TFfinder = False
        closegap = 0
        desiring = 0
        mk = 0
        snaps = 0
        mashmodes = 0
        
        copy = origin.readline()
        lff = re.match(r"(\d+),(\d+),(\d+),128(,\d+,)(\d+):(\d+:\d+:\d+:\d+:.*\n)$",copy)
        rff = re.match(r"(\d+),(\d+),(\d+)(,\d,\d+,\d+:\d+:\d+:\d+::?[^:]*)\n$",copy)
        if rff:
            mk = int(rff.group(1))
            
            
            if mk in rn.keys():
                rp[mk] = rn[mk]
                rn[mk] = rf[mk]
                rf[mk] = int(rff.group(3))
                Masher(TFfinder,desiring,gap,closegap,snaps,snap,desired,mashfile,rp,rn,rf,rfn,mashmode,mashmodes,mk)
                rfn[mk]=cp.deepcopy(rff)
                
            elif mk in rf.keys() and mk not in rp.keys():
                rn[mk] = rf[mk]
                rf[mk] = int(rff.group(3))
                mashfile.write(rfn[mk].group(0))
                rfn[mk]=cp.deepcopy(rff)
    
            elif mk in rf.keys() and mk in rp.keys():
                rn[mk] = rf[mk]
                rf[mk] = int(rff.group(3))
                Masher(TFfinder,desiring,gap,closegap,snaps,snap,desired,mashfile,rp,rn,rf,rfn,mashmode,mashmodes,mk)
                rfn[mk]=cp.deepcopy(rff)
    
            else:
                rf[mk] = int(rff.group(3))
                rfn[mk]=cp.deepcopy(rff)
                  
        elif lff:
            mk = int(lff.group(1))
    
            if mk in rn.keys():
                rp[mk] = rn[mk]
                rn[mk] = rf[mk]
                rf[mk] = int(lff.group(3))
                Masher(TFfinder,desiring,gap,closegap,snaps,snap,desired,mashfile,rp,rn,rf,rfn,mashmode,mashmodes,mk)
                LNcompress(lff,maxlnmash,rfn,copy,dummy,rp,rn,rf,mashfile,mk)
        
            elif mk in rf.keys() and mk not in rp.keys():
                mashfile.write(rfn[mk].group(0))
                rn[mk]=rf[mk]
                rf[mk]=int(lff.group(3))
                LNcompress(lff,maxlnmash,rfn,copy,dummy,rp,rn,rf,mashfile,mk)
    
            elif mk in rf.keys() and mk in rp.keys():
                rn[mk] = rf[mk]
                rf[mk] = int(lff.group(3))            
                Masher(TFfinder,desiring,gap,closegap,snaps,snap,desired,mashfile,rp,rn,rf,rfn,mashmode,mashmodes,mk)
                LNcompress(lff,maxlnmash,rfn,copy,dummy,rp,rn,rf,mashfile,mk)
                
            else:
                rf[mk]=int(lff.group(3))
                LNcompress(lff,maxlnmash,rfn,copy,dummy,rp,rn,rf,mashfile,mk)

    for i in rfn.keys():
        mashfile.write(rfn[i].group(0))       
             
    mashfile.close()