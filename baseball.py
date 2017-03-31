#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      aketay
#
# Created:     07/04/2014
# Copyright:   (c) aketay 2014
#-------------------------------------------------------------------------------
import random
import time
import readCSV
import checkplayer
import readZIPS
import baseballreference2
import FDLoader
import csv
import numpy

from fuzzywuzzy import fuzz

from collections import Counter

class LeagueAverage:
    def __init__(self,leagueOBPAL,leagueOBPAR,leagueSingleRate,leagueDoubleRate,leagueTripleRate,leagueHomeRunRate, leagueWalkRate, leagueStrikeOutRate):
        self.leagueOBPAL = leagueOBPAL
        self.leagueOBPAR = leagueOBPAR
        self.leagueSingleRate = leagueSingleRate
        self.leagueDoubleRate = leagueDoubleRate
        self.leagueTripleRate = leagueTripleRate
        self.leagueHomeRunRate = leagueHomeRunRate
        self.leagueWalkRate = leagueWalkRate
        self.leagueStrikeOutRate = leagueStrikeOutRate

class Batter:
    def __init__(self,playerName,playerOBPL,playerOBPR,playerSingleRate, playerDoubleRate, playerTripleRate, playerHomeRunRate, playerWalkRate, playerStrikeOutRate):
        self.playerName = playerName
        self.playerOBPL = playerOBPL
        self.playerOBPR = playerOBPR
        self.playerBasePosition = 0
        self.playerHitCount = 0
        self.playerWalkCount = 0
        self.playerSingleCount = 0
        self.playerDoubleCount = 0
        self.playerTripleCount = 0
        self.playerHomeRunCount = 0
        self.playerRunsCount = 0
        self.playerRBICount = 0
        self.playerOutCount = 0
        self.playerSingleRate = playerSingleRate
        self.playerDoubleRate = playerDoubleRate
        self.playerTripleRate = playerTripleRate
        self.playerHomeRunRate = playerHomeRunRate
        self.playerWalkRate = playerWalkRate
        self.playerStrikeOutRate = playerStrikeOutRate
        self.playerStrikeOutCount = 0

class Pitcher:
    def __init__(self, pitcherType, pitcherInnings, pitcherName,pitcherHandedness,pitcherOBPAL,pitcherOBPAR, pitcherSingleRate,pitcherDoubleRate,pitcherTripleRate,pitcherHomeRunRate, pitcherWalkRate, pitcherStrikeOutRate):
        self.pitcherName = pitcherName
        self.pitcherOBPAL = pitcherOBPAL
        self.pitcherOBPAR = pitcherOBPAR
        self.pitcherHandedness = pitcherHandedness
        self.pitcherSingleRate = pitcherSingleRate
        self.pitcherDoubleRate = pitcherDoubleRate
        self.pitcherTripleRate = pitcherTripleRate
        self.pitcherHomeRunRate = pitcherHomeRunRate
        self.pitcherWalkRate = pitcherWalkRate
        self.pitcherStrikeOutRate = pitcherStrikeOutRate
        #Type of Pitcher (i.e. Starter, RP, Closer, etc)
        self.pitcherType = pitcherType
        #How many innings on average this pitcher pitches
        self.pitcherInnings = pitcherInnings
        #Has pitcher pitched yet?
        self.hasPitched = 0
        self.inningsPitched = 0
        self.gotWin = False
        self.earnedRuns = 0
        self.strikeOuts = 0
        self.winCount = 0

