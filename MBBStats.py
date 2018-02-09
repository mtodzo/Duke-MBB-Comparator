'''
Created on Feb 6, 2018

@author: jonathanmichala
'''

import csv

def main():
    playerDictionary = {}
    #Dictionary mapping player to [(game number, minutes, efficiency rating)] a list of tuples to do calculations with
    
    entryDictionary = {}
    #single entries to be written into new csv
    
    fieldnames = ['player', 'gameno', 'eff', 'win']
    
    with open('./mbb_player_data2.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        with open('./mbbdata.csv') as playersFile:
            reader = csv.DictReader(playersFile)
            for row in reader:
                if row['wins_measure']!='<Null>' and row['first']!='<Null>' and row['last']!='<Null>' and row['season2']!='<Null>' and row['gameno']!='<Null>' and row['min']!='<Null>' and row['fg']!='<Null>' and row['fga']!='<Null>' and row['ft']!='<Null>' and row['fta']!='<Null>' and row['treb']!='<Null>' and row['tp']!='<Null>' and row['ast']!='<Null>' and row['tovers']!='<Null>' and row['blk']!='<Null>' and row['stl']!='<Null>':
                    
                    player = row['first'] + '_' + row['last'] + '_' + str(row['season2'])
                    eff = int(row['tp']) + int(row['treb']) + int(row['ast']) + int(row['stl']) + int(row['blk']) + int(row['fg']) + int(row['ft']) - int(row['fga']) - int(row['fta']) - int(row['tovers'])
                    if player not in playerDictionary:
                        playerDictionary[player] = [(int(row['gameno']), int(row['min']), eff, int(row['wins_measure']))]
                    else:
                        playerDictionary[player].append((int(row['gameno']), int(row['min']), eff, int(row['wins_measure'])))
        
        for (p,tupList) in playerDictionary.items():
            #find the id for the first game of the season for the player
            #and find total minutes for a player. if < 30, they cut (could change)
            minGame = tupList[0][0]
            totalMin = 0
            for tup in tupList:
                totalMin += tup[1]
                if tup[0] < minGame:
                    minGame = tup[0]
            if totalMin < 30:
                del playerDictionary[p]
                continue
            
            #change game number id to nth game of the season for that player
            for tup in tupList:
                
                #write this player's efficiency during this game to the new csv file.
                entryDictionary['player'] = p
                entryDictionary['gameno'] = 1 + tup[0] - minGame
                entryDictionary['eff'] = tup[2]
                entryDictionary['win'] = tup[3]
                writer.writerow(entryDictionary)
            
            

if __name__ == '__main__':
    main()