#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      aketay
#
# Created:     24/04/2014
# Copyright:   (c) aketay 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import json
import csv
import readCSV
import time



teamObject = readCSV.GetTeams()

class FDSALCAP:
    def __init__(self):
        self.FDSALCAPJSON = None
        self.f = None
        self.fdSalCapDict = {}
        self.getFDInfo()

    def getFDInfo(self):
        f = open(r'/Users/Slyjester/Desktop/FDSALCAP.Json')

        decoded_data = json.load(f)


        for key, value in decoded_data.items():
            self.fdSalCapDict[value[1]] = [value[5],value[0],value[6]]

        with open("FanDuelSalCap.json", "w") as outfile:
            json.dump(self.fdSalCapDict, outfile, indent=4)