class Game:
    def __init__(self):
        self.inning = 1
        self.homeScore = 0
        self.awayScore = 0
        #inningHalf 1 Top / 0 Bot
        self.inningHalf = 1
        self.outs = 0
        self.gameOver = 0
        self.homeBatter = 0
        self.awayBatter = 0
        self.currentPitcher = None


        self.setPitcher()

        self.tempLastAwayPitcher = None
        self.tempLastHomePitcher = None
        self.gameLocation = None
        self.homeWinCount = 0
        self.awayWinCount = 0




    def gameReset(self):
        self.inning = 1
        self.homeScore = 0
        self.awayScore = 0
        #inningHalf 1 Top / 0 Bot
        self.inningHalf = 1
        self.outs = 0
        self.gameOver = 0
        self.homeBatter = 0
        self.awayBatter = 0
        self.currentPitcher = None

        self.tempLastAwayPitcher = None
        self.tempLastHomePitcher = None
        self.setPitcher()

        #Reset all base position to 0
        for item in homeTeam:
            item.playerBasePosition = 0

            item.playerSingleCount = 0
            item.playerDoubleCount = 0
            item.playerTripleCount = 0
            item.playerHomeRunCount = 0
            item.playerWalkCount = 0
            item.playerHitCount = 0
            item.playerOutCount = 0
            item.playerRunsCount = 0
            item.playerRBICount = 0
            item.playerStrikeOutCount = 0

        for item in awayTeam:
            item.playerBasePosition = 0

            item.playerSingleCount = 0
            item.playerDoubleCount = 0
            item.playerTripleCount = 0
            item.playerHomeRunCount = 0
            item.playerWalkCount = 0
            item.playerHitCount = 0
            item.playerOutCount = 0
            item.playerRunsCount = 0
            item.playerRBICount = 0
            item.playerStrikeOutCount = 0

        #Reset all pitchers to no win
        for item in homeTeamPitchers:
            if item.gotWin == True:
                item.winCount +=1

            item.gotWin = False
            item.hasPitched = 0
        for item in awayTeamPitchers:
            if item.gotWin == True:
                item.winCount +=1
            item.gotWin = False
            item.hasPitched = 0

    def setPitcher(self):

        #When going to change pitchers, check to see if there is a winner
        if self.awayScore > self.homeScore and not any(person for person in awayTeamPitchers if person.gotWin == True):
            try:
                self.tempLastAwayPitcher.gotWin = True
            except:
                pass
        elif self.awayScore < self.homeScore and not any(person for person in homeTeamPitchers if person.gotWin == True):
            try:
                self.tempLastHomePitcher.gotWin = True
            except:
                pass

        if self.inningHalf == 1 and self.gameOver == 0:
            #Since Top is batting, away is pitching

            #Get the starting pitcher
            if self.inning <= next(person.pitcherInnings for person in awayTeamPitchers if person.pitcherType == "SP"):
                self.currentPitcher = next(person for person in awayTeamPitchers if person.pitcherType == "SP")
                self.currentPitcher.hasPitched = 1
                self.currentPitcher.inningsPitched +=1
                self.tempLastAwayPitcher = self.currentPitcher
            else:
                bullpenList = []
                if self.inning >= 9 and self.awayScore>= self.homeScore:
                    #Set the closer
                    self.currentPitcher = next(person for person in awayTeamPitchers if person.pitcherType == "C" )
                    self.currentPitcher.hasPitched = 1
                    self.currentPitcher.inningsPitched +=1
                    self.tempLastAwayPitcher = self.currentPitcher
                elif any(person for person in awayTeamPitchers if person.pitcherType == "C" and person.hasPitched != 1):
                    for item in awayTeamPitchers:
                        if item.pitcherType == "RP" and item.hasPitched == 0:
                            bullpenList.append(item)
                    if len(bullpenList) >0:
                        self.currentPitcher = random.choice(bullpenList)
                        self.currentPitcher.hasPitched = 1
                        self.currentPitcher.inningsPitched +=1
                        self.tempLastAwayPitcher = self.currentPitcher
                    else:
                        self.currentPitcher = self.tempLastAwayPitcher
                        self.currentPitcher.inningsPitched +=1



        elif self.inningHalf == 0 and self.gameOver ==0:
            if self.inning <= next(person.pitcherInnings for person in homeTeamPitchers if person.pitcherType == "SP"):
                self.currentPitcher = next(person for person in homeTeamPitchers if person.pitcherType == "SP")
                self.currentPitcher.hasPitched = 1
                self.currentPitcher.inningsPitched +=1
                self.tempLastHomePitcher = self.currentPitcher

            else:
                bullpenList = []
                if self.inning >= 9 and self.homeScore>= self.awayScore:
                    #Set the closer
                    self.currentPitcher = next(person for person in homeTeamPitchers if person.pitcherType == "C" )
                    self.currentPitcher.hasPitched = 1
                    self.currentPitcher.inningsPitched +=1
                    self.tempLastHomePitcher = self.currentPitcher

                elif any(person for person in homeTeamPitchers if person.pitcherType == "C" and person.hasPitched != 1):

                    for item in homeTeamPitchers:
                        if item.pitcherType == "RP" and item.hasPitched == 0:
                            bullpenList.append(item)
                    if len(bullpenList) >0:
                        self.currentPitcher = random.choice(bullpenList)
                        self.currentPitcher.hasPitched = 1
                        self.currentPitcher.inningsPitched +=1
                        self.tempLastHomePitcher = self.currentPitcher
                    else:
                        self.currentPitcher = self.tempLastHomePitcher
                        self.currentPitcher.inningsPitched +=1


        #Check to see if pitcher should be replaced


    def pitch(self):
        #if home team is hitting

        self.tempBatterOBPA = self.batterOBPA()

        self.tempBatterDoubleRateA = round(self.batterDoubleRateA(),3)
        self.tempBatterTripleRateA = round(self.batterTripleRateA(),3)
        self.tempBatterHomeRunRateA  = round(self.batterHomeRunRateA(),3)



        self.tempBatterSingleRateA = round((1 - self.tempBatterHomeRunRateA - self.tempBatterTripleRateA - self.tempBatterDoubleRateA),3)


        if self.inningHalf == 1:


            if self.outs != 3:
                pitchChance = random.random()
                hitChance = random.random()
                walkChance = random.random()

                #pitch

                if pitchChance <= self.tempBatterOBPA:

                    if walkChance <= homeTeam[self.homeBatter % 9].playerWalkRate:
                        #Player Walks
                        self.baseCount("Walk")
                        homeTeam[self.homeBatter % 9].playerWalkCount +=1
                        self.homeBatter +=1
                    else:

                        if hitChance < self.tempBatterSingleRateA:
                            self.baseCount("Single")
                            homeTeam[self.homeBatter % 9].playerHitCount +=1
                            self.homeBatter +=1
                        elif hitChance > self.tempBatterSingleRateA and hitChance < (self.tempBatterSingleRateA + self.tempBatterDoubleRateA):
                            self.baseCount("Double")
                            homeTeam[self.homeBatter % 9].playerHitCount +=1
                            self.homeBatter +=1
                        elif hitChance > (self.tempBatterSingleRateA + self.tempBatterDoubleRateA) and hitChance < (self.tempBatterSingleRateA + self.tempBatterDoubleRateA + self.tempBatterTripleRateA):
                            self.baseCount("Triple")
                            homeTeam[self.homeBatter % 9].playerHitCount +=1
                            self.homeBatter +=1
                        elif hitChance > (self.tempBatterSingleRateA + self.tempBatterDoubleRateA + self.tempBatterTripleRateA) and hitChance <(self.tempBatterSingleRateA + self.tempBatterDoubleRateA + self.tempBatterTripleRateA + self.tempBatterHomeRunRateA):
                            self.baseCount("Home Run")
                            homeTeam[self.homeBatter % 9].playerHitCount +=1
                            self.homeBatter +=1
                else:
                    self.outType()
                    self.outs +=1
                    self.homeBatter +=1

        #if away team is hitting
        elif self.inningHalf == 0:

            if self.outs != 3:
                pitchChance = random.random()
                hitChance = random.random()
                walkChance = random.random()

                #pitch
                #if the player gets on base, then decide what it is

                if pitchChance <= self.tempBatterOBPA:
                    if walkChance <= awayTeam[self.awayBatter % 9].playerWalkRate:
                        #Player Walks
                        self.baseCount("Walk")
                        awayTeam[self.awayBatter % 9].playerWalkCount +=1
                        self.awayBatter +=1
                    else:
                        if hitChance < self.tempBatterSingleRateA:
                            self.baseCount("Single")
                            awayTeam[self.awayBatter % 9].playerHitCount +=1
                            self.awayBatter +=1
                        elif hitChance > self.tempBatterSingleRateA and hitChance < (self.tempBatterSingleRateA + self.tempBatterDoubleRateA):
                            self.baseCount("Double")
                            awayTeam[self.awayBatter % 9].playerHitCount +=1
                            self.awayBatter +=1
                        elif hitChance > (self.tempBatterSingleRateA + self.tempBatterDoubleRateA) and hitChance < (self.tempBatterSingleRateA + self.tempBatterDoubleRateA + self.tempBatterTripleRateA):
                            self.baseCount("Triple")
                            awayTeam[self.awayBatter % 9].playerHitCount +=1
                            self.awayBatter +=1
                        elif hitChance > (self.tempBatterSingleRateA + self.tempBatterDoubleRateA + self.tempBatterTripleRateA) and hitChance <(self.tempBatterSingleRateA + self.tempBatterDoubleRateA + self.tempBatterTripleRateA + self.tempBatterHomeRunRateA):
                            self.baseCount("Home Run")
                            awayTeam[self.awayBatter % 9].playerHitCount +=1
                            self.awayBatter +=1
                else:
                    self.outType()
                    self.outs +=1
                    self.awayBatter +=1


    def outType(self):
        strikeOutChance = random.random()
        if self.inningHalf == 1:
            if strikeOutChance <= homeTeam[self.homeBatter % 9].playerStrikeOutRate:
                homeTeam[self.homeBatter % 9].playerStrikeOutCount +=1
                self.currentPitcher.strikeOuts +=1
            else:
                homeTeam[self.homeBatter % 9].playerOutCount +=1
        elif self.inningHalf == 0:
            if strikeOutChance <= awayTeam[self.awayBatter % 9].playerStrikeOutRate:
                awayTeam[self.awayBatter % 9].playerStrikeOutCount +=1
                self.currentPitcher.strikeOuts +=1
            else:
                awayTeam[self.awayBatter % 9].playerOutCount +=1

    def baseCount(self,hitType):
         #if home team is hitting
        if self.inningHalf == 1:
            #if hits a single
            if hitType == "Single":

                for items in homeTeam:
                    if items.playerBasePosition != 0:
                        items.playerBasePosition +=1
                homeTeam[self.homeBatter % 9].playerBasePosition +=1
                homeTeam[self.homeBatter % 9].playerSingleCount +=1
            elif hitType == "Double":

                for items in homeTeam:
                    if items.playerBasePosition != 0:
                        items.playerBasePosition +=3
                homeTeam[self.homeBatter % 9].playerBasePosition +=2
                homeTeam[self.homeBatter % 9].playerDoubleCount += 1
            elif hitType == "Triple":

                for items in homeTeam:
                    if items.playerBasePosition != 0:
                        items.playerBasePosition +=3
                homeTeam[self.homeBatter % 9].playerBasePosition +=3
                homeTeam[self.homeBatter % 9].playerTripleCount +=1
            elif hitType == "Home Run":

                for items in homeTeam:
                    if items.playerBasePosition != 0:
                        items.playerBasePosition = 4
                homeTeam[self.homeBatter % 9].playerBasePosition = 4
                homeTeam[self.homeBatter % 9].playerHomeRunCount +=1
            elif hitType =="Walk":
                #if bases are loaded
                if any(item.playerBasePosition == 1 for item in homeTeam) and any(item.playerBasePosition == 2 for item in homeTeam) and any(item.playerBasePosition == 3 for item in homeTeam):
                    for item in homeTeam:
                        item.playerBasePosition +=1
                    homeTeam[self.homeBatter % 9].playerBasePosition = 1
                #if there is a guy on 1st and 2nd then
                elif any(item.playerBasePosition == 1 for item in homeTeam) and any (item.playerBasePosition == 2 for item in homeTeam):
                    for item in homeTeam:
                        item.playerBasePosition +=1
                    homeTeam[self.homeBatter % 9].playerBasePosition = 1
                #if there is a guy on 1st and 3rd then
                elif any(item.playerBasePosition == 1 for item in homeTeam) and any (item.playerBasePosition == 3 for item in homeTeam):
                    for item in homeTeam:
                        if item.playerBasePosition == 1:
                            item.playerBasePosition = 2
                    homeTeam[self.homeBatter % 9].playerBasePosition = 1
                else:
                    homeTeam[self.homeBatter % 9].playerBasePosition = 1
            #Score Runners
            for items in homeTeam:
                if items.playerBasePosition >= 4:
                    items.playerBasePosition = 0
                    if homeTeam[self.homeBatter % 9].playerName == items.playerName:
                        homeTeam[self.homeBatter % 9].playerRunsCount +=1
                    else:
                        homeTeam[self.homeBatter % 9].playerRBICount +=1
                        items.playerRunsCount +=1
                    self.homeScore +=1
                    self.currentPitcher.earnedRuns +=1
                    #if other team takes lead then they can't get credit for win
                    if self.homeScore > self.awayScore:
                        for item in awayTeamPitchers:
                            item.gotWin = False

            if self.inning >= 9:
                self.checkGameOver()

        #if away team is hitting
        elif self.inningHalf == 0:
            if hitType == "Single":
                for items in awayTeam:
                    if items.playerBasePosition !=0:
                        items.playerBasePosition +=1
                awayTeam[self.awayBatter % 9].playerBasePosition +=1
                awayTeam[self.awayBatter % 9].playerSingleCount +=1
            elif hitType == "Double":
                 for items in awayTeam:
                    if items.playerBasePosition !=0:
                        items.playerBasePosition +=2
                 awayTeam[self.awayBatter % 9].playerBasePosition +=2
                 awayTeam[self.awayBatter % 9].playerDoubleCount +=1
            elif hitType == "Triple":
                for items in awayTeam:
                    if items.playerBasePosition !=0:
                        items.playerBasePosition +=3
                awayTeam[self.awayBatter % 9].playerBasePosition +=3
                awayTeam[self.awayBatter % 9].playerTripleCount +=1
            elif hitType == "Home Run":
                for items in awayTeam:
                    if items.playerBasePosition != 0:
                        items.playerBasePosition = 4
                awayTeam[self.awayBatter % 9].playerBasePosition = 4
                awayTeam[self.awayBatter % 9].playerHomeRunCount +=1
            elif hitType =="Walk":
                #if bases are loaded

                if any(item.playerBasePosition == 1 for item in awayTeam) and any(item.playerBasePosition == 2 for item in awayTeam) and any(item.playerBasePosition == 3 for item in awayTeam):
                    for item in awayTeam:
                        item.playerBasePosition +=1
                    awayTeam[self.awayBatter % 9].playerBasePosition = 1
                #if there is a guy on 1st and 2nd then
                elif any(item.playerBasePosition == 1 for item in awayTeam) and any (item.playerBasePosition == 2 for item in awayTeam):
                    for item in awayTeam:
                        item.playerBasePosition +=1
                    awayTeam[self.awayBatter % 9].playerBasePosition = 1
                #if there is a guy on 1st and 3rd then
                elif any(item.playerBasePosition == 1 for item in awayTeam) and any (item.playerBasePosition == 3 for item in awayTeam):
                    for item in awayTeam:
                        if item.playerBasePosition == 1:
                            item.playerBasePosition = 2
                    awayTeam[self.awayBatter % 9].playerBasePosition = 1
                else:
                    awayTeam[self.awayBatter % 9].playerBasePosition = 1

           #Score Runners
            for items in awayTeam:
                if items.playerBasePosition >= 4:
                    items.playerBasePosition = 0
                    if awayTeam[self.awayBatter % 9].playerName == items.playerName:
                        awayTeam[self.awayBatter % 9].playerRunsCount +=1
                    else:
                        awayTeam[self.homeBatter % 9].playerRBICount +=1
                        items.playerRunsCount +=1
                    self.awayScore +=1
                    self.currentPitcher.earnedRuns +=1
                    #if other team takes lead then they can't get credit for win
                    if self.awayScore > self.homeScore:
                        for item in homeTeamPitchers:
                            item.gotWin = False
            if self.inning >= 9:
                self.checkGameOver()

    def batterOBPA(self):
        #Get Adjusted OBP using Log-5 Formula

        #if top half
        if self.inningHalf == 1:
            #test for handedness
            if self.currentPitcher.pitcherHandedness =="R":
                BA = homeTeam[self.homeBatter % 9].playerOBPR
                PA = self.currentPitcher.pitcherOBPAR
                result = ((BA * PA)/leagueAverages.leagueOBPAR)/(((BA * PA)/leagueAverages.leagueOBPAR)+((1-BA)*(1-PA)/(1-leagueAverages.leagueOBPAR)))* float(parkFactors.parkDict[self.gameLocation][6])
            else:
                BA = homeTeam[self.homeBatter % 9].playerOBPL
                PA = self.currentPitcher.pitcherOBPAL

                result = ((BA * PA)/leagueAverages.leagueOBPAL)/(((BA * PA)/leagueAverages.leagueOBPAL)+((1-BA)*(1-PA)/(1-leagueAverages.leagueOBPAL)))* float(parkFactors.parkDict[self.gameLocation][5])

            return result
        elif self.inningHalf == 0:
            if self.currentPitcher.pitcherHandedness =="R":
                BA = awayTeam[self.awayBatter % 9].playerOBPR
                PA = self.currentPitcher.pitcherOBPAR
                result = ((BA * PA)/leagueAverages.leagueOBPAR)/(((BA * PA)/leagueAverages.leagueOBPAR)+((1-BA)*(1-PA)/(1-leagueAverages.leagueOBPAR)))* float(parkFactors.parkDict[self.gameLocation][6])
            else:
                BA = awayTeam[self.awayBatter % 9].playerOBPL
                PA = self.currentPitcher.pitcherOBPAL
                result = ((BA * PA)/leagueAverages.leagueOBPAL)/(((BA * PA)/leagueAverages.leagueOBPAL)+((1-BA)*(1-PA)/(1-leagueAverages.leagueOBPAL)))* float(parkFactors.parkDict[self.gameLocation][5])

            return result

    def batterSingleRateA(self):
        #Get Adjusted Single Rate using Log-5 Formula

        #if top half
        if self.inningHalf == 1:
            BA = homeTeam[self.homeBatter % 9].playerSingleRate
            PA = self.currentPitcher.pitcherSingleRate
            try:
                result = ((BA * PA)/leagueAverages.leagueSingleRate)/(((BA * PA)/leagueAverages.leagueSingleRate)+((1-BA)*(1-PA)/(1-leagueAverages.leagueSingleRate)))
                return result
            except:
                return 0
        elif self.inningHalf == 0:
            BA = awayTeam[self.awayBatter % 9].playerSingleRate
            PA = self.currentPitcher.pitcherSingleRate
            try:
                return ((BA * PA)/leagueAverages.leagueSingleRate)/(((BA * PA)/leagueAverages.leagueSingleRate)+((1-BA)*(1-PA)/(1-leagueAverages.leagueSingleRate)))
            except:
                return 0
    def batterDoubleRateA(self):
        #Get Adjusted Single Rate using Log-5 Formula

        #if top half
        if self.inningHalf == 1:
            BA = homeTeam[self.homeBatter % 9].playerDoubleRate
            PA = self.currentPitcher.pitcherDoubleRate

            try:
                result = ((BA * PA)/leagueAverages.leagueDoubleRate)/(((BA * PA)/leagueAverages.leagueDoubleRate)+((1-BA)*(1-PA)/(1-leagueAverages.leagueDoubleRate)))* float(parkFactors.parkDict[self.gameLocation][3])
                return result
            except:
                return 0
        elif self.inningHalf == 0:
            BA = awayTeam[self.awayBatter % 9].playerDoubleRate
            PA = self.currentPitcher.pitcherDoubleRate
            try:
                return ((BA * PA)/leagueAverages.leagueDoubleRate)/(((BA * PA)/leagueAverages.leagueDoubleRate)+((1-BA)*(1-PA)/(1-leagueAverages.leagueDoubleRate)))* float(parkFactors.parkDict[self.gameLocation][3])
            except:
                return 0

    def batterTripleRateA(self):
        #Get Adjusted Single Rate using Log-5 Formula

        #if top half
        if self.inningHalf == 1:
            BA = homeTeam[self.homeBatter % 9].playerTripleRate
            PA = self.currentPitcher.pitcherTripleRate
            try:
                result = ((BA * PA)/leagueAverages.leagueTripleRate)/(((BA * PA)/leagueAverages.leagueTripleRate)+((1-BA)*(1-PA)/(1-leagueAverages.leagueTripleRate))) * float(parkFactors.parkDict[self.gameLocation][4])
            except:
                result = 0

            return result
        elif self.inningHalf == 0:
            BA = awayTeam[self.awayBatter % 9].playerTripleRate
            PA = self.currentPitcher.pitcherTripleRate
            try:
                return ((BA * PA)/leagueAverages.leagueTripleRate)/(((BA * PA)/leagueAverages.leagueTripleRate)+((1-BA)*(1-PA)/(1-leagueAverages.leagueTripleRate))) * float(parkFactors.parkDict[self.gameLocation][4])
            except:
                return 0

    def batterHomeRunRateA(self):
        #Get Adjusted Single Rate using Log-5 Formula

        #if top half
        if self.inningHalf == 1:
            BA = homeTeam[self.homeBatter % 9].playerHomeRunRate
            PA = self.currentPitcher.pitcherHomeRunRate
            try:
                result = ((BA * PA)/leagueAverages.leagueHomeRunRate)/(((BA * PA)/leagueAverages.leagueHomeRunRate)+((1-BA)*(1-PA)/(1-leagueAverages.leagueHomeRunRate))) * float(parkFactors.parkDict[self.gameLocation][0])
                return result
            except:
                return 0

        elif self.inningHalf == 0:
            BA = awayTeam[self.awayBatter % 9].playerHomeRunRate
            PA = self.currentPitcher.pitcherHomeRunRate
            try:
                return ((BA * PA)/leagueAverages.leagueHomeRunRate)/(((BA * PA)/leagueAverages.leagueHomeRunRate)+((1-BA)*(1-PA)/(1-leagueAverages.leagueHomeRunRate))) * float(parkFactors.parkDict[self.gameLocation][0])
            except:
                return 0


    def doSequence(self):
        #if the inning is still going

        if self.inning >=9:
            self.checkGameOver()

        if self.outs < 3 and self.gameOver !=1:


            self.pitch()


        #if there are three outs in an inning and the game is not over
        if self.outs >=3 and self.gameOver ==0:

            #Check to see if game over
            if self.inning >=9:
                self.checkGameOver()
            #if not game over then
            if currentGame.gameOver == 0:
                #if top half
                if self.inningHalf == 1:

                    self.inningHalf = 0
                    #Switch pitchers
                    self.setPitcher()
                  #  print "Inning: " + str(self.inning)
                  #  print "Home: " + str(self.homeScore) + " Away: " + str(self.awayScore)
                    self.outs = 0
                    for items in homeTeam:
                        items.playerBasePosition = 0

                #if bottom half
                elif self.inningHalf == 0:
                   # print "Inning: " + str(self.inning)
                   # print "Home: " + str(self.homeScore) + " Away: " + str(self.awayScore)
                    self.inning +=1
                    self.inningHalf = 1
                    #Switch pitchers
                    self.setPitcher()

                    self.outs = 0
                    for items in awayTeam:
                        items.playerBasePosition = 0

        #Check if game is over
    def checkGameOver(self):
      if self.inning >=9 and self.inningHalf == 0:
        if self.homeScore < self.awayScore:
            self.gameOver = 1
            if self.homeScore > self.awayScore:
                self.homeWinCount +=1
            elif self.awayScore > self.homeScore:
                self.awayWinCount +=1

          #  print "Teams were tied, and away scored a run in the bottom half, game over!"

      if self.inning >=9 and self.inningHalf == 0 and self.outs >=3:
        if self.homeScore > self.awayScore:
            self.gameOver = 1
            if self.homeScore > self.awayScore:
                self.homeWinCount +=1
            elif self.awayScore > self.homeScore:
                self.awayWinCount +=1
           # print "Away didn't tie it up or take the lead, game over!"
      if self.inning>=9 and self.inningHalf == 1 and self.outs >=3:
        if self.homeScore < self.awayScore:
            self.gameOver = 1
            if self.homeScore > self.awayScore:
                self.homeWinCount +=1
            elif self.awayScore > self.homeScore:
                self.awayWinCount +=1
            #print "Home Team didn't tie it up or take the lead, game over!"

