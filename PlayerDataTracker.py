import csv

class Player:
    def __init__(self, n):
        self.name = n
        self.gameno = []
        self.eff = []
        self.totalEff = []

    def addGame(self, gn, eff):
        eff = int(eff)
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

class PlayerDataTracker:
    def __init__(self):
        self.players = {}
        self.readFile()

    def readFile(self):
        with open('./data/mbb_player_data.csv', newline='', errors='ignore') as playerFile:
            reader = csv.DictReader(playerFile, delimiter=',')
            # read through entries, adding to neighbourhood list and price per neighbourhood dictionary
            for row in reader:
                if row["player"] in self.players:
                    self.players[row["player"]].addGame(row["gameno"], row["eff"])
                else:
                    self.players[row["player"]] = Player(row["player"])

    def getXVals(self):
        return self.xVals

    def getYVals(self):
        return self.yVals

    def getPlayers(self):
        listOfPlayers = []
        for name, playerObj in self.players.items():
             listOfPlayers.append(playerObj)
        return listOfPlayers
