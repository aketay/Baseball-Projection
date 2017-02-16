
import urllib2
import csv

from bs4 import BeautifulSoup
from collections import defaultdict


class BaseballReference:

    def __init__(self):
        self.tempList = []
        self.list1 = []
        self.list2 =[]
        self.list3 =[]
        self.leagueAverageDict = {}

    def getLeagueAveragesSplits(self):
        websiteString = "http://www.baseball-reference.com/leagues/split.cgi?t=b&lg=MLB&year=2014"

        try:

            sock2 = urllib2.urlopen(websiteString)

        except urllib2.HTTPError, e:

            urlerrorCode = e.code

            print urlerrorCode

            print e.fp.read()

        dataslerp = sock2.read()

        dataderp = dataslerp.replace('&nbsp;', '')

        soup = BeautifulSoup(dataderp)

        selects = soup.find_all("table", { "id" : "plato" })

        for row in selects[0].find_all("tr"):

            cells = row.find_all("td")
            #(OBPL,OBPR 1B, 2B, 3B, HR, Walk, Strike Out)
            if len(cells)>0:
                if cells[0].text == "vs RHP":
                    self.leagueAverageDict['OBPR'] = float(cells[16].text)
                if cells[0].text == "vs LHP":
                    self.leagueAverageDict['OBPL'] = float(cells[16].text)

    def getLeagueAverages(self):
        websiteString = "http://www.baseball-reference.com/leagues/MLB/2014-standard-batting.shtml"

        try:

            sock2 = urllib2.urlopen(websiteString)

        except urllib2.HTTPError, e:

            urlerrorCode = e.code

            print urlerrorCode

            print e.fp.read()

        dataslerp = sock2.read()

        dataderp = dataslerp.replace('&nbsp;', '')

        soup = BeautifulSoup(dataderp)

        selects = soup.find_all("table", { "id" : "teams_standard_batting" })

        for row in selects[0].find_all("tr",{"class":"stat_total"}):

            cells = row.find_all("td")

            #(OBPL,OBPR 1B, 2B, 3B, HR, Walk, Strike Out)
            if len(cells)>0:
                self.leagueAverageDict['PA'] = float(cells[5].text)
                self.leagueAverageDict['AB'] = float(cells[6].text)
                self.leagueAverageDict['R'] = float(cells[7].text)
                self.leagueAverageDict['H'] = float(cells[8].text)
                self.leagueAverageDict['2B'] = float(cells[9].text)
                self.leagueAverageDict['3B'] = float(cells[10].text)
                self.leagueAverageDict['HR'] = float(cells[11].text)
                self.leagueAverageDict['BB'] = float(cells[15].text)
                self.leagueAverageDict['SO'] = float(cells[16].text)


        self.leagueAverageDict['WalkRate'] = round(self.leagueAverageDict['BB']/(self.leagueAverageDict['BB']+self.leagueAverageDict['H']),3)
        self.leagueAverageDict['SORate'] = round(self.leagueAverageDict['SO']/(self.leagueAverageDict['AB']-self.leagueAverageDict['H']),3)
        self.leagueAverageDict['1BRate'] = round((self.leagueAverageDict['H']-self.leagueAverageDict['2B']-self.leagueAverageDict['3B']-self.leagueAverageDict['HR'])/self.leagueAverageDict['H'],3)
        self.leagueAverageDict['2BRate'] = round(self.leagueAverageDict['2B']/self.leagueAverageDict['H'],3)
        self.leagueAverageDict['3BRate'] = round(self.leagueAverageDict['3B']/self.leagueAverageDict['H'],3)
        self.leagueAverageDict['HRRate'] = round(self.leagueAverageDict['HR']/self.leagueAverageDict['H'],3)

        self.getLeagueAveragesSplits()

    def getBRPlayers(self,teamName):

        websiteString = "http://www.baseball-reference.com/teams/" + teamName+ "/2014.shtml"

        try:

            sock2 = urllib2.urlopen(websiteString)

        except urllib2.HTTPError, e:

            urlerrorCode = e.code

            print urlerrorCode

            print e.fp.read()

        dataslerp = sock2.read()

        dataderp = dataslerp.replace('&nbsp;', '')

        soup = BeautifulSoup(dataderp)

        for a in soup.find_all('a', href=True):

            for item in test2.my_data:

                if item[0] == a.text:

                    print a.text , a['href'][11:-6]

    def getBatterStats(self):

        currentYear = "2013"

        websiteString = "http://www.baseball-reference.com/leagues/MLB/"+str(currentYear)+"-value-pitching.shtml"

        try:

            sock2 = urllib2.urlopen(websiteString)

        except urllib2.HTTPError, e:

            urlerrorCode = e.code

            print urlerrorCode

            print e.fp.read()

        dataslerp = sock2.read()

        dataderp = dataslerp.replace('&nbsp;', ' ')

        soup = BeautifulSoup(dataderp)

        selects = soup.find_all("table", { "id" : "players_value_pitching" })

        for row in selects[0].find_all("tr"):

            cells = row.find_all("td")

            self.playerList = {}

            if len(cells)>0:

                self.playerList['Year'] = currentYear

                self.playerList['PlayerID'] = cells[1].a['href'][11:-6]

                self.playerList['Name'] = cells[1].text.replace('*','')

                self.playerList['Age'] = cells[2].text

                self.playerList['Tm'] = cells[3].text

                self.playerList['IP'] = cells[4].text

                self.playerList['G'] = cells[5].text

                self.playerList['GS'] = cells[6].text

                self.playerList['R'] = cells[7].text

                self.playerList['RA9'] = cells[8].text

                self.playerList['RA9opp'] = cells[9].text

                self.playerList['RA9def'] = cells[10].text

                self.playerList['RA9role'] = cells[11].text

                self.playerList['PPFp'] = cells[12].text

                self.playerList['RA9avg'] = cells[13].text

                self.playerList['RAA'] = cells[14].text

                self.playerList['WAA'] = cells[15].text

                self.playerList['gmLI'] = cells[16].text

                self.playerList['WAAadj'] = cells[17].text

                self.playerList['WAR'] = cells[18].text

                self.playerList['RAR'] = cells[19].text

                self.playerList['waaWL%'] = cells[20].text

                self.playerList['162WL%'] = cells[21].text

                self.playerList['Salary'] = cells[22].text

                self.playerList['Acquired'] = cells[23].text

                self.list1.append(self.playerList)

    def getBatterStats2(self):

            currentYear = "2013"

            websiteString = "http://www.baseball-reference.com/leagues/MLB/"+ str(currentYear) +"-batting-pitching.shtml"

            try:

                sock2 = urllib2.urlopen(websiteString)

            except urllib2.HTTPError, e:

                urlerrorCode = e.code

                print urlerrorCode

                print e.fp.read()

            dataslerp = sock2.read()

            dataderp = dataslerp.replace('&nbsp;', ' ')

            soup = BeautifulSoup(dataderp)

            selects = soup.find_all("table", { "id" : "players_batting_pitching" })

            for row in selects[0].find_all("tr"):

                cells = row.find_all("td")

                self.playerList = {}

                if len(cells)>0:

                    self.playerList['Year'] = currentYear

                    self.playerList['PlayerID'] = cells[1].a['href'][11:-6]

                    self.playerList['Name'] = cells[1].text.replace('*','')

                    self.playerList['Age'] = cells[2].text

                    self.playerList['Tm'] = cells[3].text

                    self.playerList['IP'] = cells[4].text

                    self.playerList['G'] = cells[6].text

                    self.playerList['PA'] = cells[7].text

                    self.playerList['AB'] = cells[8].text

                    self.playerList['R'] = cells[9].text

                    self.playerList['H'] = cells[10].text

                    self.playerList['2B'] = cells[11].text

                    self.playerList['3B'] = cells[12].text

                    self.playerList['HR'] = cells[13].text

                    self.playerList['SB'] = cells[14].text

                    self.playerList['CS'] = cells[15].text

                    self.playerList['BB'] = cells[16].text

                    self.playerList['SO'] = cells[17].text

                    self.playerList['BA'] = cells[18].text

                    self.playerList['OBP'] = cells[19].text

                    self.playerList['SLG'] = cells[20].text

                    self.playerList['OPS'] = cells[21].text

                    self.playerList['BAbip'] = cells[22].text

                    self.playerList['TB'] = cells[23].text

                    self.playerList['GDP'] = cells[24].text

                    self.playerList['HBP'] = cells[25].text

                    self.playerList['SH'] = cells[26].text

                    self.playerList['SF'] = cells[27].text

                    self.playerList['IBB'] = cells[28].text

                    self.playerList['ROE'] = cells[29].text

                    self.list2.append(self.playerList)

    def getBatterStats3(self):

                currentYear = "2013"

                websiteString = "http://www.baseball-reference.com/leagues/MLB/"+ str(currentYear) +"-standard-pitching.shtml"

                try:

                    sock2 = urllib2.urlopen(websiteString)

                except urllib2.HTTPError, e:

                    urlerrorCode = e.code

                    print urlerrorCode

                    print e.fp.read()

                dataslerp = sock2.read()

                dataderp = dataslerp.replace('&nbsp;', ' ')

                soup = BeautifulSoup(dataderp)

                selects = soup.find_all("table", { "id" : "players_standard_pitching" })

                for row in selects[0].find_all("tr"):

                    cells = row.find_all("td")

                    self.playerList = {}

                    if len(cells)>0:
                        try:
                            self.playerList['Year'] = currentYear

                            self.playerList['PlayerID'] = cells[1].a['href'][11:-6]

                            self.playerList['Name'] = cells[1].text.replace('*','')

                            self.playerList['Age'] = cells[2].text

                            self.playerList['Tm'] = cells[3].text

                            self.playerList['ERA'] = cells[8].text

                            self.playerList['G'] = cells[9].text

                            self.playerList['IP'] = cells[15].text

                            self.playerList['H'] = cells[16].text

                            self.playerList['R'] = cells[17].text

                            self.playerList['ER'] = cells[18].text

                            self.playerList['HR'] = cells[19].text

                            self.playerList['BB'] = cells[20].text

                            self.playerList['SO'] = cells[21].text

                            self.playerList['HBP'] = cells[22].text

                            self.playerList['FIP'] = cells[28].text

                            self.playerList['WHIP'] = cells[29].text

                            self.playerList['BB9'] = cells[32].text

                            self.playerList['SO9'] = cells[33].text

                            self.list3.append(self.playerList)
                        except:
                            pass


test1 = BaseballReference()
#
test1.getBatterStats()
test1.getBatterStats2()
test1.getBatterStats3()

d = defaultdict(dict)
newList =[]
finalList = []
for item in test1.list1:
    for thing in test1.list2:
        if item['Tm'] == thing['Tm'] and item['PlayerID'] == thing['PlayerID'] and item['Year']==thing['Year']:
            newList.append(dict(item.items() + thing.items()))

for item in newList:
    for thing in test1.list3:
        if item['Tm'] == thing['Tm'] and item['PlayerID'] == thing['PlayerID'] and item['Year']==thing['Year']:
            finalList.append(dict(item.items() + thing.items()))

f = open('TestData1.csv', 'wb')
# get a csv writer
writer = csv.writer( f )
keys = finalList[0].keys()
dict_writer = csv.DictWriter(f, keys)
dict_writer.writer.writerow(keys)
dict_writer.writerows(finalList)
f.close()
# Sim.getLeagueAverages()
#
# #(OBPL,OBPR 1B, 2B, 3B, HR, Walk, Strike Out)
#
# for item in Sim.leagueAverageDict.keys():
#     print item,Sim.leagueAverageDict[item]