#Write Final Data to csv
def writeFinalPlayerInfo():
        f = open(r'/Users/Aketay/Desktop/FDFinalInfo.csv', 'a')

        for item in finalPlayerList.keys():
            for player in finalComparison.fdSalCapDict.keys():
                if fuzz.ratio(playerStats.playerNameList[item],player) > 85:
                    tempRow = [playerStats.playerNameList[item],finalComparison.fdSalCapDict[player][0],finalComparison.fdSalCapDict[player][1],finalPlayerList[item]]
                    wr = csv.writer(f, dialect='excel')
                    wr.writerow(tempRow)

        f.close()

def writePlayerStatInfo():
        #f = open(r'/Users/Aketay/Desktop/PlayerStatInfo.csv', 'a')

        for item in playerStats.topTeamLineUp:
            print item


                    # tempRow = [playerStats.playerNameList[item],finalComparison.fdSalCapDict[player][0],finalComparison.fdSalCapDict[player][1],finalPlayerList[item]]
                    # wr = csv.writer(f, dialect='excel')
                    # wr.writerow(tempRow)
        for item in playerStats.botTeamLineUp:
            print item

        for item in playerStats.topTeamPitchingLineUp:
            print item


        for item in playerStats.botTeamPitchingLineUp:
            print item

        # f.close()

