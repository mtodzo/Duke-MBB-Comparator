import csv

class Team:
    def __init__(self, n):
        self.name = n
        self.gameno = []
        self.eff = []
        self.totalEff = []

    def addGame(self, gn, eff):
        eff = float(eff)
        self.gameno.append(gn)
        self.eff.append(eff)

        totalEff = 0
        for i in range(len(self.gameno)): # iterate through all previous scores
            totalEff += self.eff[i]
        self.totalEff.append(totalEff)

    def getName(self):
        return self.name
    def getGameNos(self):
        return self.gameno
    def getEffs(self):
        return self.eff
    def getAverageEffs(self):
        avgEffs = []
        counter = 0
        for i in range(len(self.totalEff)):
            avgEffs.append(self.totalEff[i]/(int(i)+1))
        return avgEffs

class TeamDataTracker:
    def __init__(self):
        self.teams = {}
        self.readFile()

    def readFile(self):
        with open('./data/TeamComparisonData.csv', newline='', errors='ignore') as teamFile:
            reader = csv.DictReader(teamFile, delimiter=',')
            # read through entries, adding to neighbourhood list and price per neighbourhood dictionary
            for row in reader:
                if row["Team"] in self.teams:
                    self.teams[row["Team"]].addGame(row["Game No."], row["Offensive Rating"])
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
