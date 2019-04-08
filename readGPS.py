# read from GPS file and get which game each player is playing

#GLOBAL VARIABLE
DATES = {}

def readGPS():
    fileIn = open("gps.csv", "r")
    line = fileIn.readline()
    gamePlayers = {}  # key: gemID | value: list of playerID
    lineNumber = 1

    for line in fileIn:
        if lineNumber%4000 == 1:
            line = line.strip().split(",")
            gameID = int(line[0])
            playerID = int(line[2])
            # print("gameID: " + str(gameID))
            # print("playerID: " + str(playerID))
            if gameID in gamePlayers.keys():
                game = gamePlayers[gameID]
                if playerID not in game:
                    gamePlayers[gameID].append(playerID)
            else:
                gamePlayers[gameID] = [playerID]
        lineNumber += 1;

    print(gamePlayers)
    # for key in gamePlayers:
    #     print(str(key) + ":")
    #     print(gamePlayers[key])
    #     print("\n\n")

    return gamePlayers

# def getRandomSample():
#     gps_data = pd.read_csv("gps.csv")
#     gps_data.sample(frac=0.003, replace=False, random_state=1)

def getWellness(gameDates, gamePlayers):
    gameWellness = {} #key: gameID; value: {playerID: fatigue}
    fileIn = open("wellness.csv", "r")
    line = fileIn.readline()

    for line in fileIn:
        line = line.strip().split(",")
        date = line[0]
        date = date.replace('/', '-')
        list = date.split('-')
        if len(list[1]) == 1:
            list[1] = '0'+list[1]
        if len(list[2]) == 1:
            list[2] = '0' + list[2]
        date = '-'.join(list)
        playerFatigues = {}
        if date in gameDates.keys():
            gameIDs = gameDates[date]
            playerID = int(line[1])
            fatigue = int(line[2])

            # soreness = int(line[3])
            # desire = int(line[4])
            # irritability = int(line[5])
            # monitoringScore = int([10])
            for gameID in gameIDs:
                playerIDs = gamePlayers[gameID]
                if playerID in playerIDs:
                    # if playerID in gameWellness[gameID].keys():
                    #     gameWellness[gameID][playerID] = fatigue
                    # else:
                    if gameID not in gameWellness.keys():
                        gameWellness[gameID] = {playerID: fatigue}
                    else:
                        gameWellness[gameID][playerID] = fatigue
    print(gameWellness)
    return gameWellness


def writeGameInfo(gamePlayers, gameDates, gameWellness):
    fileOut = open("gameInfo.csv", "w")
    print("Date,gameID,playerID, fatigue", file=fileOut)
    # for key in gamePlayers:
    #     print(str(key), file=fileOut, end=',')
    #     for player in gamePlayers[key]:
    #         print(str(player), file=fileOut, end=',')
    #     print(file=fileOut)
    for gameID in gameWellness.keys():
        date = DATES[gameID]
        for playerID in gameWellness[gameID].keys():
            fatigue = gameWellness[gameID][playerID]
            print(date + "," + str(gameID) + "," + str(playerID) + "," + str(fatigue), file=fileOut)
        print(file=fileOut)


def getGame():
    global DATES
    fileIn = open("games.csv", "r")
    line = fileIn.readline()
    gameDates = {}
    for line in fileIn:
        line = line.strip().split(",")
        gameID = int(line[0])
        date = line[1]
        if date not in gameDates:
            gameDates[date] = [gameID]
        else:
            gameDates[date].append(gameID)
        DATES[gameID] = date
    print(gameDates)
    print(DATES)
    return gameDates

#  get the average duration of each training session type for each game day
def getAvgDuration(gameDates):
    avgDuration = {} #key: date; value: {sessionType: [sum, n]}
    fileIn = open("rpe.csv", "r")
    line = fileIn.readline()
    avgACratio = {} # AcuteChronicRatio ||| key: date; value: [sum, n]

    for line in fileIn:
        line = line.strip().split(",")
        date = line[0]
        date = date.replace('/', '-')
        list = date.split('-')
        if len(list[1]) == 1:
            list[1] = '0'+list[1]
        if len(list[2]) == 1:
            list[2] = '0' + list[2]
        date = '-'.join(list)
        if date in gameDates.keys():
            if line[4] != "NA":
                sessionType = line[3]
                duration = int(line[4])
                if date in avgDuration.keys():
                    if sessionType in avgDuration[date].keys():
                        avgDuration[date][sessionType][0] += duration
                        avgDuration[date][sessionType][1] += 1
                    else:
                        avgDuration[date][sessionType] = [duration, 1]
                else:
                    avgDuration[date] = {}
                    avgDuration[date][sessionType] = [duration, 1]
        if line[10] != "NA": # calculate the average AC ratio
            acratio = float(line[10])
            if date in avgACratio.keys():
                avgACratio[date][0] += acratio
                avgACratio[date][1] += 1
            else:
                avgACratio[date] = [acratio, 1]

    print("averageDuration: ")
    print(avgDuration)
    print("\nprint averageACratio: ")
    print(avgACratio)
    fileOutAvgDur = open("avgDuration.csv", "w")
    for date in avgDuration.keys():
        for sessionType in avgDuration[date].keys():
            sum = avgDuration[date][sessionType][0]
            n = avgDuration[date][sessionType][1]
            avg = sum/n
            print(date + "," + sessionType + "," + str(avg), file=fileOutAvgDur)

    fileOutAvgACr = open("avgACratio.csv", "w")
    for date in avgACratio.keys():
        sum = avgACratio[date][0]
        n = avgACratio[date][1]
        avg = sum/n
        print(date + "," + str(avg), file=fileOutAvgACr)



def main():
    gamePlayers = readGPS()
    gameDates = getGame()
    # getRandomSample()
    gameWellness = getWellness(gameDates, gamePlayers)
    writeGameInfo(gamePlayers, gameDates, gameWellness)
    print()
    getAvgDuration(gameDates)



main()