def playerStandardDev():
    for item in homeTeam:
        tempFDPoints = item.playerSingleCount + (2* item.playerDoubleCount) +(3 * item.playerTripleCount) +(4 * item.playerHomeRunCount) + item.playerRunsCount + item.playerRBICount + item.playerWalkCount -(0.25 * item.playerStrikeOutCount) - (0.25 * item.playerOutCount)
        if item.playerName in topTeamBatterSDChart:
            topTeamBatterSDChart[item.playerName].append(tempFDPoints)
        else:
            topTeamBatterSDChart[item.playerName] = [ tempFDPoints ]


def getStandardDev():
    for item in homeTeam:
      print item.playerName,"Average: ", numpy.average(topTeamBatterSDChart[item.playerName]),"Standard Dev.:",  numpy.std(topTeamBatterSDChart[item.playerName])




topTeamBatterSDChart = dict()
topTeamBatterFinalSD = []

#Initialize the list of objects for home/away batters
homeTeam =[]
awayTeam =[]

#Get the teams from the Line-up Spreadsheet
parkFactors = readCSV.GetTeams()

#Load Park Factors
parkFactors.getParkFactors()


#Create PlayerStats Class
playerStats = checkplayer.PlayerStats()

#
projectionsZIPS = readZIPS.GetTeams()

