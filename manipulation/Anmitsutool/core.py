# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 23:49:19 2020

@author: Transcendence
"""


def Masher(TFfinder,desiring,gap,closegap,snaps,snap,desired,mashfile,rp,rn,rf,rfn,mashmode,mashmodes,mk):

    for i in gap.keys():
        if i<=rn[mk] and closegap < i:
            closegap = i
 
    for i in range(int(len(desired)/2)):
        if desired[2*i]<=rn[mk] and desired[2*i+1]>=rn[mk]:
            TFfinder = True
            desiring=desired[2*i]
            snaps=snap[i]
            mashmodes = mashmode[i]
            if mashmodes == 1:
                if mk >= 256:
                    desiring -= gap[closegap]*snaps
                    
                snaps *= 2
            if mashmodes == 2:
                if mk <= 256:
                    desiring -= gap[closegap]*snaps
                snaps *= 2

    if TFfinder:
        while True:
            if int(desiring) <= rn[mk] and int(desiring + gap[closegap]*snaps) > rn[mk]:
                break;
            desiring += gap[closegap]*snaps

        if int(desiring + gap[closegap]*snaps) >= rf[mk] and int(desiring) <= rp[mk]:
            mashfile.write(rfn[mk].group(0))
        elif int(desiring + gap[closegap]*snaps) >= rf[mk] and int(desiring) > rp[mk]:
            rn[mk]=int(desiring)
            mashfile.write(rfn[mk].group(1)+","+rfn[mk].group(2)+","+str(rn[mk])+rfn[mk].group(4)+"\n")
        elif int(desiring + gap[closegap]*snaps) < rf[mk] and int(desiring) <= rp[mk]:
            rn[mk]=int(desiring + gap[closegap]*snaps)
            mashfile.write(rfn[mk].group(1)+","+rfn[mk].group(2)+","+str(rn[mk])+rfn[mk].group(4)+"\n")
        else:
            if int(rn[mk]-desiring) > int(desiring + gap[closegap]*snaps-rn[mk]):
                rn[mk]=int(desiring + gap[closegap]*snaps)
                mashfile.write(rfn[mk].group(1)+","+rfn[mk].group(2)+","+str(rn[mk])+rfn[mk].group(4)+"\n")
            else:
                rn[mk]=int(desiring)
                mashfile.write(rfn[mk].group(1)+","+rfn[mk].group(2)+","+str(rn[mk])+rfn[mk].group(4)+"\n")
                
    else:
         mashfile.write(rfn[mk].group(0))