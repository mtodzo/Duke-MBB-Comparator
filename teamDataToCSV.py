import csv

def main():
    teamDict = {}
    fieldnames = ["Team", "Game No.", "Offensive Rating", "Defensive Rating", "Overall Rating"]

#vals[0] = season years
#vals[1] = total possessions
#vals[2] = total points
#vals[3] = opponent total possessions
#vals[4] = oppenent total points

    #open DukeData file to read in desired data and write to new file
    with  open ('./DukeData_2018.csv', newline ='', errors = 'ignore') as dukeFile:
        reader = csv.DictReader(dukeFile, delimiter = ',')

        #write per game
        for row in reader:
            if row["gameno"] in teamDict:
                vals = teamDict.get(row["gameno"])
                vals[0] = vals[0]   #season is unchanged
                if row["fga"] != '<Null>':
                    vals[1] += int(row["fga"])
                if row["oreb"] != '<Null>':
                    vals[1] -= int(row["oreb"])
                if row["tovers"] != '<Null>':
                    vals[1] += int(row["tovers"])
                if row["fta"] != '<Null>':
                    vals[1] += (.4*int(row["fta"]))
                if row["tp"] != '<Null>':
                    vals[2] += int(row["tp"])

                teamDict[row["gameno"]] = vals
            else:
                vals = []
                if row["season"]:
                    vals.append(row["season"])
                else:
                    continue
                #vals[0] = row["season"]
                vals.append(int(row["fga"]) - int(row["oreb"]) + int(row["tovers"]) + (.4*int(row["fta"])))
                vals.append(int(row["tp"]))
                vals.append(0) #placeholders for opponent data
                vals.append(0)
                teamDict[row["gameno"]] = vals


    with  open ('./OpponentData_2018.csv', newline ='', errors = 'ignore') as opponentFile:
        reader = csv.DictReader(opponentFile, delimiter = ',')

        #write per game
        for row in reader:
            if row["gameno"] in teamDict:
                vals = teamDict.get(row["gameno"])
                if row["fga"] != '<Null>':
                    vals[3] += int(row["fga"])
                if row["oreb"] != '<Null>':
                    vals[3] -= int(row["oreb"])
                if row["tovers"] != '<Null>':
                    vals[3] += int(row["tovers"])
                if row["fta"] != '<Null>':
                    vals[3] += (.4*int(row["fta"]))
                if row["tp"] != '<Null>':
                    vals[4] += int(row["tp"])

                teamDict[row["gameno"]] = vals


    #opens TeamComparisonData (the csv file created in this program)
    #this file will contain only the desired info to be exported
    #with command automatically closes file after executing block
    with open ('./TeamComparisonData.csv', 'w') as csvfile:
        #initializes writer and writes desired headers
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        counter = 0
        pastSeason = teamDict.get(sorted(teamDict.keys())[0])[0]
        seasonPoints = 0
        seasonPossessions = 0
        oppPossessions = 0
        oppPoints = 0
        for key in sorted(teamDict.keys()):
            rowDictionary = {}
            if teamDict.get(key)[0] != pastSeason:
                pastSeason = teamDict.get(key)[0]
                counter = 0
                seasonPoints = 0
                seasonPossessions = 0
                oppPoints = 0
                oppPossessions = 0

            seasonPossessions += teamDict.get(key)[1]
            seasonPoints += teamDict.get(key)[2]
            oppPossessions += teamDict.get(key)[3]
            oppPoints += teamDict.get(key)[4]
            counter+=1

            rowDictionary["Team"] = teamDict.get(key)[0]         #write season
            rowDictionary["Game No."] = counter          #write game number
            if seasonPossessions != 0:
                rowDictionary["Offensive Rating"] = seasonPoints/seasonPossessions*100   #write offensive Rating
            if oppPossessions != 0:
                rowDictionary["Defensive Rating"] = oppPoints/oppPossessions*100   #write defensive Rating
            if seasonPossessions != 0 and oppPossessions != 0:
                rowDictionary["Overall Rating"] = (seasonPoints/seasonPossessions*100 - oppPoints/oppPossessions*100)

            writer.writerow(rowDictionary)

main()
    #field goals attempted - offensive rebounds + turnovers + (0.4 x free throws attempted) = total number of possessions
    #Tm total points / tm total possessions * 100

    #defensive efficiecy
    #total points of other team / total possessions of other team * 100

    # ways to compare:
    #offensive rating
    #defensive rating
    #overall rating -> avg of offensive and defensive
    #record
    #something that takes into account rank
    #    -> fulfilling expectation?