#Gets the League Averages from Baseball-Reference
leagueAveragesGrabber = baseballreference2.BaseballReference()
leagueAveragesGrabber.getLeagueAverages()

for item in parkFactors.topTeam:
    playerStats.checkPlayerStatType(item)

playerStats.TopTeam = False

for item in parkFactors.botTeam:
    playerStats.checkPlayerStatType(item)

for item in playerStats.topTeamLineUp:
    homeTeam.append(Batter(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]))

for item in playerStats.botTeamLineUp:
    awayTeam.append(Batter(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8]))


#Initialize the list of objects for home/away pitchers
homeTeamPitchers = []
awayTeamPitchers = []

playerStats.TopTeam = True
for item in parkFactors.topTeamPitchers:
    playerStats.checkPitcherStatsType(item[0],item[1])

playerStats.TopTeam = False
for item in parkFactors.botTeamPitchers:
    playerStats.checkPitcherStatsType(item[0],item[1])


#(Pitcher Type, Innings, Name, Handedness, OBPAL,OBPAR, Single, Double, Triple, HR, Walk, Strike Out)
for item in playerStats.topTeamPitchingLineUp:
    homeTeamPitchers.append(Pitcher(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11]))


for item in playerStats.botTeamPitchingLineUp:
    awayTeamPitchers.append(Pitcher(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11]))


