import csv
import collections

class Team:
    def __init__(self, n):
        self.name = n
        self.gameno = []
        self.offensiveEffs = []
        self.totalOffensiveEffs = []
        self.defensiveEffs = []
        self.totalDefensiveEffs = []
        self.overallEffs = []
        self.totalOverallEffs = []

    def addGame(self, gn, offEff, dEff, overEff):
        offEff, dEff, overEff = float(offEff), float(dEff), float(overEff)
        self.gameno.append(gn)
        self.offensiveEffs.append(offEff)
        self.defensiveEffs.append(dEff)
        self.overallEffs.append(overEff)

        totalOffensiveEffs = 0
        totalDefensiveEffs = 0
        totalOverallEffs = 0
        for i in range(len(self.gameno)): # iterate through all previous scores
            totalOffensiveEffs += self.offensiveEffs[i]
            totalDefensiveEffs += self.defensiveEffs[i]
            totalOverallEffs += self.overallEffs[i]
        self.totalOffensiveEffs.append(totalOffensiveEffs)
        self.totalDefensiveEffs.append(totalDefensiveEffs)
        self.totalOverallEffs.append(totalOverallEffs)

    def getName(self):
        return self.name
    def getGameNos(self):
        return self.gameno

    def getAverageEffs(self, type):
        avgEffs = []
        counter = 0

        effList = []
        if type == 'offensive':
            effList = self.totalOffensiveEffs
        elif type == 'defensive':
            effList = self.totalDefensiveEffs
        elif type == 'overall':
            effList = self.totalOverallEffs

        for i in range(len(effList)):
            avgEffs.append(effList[i]/(int(i)+1))
        return avgEffs

    def getTeamAverage(self, type):
        effList = []
        if type == 'offensive':
            effList = self.totalOffensiveEffs
        elif type == 'defensive':
            effList = self.totalDefensiveEffs
        elif type == 'overall':
            effList = self.totalOverallEffs
        return effList[len(effList)-1]/int(self.gameno[len(self.gameno)-1])

class TeamDataTracker:
    def __init__(self):
        self.teams = collections.OrderedDict()
        self.readFile()

    def readFile(self):
        with open('./data/TeamComparisonData.csv', newline='', errors='ignore') as teamFile:
            reader = csv.DictReader(teamFile, delimiter=',')
            # read through entries, adding to neighbourhood list and price per neighbourhood dictionary
            for row in reader:
                if int(row["Team"][0:4]) >= 1957:
                    if row["Team"] in self.teams:
                        self.teams[row["Team"]].addGame(row["Game No."], row["Offensive Rating"], row["Defensive Rating"], row["Overall Rating"])
                    else:
                        self.teams[row["Team"]] = Team(row["Team"])

    def getXVals(self):
        return self.xVals

    def getYVals(self):
        return self.yVals

    def getTeams(self):
        listOfTeams = []
        for name, teamObj in self.teams.items():
             listOfTeams.append(teamObj)
        return listOfTeams

    def getTeamAverages(self, t):
        teamAverages = []
        for name, teamObj in self.teams.items():
            teamAverages.append(teamObj.getTeamAverage(t))
        return teamAverages

    def getTeamNames(self):
        teamNames = []
        for name, teamObj in self.teams.items():
             teamNames.append(name[:4])
        return teamNames
