#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      aketay
#
# Created:     24/04/2014
# Copyright:   (c) aketay 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
import numpy
import FDLoader



class GetTeams:
    def __init__(self):
        self.rownum = 0
        self.getZipsData()
        self.getZipsPitcherData()
        self.playerList ={}
        self.pitcherList ={}


    def getZipsData(self):
        self.my_data = numpy.genfromtxt('Zips_Update.csv', names=True, dtype=None,
         delimiter=',')
        for item in self.my_data:
            for x in range(0,len(item)):
                item[x] = item[x].replace('"','')


    def getZipsPitcherData(self):
        self.my_PitcherData = numpy.genfromtxt('Zips_P_Update.csv', names=True, dtype=None,
         delimiter=',')
        for item in self.my_PitcherData:
            for x in range(0,len(item)):
                item[x] = item[x].replace('"','')