writePlayerStatInfo()

#Need an error checking module!!!!!

#(Pitcher Type, Innings, Name, Handedness, OBPAL,OBPAR, Single, Double, Triple, HR, Walk, Strike Out):


#(Player name, OBP-left,OBP-Right, Single, Double, Triple, HR, Walk, Strike Out)





leagueAverages = LeagueAverage(leagueAveragesGrabber.leagueAverageDict['OBPL'],leagueAveragesGrabber.leagueAverageDict['OBPR'],leagueAveragesGrabber.leagueAverageDict['1BRate'],leagueAveragesGrabber.leagueAverageDict['2BRate'],leagueAveragesGrabber.leagueAverageDict['3BRate'],leagueAveragesGrabber.leagueAverageDict['HRRate'],leagueAveragesGrabber.leagueAverageDict['WalkRate'],leagueAveragesGrabber.leagueAverageDict['SORate'])

#initialize the game sim
currentGame = Game()

#Set Game Location
currentGame.gameLocation = parkFactors.location

#Keep track of game stats
gameScores = []

##print "Printing dictionary"
##
##for item in playerStats.playerNameList.keys():
##    print playerStats.playerNameList[item]
##    for thing in projectionsZIPS.my_data:
##        if thing[0] == playerStats.playerNameList[item]:
##            print str(item) + " : " + str(thing)

