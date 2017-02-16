#-------------------------------------------------------------------------------
# Name:readCSV        
# Purpose:
#
# Author:      aketay
#
# Created:     24/04/2014
#-------------------------------------------------------------------------------
import csv

class GetTeams:
    def __init__(self):
        self.rownum = 0
        self.sheetDict ={}
        self.parkDict={}

        self.topTeam =[]
        self.botTeam =[]
        self.topTeamPitchers = []
        self.botTeamPitchers = []
        self.location = ""
        self.getStuff()

    def getStuff(self):
        ifile  = open("lineuptest.csv", "rb")
        reader = csv.reader(ifile)

        for row in reader:
            self.sheetDict[row[0]]=[row[1],row[2]]

        for item in self.sheetDict.keys():
            if item == "1":
                self.topTeam.insert(0,self.sheetDict[item][0])
                self.botTeam.insert(0,self.sheetDict[item][1])
            elif item == "2":
                self.topTeam.insert(1,self.sheetDict[item][0])
                self.botTeam.insert(1,self.sheetDict[item][1])
            elif item == "3":
                self.topTeam.insert(2,self.sheetDict[item][0])
                self.botTeam.insert(2,self.sheetDict[item][1])
            elif item == "4":
                self.topTeam.insert(3,self.sheetDict[item][0])
                self.botTeam.insert(3,self.sheetDict[item][1])
            elif item == "5":
                self.topTeam.insert(4,self.sheetDict[item][0])
                self.botTeam.insert(4,self.sheetDict[item][1])
            elif item == "6":
                self.topTeam.insert(5,self.sheetDict[item][0])
                self.botTeam.insert(5,self.sheetDict[item][1])
            elif item == "7":
                self.topTeam.insert(6,self.sheetDict[item][0])
                self.botTeam.insert(6,self.sheetDict[item][1])
            elif item == "8":
                self.topTeam.insert(7,self.sheetDict[item][0])
                self.botTeam.insert(7,self.sheetDict[item][1])
            elif item == "9":
                self.topTeam.insert(8,self.sheetDict[item][0])
                self.botTeam.insert(8,self.sheetDict[item][1])
            elif item =="location":
                self.location = self.sheetDict[item][0]
            elif item =="Starting Pitcher":
                self.topTeamPitchers.append([self.sheetDict[item][0],"SP"])
                self.botTeamPitchers.append([self.sheetDict[item][1],"SP"])
            elif item =="7th":
                self.topTeamPitchers.append([self.sheetDict[item][0],"RP"])
                self.botTeamPitchers.append([self.sheetDict[item][1],"RP"])
            elif item =="8th":
                self.topTeamPitchers.append([self.sheetDict[item][0],"RP"])
                self.botTeamPitchers.append([self.sheetDict[item][1],"RP"])
            elif item =="9th":
                self.topTeamPitchers.append([self.sheetDict[item][0],"RP"])
                self.botTeamPitchers.append([self.sheetDict[item][1],"RP"])
            elif item =="Closer":
                self.topTeamPitchers.append([self.sheetDict[item][0],"C"])
                self.botTeamPitchers.append([self.sheetDict[item][1],"C"])


        ifile.close()

    def getParkFactors(self):
        ifile  = open("parkfactors.csv", "rb")
        reader = csv.reader(ifile)

        # Home Runs, Runs Scored, Hits, Doubles, Triples, LHB- Rating, RHB- Rating
        for row in reader:
            self.parkDict[row[0]]=[row[1],row[2],row[3],row[4],row[5],row[6],row[7]]



        ifile.close()

