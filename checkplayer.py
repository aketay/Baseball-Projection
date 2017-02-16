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
import datetime
import time
import urllib2
import re
import math
import readZIPS

from bs4 import BeautifulSoup
from datetime import timedelta, date
from urllib2 import HTTPError
from fuzzywuzzy import fuzz

class PlayerStats:
    def __init__(self):
        self.TopTeam = True
        self.topTeamLineUp = []
        self.botTeamLineUp = []
        self.topTeamPitchingLineUp =[]
        self.botTeamPitchingLineUp = []
        self.playerNameList = {}
        self.zipsData = readZIPS.GetTeams()
        self.tempPitcherData = {}



    def checkPitcherStatsType(self,s,pitcherType):
            websiteString = "http://espn.go.com/mlb/player/splits/_/id/" + s
            try:
                sock2 = urllib2.urlopen(websiteString)
            except urllib2.HTTPError, e:
                urlerrorCode = e.code
                print urlerrorCode
                print e.fp.read()




            dataslerp = sock2.read()

            dataderp = dataslerp.replace('&nbsp;', '')

            soup = BeautifulSoup(dataderp)

            selects = soup.find_all("select", { "class" : "tablesm" })

            self.playerNameList[s] = soup.select("#content > div.mod-container.mod-no-header-footer.mod-page-header > div.mod-content > h1")[0].text


            yearlist = []

            for item in selects[0].find_all("option"):
                yearlist.append(item.contents)

            if any("3 year (2011-2013)" in s for s in yearlist):
                websiteString = "http://espn.go.com/mlb/player/splits/_/id/" + s + "/type/pitching/"
                self.getPitcherStats(s,websiteString,pitcherType)
            else:
                websiteString = "http://espn.go.com/mlb/player/splits/_/id/" + s + "/type/pitching/"
                self.getPitcherStats(s,websiteString,pitcherType)
                print "We aint got 3 years!"

    def getPitcherStatsZips(self,s):
            websiteString = "http://www.fangraphs.com/statss.aspx?playerid=" + s + "&position=P"

            try:
                sock2 = urllib2.urlopen(websiteString)
            except urllib2.HTTPError, e:
                urlerrorCode = e.code
                print urlerrorCode
                print e.fp.read()

            dataslerp = sock2.read()

            dataderp = dataslerp.replace('&nbsp;', '')

            soup = BeautifulSoup(dataderp)

            table = soup.find_all("table", { "class" : "rgMasterTable", "id":"SeasonStats1_dgSeason2_ctl00" })

            rows = table[0].find_all("tr")


            for item in rows:
                cells = item.find_all("td")
                try:
                    if cells[0].text =="2014" and cells[1].text == "ZiPS (U)":
                        self.tempPitcherData['AVG']= cells[8].text

                except:
                    pass




    def getPitcherStats(self,s,passedString,pitcherType):
            websiteString = passedString
            playerVsLeft = 0
            playerVsRight = 0

            try:
                sock2 = urllib2.urlopen(websiteString)

            except urllib2.HTTPError, e:
                urlerrorCode = e.code
                print urlerrorCode
                print e.fp.read()

            dataslerp = sock2.read()

            dataderp = dataslerp.replace('&nbsp;', '')


            soup = BeautifulSoup(dataderp)

            table = soup.find_all("table", { "class" : "tablehead" })

            rows = table[0].find_all("tr")
            pitcherHandedness = "R"
            handednessList = soup.find_all("ul", {"class" : "general-info"})
            for item in handednessList[0].find_all("li"):
                if "Throws: R" in item.text:
                    pitcherHandedness = "R"
                elif "Throws: L" in item.text:
                    pitcherHandedness = "L"

            ipRows = rows[2].find_all("td")

            pitcherIP = float(ipRows[9].text)
            pitcherGP = float(ipRows[6].text)


            #(Pitcher Type, Innings, Name, Handedness, OBPAL,OBPAR, Single, Double, Triple, HR, Walk, Strike Out)
            for item in rows:
                cells = item.find_all("td")
                if cells[0].text =="Total":
                    pitcherHits = float(cells[3].text)
                    pitcher2B = float(cells[4].text)
                    pitcher3B = float(cells[5].text)
                    pitcherHR = float(cells[6].text)
                    pitcherBB = float(cells[8].text)
                    pitcherHPB = float(cells[9].text)
                    pitcherSO = float(cells[10].text)


                if cells[0].text =="vs. Left":
                    pitcherVsLeft = float(cells[14].text)
                    pitcherVsLeftAB = float(cells[1].text)

                if cells[0].text =="vs. Right":
                    pitcherVsRight = float(cells[14].text)
                    pitcherVsRightAB = float(cells[1].text)


            try:
                pitcherName =  soup.select("#content > div.mod-container.mod-no-header-footer.mod-page-header > div.mod-content > h1")[0].text.strip()
            except:
                try:
                    pitcherName =  soup.select("#content > div.mod-container.mod-no-header-footer.mod-page-header.mod-header-no-headshot > div.mod-content > div.player-bio > h1")[0].text.strip()
                except:
                    pitcherName = "Nope"



            for item in self.zipsData.my_PitcherData:
                if fuzz.ratio(item[0],pitcherName) > 85:
                    self.tempPitcherData['H'] = float(item[7])
                    self.tempPitcherData['IP'] = float(item[6])
                    self.tempPitcherData['HR'] = float(item[9])
                    self.tempPitcherData['SO'] = float(item[10])
                    self.tempPitcherData['G'] = float(item[5])
                    self.tempPitcherData['BB'] = float(item[11])
                    self.getPitcherStatsZips(str(item[17]))
                    self.tempPitcherData['AB'] = round(float(self.tempPitcherData['H']) / float(self.tempPitcherData['AVG']),3)
                    self.tempPitcherData['OBP'] = round((float(item[7])+float(item[11]))/(self.tempPitcherData['AB']+float(item[11])),3)

            try:
                pitcherInnings = math.trunc(pitcherIP/pitcherGP)
                if pitcherInnings < 1:
                    pitcherInngs = 1


            except:
                pitcherInnings = 1

            try:
                pitcher1BA = round((pitcherHits-pitcher2B-pitcher3B-pitcherHR)/(pitcherHits),3)

            except:
                pitcher1BA = 0.01

            try:
                pitcher2BA = round((pitcher2B/pitcherHits),3)
            except:
                pitcher2BA = 0.01

            try:
                pitcher3BA = round((pitcher3B/pitcherHits),3)
            except:
                pitcher3BA = 0.01

            try:
                pitcherHRA = round((pitcherHR/pitcherHits),3)
            except:
                pitcherHRA = 0.01

            try:
                pitcherBBA = round((pitcherHPB + pitcherBB )/(pitcherHits + pitcherHPB + pitcherBB),3)
            except:
                pitcherBBA = 0.01

            try:
                pitcherSOA = round(pitcherSO / (math.trunc(pitcherIP)*3),3)
            except:
                pitcherSOA = 0.01


            if pitcherIP < 100:
                pitcherInnings = math.trunc(self.tempPitcherData['IP']/self.tempPitcherData['G'])
                if pitcherInnings < 1:
                    pitcherInngs = 1

                pitcherBBA = round((float(self.tempPitcherData['BB']))/(float(self.tempPitcherData['H']) + float(self.tempPitcherData['BB'])),3)
                pitcherSOA = round(float(self.tempPitcherData['SO'] )/ (math.trunc(float(self.tempPitcherData['IP']))*3),3)
                pitcherHRA = round(float((self.tempPitcherData['HR']/self.tempPitcherData['H'])),3)


                pitcher2BA = round((pitcher2BA * (pitcherIP/100))+(0.210*((100-pitcherIP)/100)),3)
                pitcher3BA = round((pitcher3BA * (pitcherIP/100))+(0.022*((100-pitcherIP)/100)),3)
                pitcher1BA = round((1- pitcher2BA-pitcher3BA-pitcherHRA),3)

            if pitcherVsLeftAB < 100:
                pitcherVsLeft = round((pitcherVsLeft * (pitcherVsLeftAB/100))+(self.tempPitcherData['OBP']*((100-pitcherVsLeftAB)/100)),3)

            if pitcherVsRightAB < 100:
                pitcherVsRight = round((pitcherVsRight * (pitcherVsRightAB/100))+(self.tempPitcherData['OBP']*((100-pitcherVsRightAB)/100)),3)

            #(Pitcher Type, Innings, Name, Handedness, OBPAL,OBPAR, Single, Double, Triple, HR, Walk, Strike Out):
            if self.TopTeam == True:
                self.topTeamPitchingLineUp.append((pitcherType,pitcherInnings,s,pitcherHandedness,pitcherVsLeft,pitcherVsRight,pitcher1BA,pitcher2BA,pitcher3BA,pitcherHRA,pitcherBBA, pitcherSOA))
            elif self.TopTeam == False:
                self.botTeamPitchingLineUp.append((pitcherType,pitcherInnings,s,pitcherHandedness,pitcherVsLeft,pitcherVsRight,pitcher1BA,pitcher2BA,pitcher3BA,pitcherHRA,pitcherBBA,pitcherSOA))

            time.sleep(1)





    def checkPlayerStatType(self,s):
                websiteString = "http://espn.go.com/mlb/player/splits/_/id/" + s
                try:
                    sock2 = urllib2.urlopen(websiteString)
                except urllib2.HTTPError, e:
                    urlerrorCode = e.code
                    print urlerrorCode
                    print e.fp.read()

                dataslerp = sock2.read()

                dataderp = dataslerp.replace('&nbsp;', '')

                soup = BeautifulSoup(dataderp)


                try:
                    self.playerNameList[s] = soup.select("#content > div.mod-container.mod-no-header-footer.mod-page-header > div.mod-content > h1")[0].text
                except:
                    self.playerNameList[s] = s

                selects = soup.find_all("select", { "class" : "tablesm" })

                yearlist = []

                for item in selects[0].find_all("option"):
                    yearlist.append(item.contents)

                if any("3 year (2011-2013)" in s for s in yearlist):
                    websiteString = "http://espn.go.com/mlb/player/splits/_/id/" + s + "/type/batting/"
                    self.getplayerstats(s,websiteString)
                else:
                    websiteString = "http://espn.go.com/mlb/player/splits/_/id/" + s + "/type/batting/"
                    self.getplayerstats(s,websiteString)


    def getplayerstats(self,s,passedString):
            websiteString = passedString

            playerVsLeft = 0
            playerVsRight = 0

            try:
                sock2 = urllib2.urlopen(websiteString)

            except urllib2.HTTPError, e:
                urlerrorCode = e.code
                print urlerrorCode
                print e.fp.read()

            dataslerp = sock2.read()

            dataderp = dataslerp.replace('&nbsp;', '')

            soup = BeautifulSoup(dataderp)

            table = soup.find_all("table", { "class" : "tablehead" })

            rows = table[0].find_all("tr")
            playerVsLeftAB = 0
            playerVsLeft = 0
            playerVsRight = 0
            playerVsRightAB = 0

            for item in rows:
                cells = item.find_all("td")
                if cells[0].text =="Total":
                    playerAtBats = float(cells[1].text)
                    playerHits = float(cells[3].text)
                    playerDoubles = float(cells[4].text)
                    playerTriples = float(cells[5].text)
                    playerHomeRuns = float(cells[6].text)
                    playerWalks = float(cells[8].text)
                    playerHBP = float(cells[9].text)
                    playerStrikeOuts = float(cells[10].text)

                if cells[0].text =="vs. Left":
                    playerVsLeft = float(cells[14].text)
                    playerVsLeftAB = float(cells[1].text)



                if cells[0].text =="vs. Right":
                    playerVsRight = float(cells[14].text)
                    playerVsRightAB = float(cells[1].text)
            try:
                playerName =  soup.select("#content > div.mod-container.mod-no-header-footer.mod-page-header > div.mod-content > h1")[0].text.strip()
            except:
                try:
                    playerName =  soup.select("#content > div.mod-container.mod-no-header-footer.mod-page-header.mod-header-no-headshot > div.mod-content > div.player-bio > h1")[0].text.strip()
                except:
                    playerName = "Nope"


            #Checks Batters Against Zips!
            tempStats = None

            for item in self.zipsData.my_data:
                   if fuzz.ratio(item[0],playerName) > 85:
                       tempStats = item

            try:

                if playerVsLeftAB < 100:
                    playerVsLeft = round((float(tempStats[16])*round(((100-playerVsLeftAB)/100),3)+ playerVsLeft* round(playerVsLeftAB/100,3)),3)

                if playerVsRightAB < 100:
                    playerVsRight = round((float(tempStats[16])*round(((100-playerVsRightAB)/100),3)+ playerVsLeft* round(playerVsRightAB/100,3)),3)

                if playerAtBats < 100:
                    playerHits = float(tempStats[4])
                    playerDoubles = float(tempStats[5])
                    playerTriples = float(tempStats[6])
                    playerHomeRuns = float(tempStats[7])
                    playerWalks = float(tempStats[10])
                    playerHBP = float(tempStats[12])
                    playerStrikeOuts = float(tempStats[11])
                    playerAtBats = float(tempStats[3])
            except:
                pass



            try:
                playerSingles = (playerHits - playerDoubles - playerTriples - playerHomeRuns)
            except:
                playerSinges = 0
            try:
                player1B = round(float(playerSingles)/float(playerHits),3)
            except:
                player1B = 0

            try:
                player2B = round(float(playerDoubles)/float(playerHits),3)
            except:
                player2B = 0

            try:
                player3B = round(float(playerTriples)/float(playerHits),3)
            except:
                player3B = 0

            try:
                playerHR = round(float(playerHomeRuns)/float(playerHits),3)
            except:
                playerHR = 0

            try:
                playerWalkRate = round((playerWalks + playerHBP )/(playerWalks + playerHBP + playerAtBats),3)
            except:
                playerWalkRate = 0

            try:
                playerStrikeOutRate = round(float(playerStrikeOuts) / float(playerAtBats),3)
            except:
                playerStrikeOutRate = 0

            if self.TopTeam == True:
                self.topTeamLineUp.append((s,playerVsLeft,playerVsRight,player1B,player2B,player3B,playerHR,playerWalkRate,playerStrikeOutRate))
            elif self.TopTeam == False:
                self.botTeamLineUp.append((s,playerVsLeft,playerVsRight,player1B,player2B,player3B,playerHR,playerWalkRate,playerStrikeOutRate))

            time.sleep(1)