#Game Play loop. If game is over it stops running


for x in range(0,10000):
    while currentGame.gameOver == 0:
        currentGame.doSequence()
    gameScores.append(currentGame.inning)
    playerStandardDev()
    currentGame.gameReset()
   # time.sleep()

getStandardDev()

time.sleep(30)

c = Counter(gameScores)

print "Percent of Games going to 9 Innings: " + str(float(c[9])/float(len(gameScores)))

print "Percent of Games going to 10 Innings: " + str(float(c[10])/float(len(gameScores)))

print "Percent of Games going to 11 Innings: " + str(float(c[11])/float(len(gameScores)))

print "Top Win %: " ,currentGame.homeWinCount/10000 , "Away Win %: ", currentGame.awayWinCount/10000

print currentGame.homeWinCount
print currentGame.awayWinCount

temptotalcount = 0
for item in c.keys():
    if item > 11:
      temptotalcount += c[item]

print "Percent of Games going to 12+ Innings: " + str(float(temptotalcount)/float(len(gameScores)))

finalPlayerList = {}

for item in homeTeam:
    woozle = item.playerOutCount + item.playerWalkCount + item.playerStrikeOutCount + item.playerHitCount
    tempFDPoints = item.playerSingleCount + (2* item.playerDoubleCount) +(3 * item.playerTripleCount) +(4 * item.playerHomeRunCount) + item.playerRunsCount + item.playerRBICount + item.playerWalkCount -(0.25 * item.playerStrikeOutCount) - (0.25 * item.playerOutCount)
    finalPlayerList[str(item.playerName)] = str(round((tempFDPoints/10000),2))

for item in awayTeam:
    woozle = item.playerOutCount + item.playerWalkCount + item.playerStrikeOutCount + item.playerHitCount
    tempFDPoints = item.playerSingleCount + (2* item.playerDoubleCount) +(3 * item.playerTripleCount) +(4 * item.playerHomeRunCount) + item.playerRunsCount + item.playerRBICount + item.playerWalkCount -(0.25 * item.playerStrikeOutCount) - (0.25 * item.playerOutCount)
    finalPlayerList[str(item.playerName)] = str(round((tempFDPoints/10000),2))

for item in homeTeamPitchers:
    tempFDPoints = item.inningsPitched + item.strikeOuts +(4 * item.winCount) - item.earnedRuns
    finalPlayerList[str(item.pitcherName)] = str(round((tempFDPoints/10000),2))

for item in awayTeamPitchers:
    tempFDPoints = item.inningsPitched + item.strikeOuts +(4 * item.winCount) - item.earnedRuns
    finalPlayerList[str(item.pitcherName)] = str(round((tempFDPoints/10000),2))

finalComparison = FDLoader.FDSALCAP()

writeFinalPlayerInfo()
