import datetime
import time
import urllib2
import re
from bs4 import BeautifulSoup
from datetime import timedelta, date
from urllib2 import HTTPError

#Initialize Variables

gameMatrix = []
gameList =[]
# Get Webpage Data
class GetData:
    def __init__(self):
        self.awayTeam = []
        self.homeTeam = []


    def getplayerstats(self,s):
        websiteString = "http://espn.go.com/mlb/player/splits/_/id/" + s + "/type/batting3/"
        try:
            sock2 = urllib2.urlopen(websiteString)
            print websiteString
        except urllib2.HTTPError, e:
            urlerrorCode = e.code
            print urlerrorCode
            print e.fp.read()

        dataslerp = sock2.read()

        dataderp = dataslerp.replace('&nbsp;', '')

        soup = BeautifulSoup(dataderp)

        table = soup.find_all("table", { "class" : "tablehead" })

        rows = table[0].find_all("tr")

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
            if cells[0].text =="vs. Right":
                playerVsRight = float(cells[14].text)



        try:
            playerSingles = (playerHits - playerDoubles - playerTriples - playerHomeRuns)
        except:
            print "Shwat?"
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


        if self.homeadd == 1:
            self.homeTeam.append([s,playerVsLeft,playerVsRight,player1B,player2B,player3B,playerHR,playerWalkRate,playerStrikeOutRate])
        elif self.homeadd == 0:
            self.awayTeam.append([s,playerVsLeft,playerVsRight,player1B,player2B,player3B,playerHR,playerWalkRate,playerStrikeOutRate])

        time.sleep(1)


    def getteamdata(self):
        websiteString = "http://espn.go.com/mlb/preview?id=" + self.s
        try:
            sock2 = urllib2.urlopen(websiteString)
            print "Opened:" + " " + websiteString
        except urllib2.HTTPError, e:
            urlerrorCode = e.code
            print urlerrorCode
            print e.fp.read()

        dataslerp = sock2.read()

        dataderp = dataslerp.replace('&nbsp;', '')

        soup = BeautifulSoup(dataderp)

        table = soup.find_all("div", { "class" : "mod-container mod-open mlb-box mod-open-gamepack" })
        rowCounter = 0
        playerList = []

        for item in table[1].find_all("td"):
            if rowCounter % 3 == 0:
                rowNum = item.text
                rowCounter +=1
            elif rowCounter % 3 == 1:
                for link in item.find_all('a'):
                    leftPlayer = re.findall(r'\d+',link['href'].replace("http://espn.go.com/mlb/player/_/id/",""))
                rowCounter +=1
            elif rowCounter % 3 == 2:
                for link in item.find_all('a'):
                    rightPlayer = re.findall(r'\d+',link['href'].replace("http://espn.go.com/mlb/player/_/id/",""))
                playerList.append([rowNum,leftPlayer[0],rightPlayer[0]])
                rowCounter +=1

        for item in playerList:
            self.homeadd = 1

            self.getplayerstats(item[1])


        for item in playerList:
            self.homeadd = 0
            self.getplayerstats(item[2])







#main function

#Find games between these dates and get data


