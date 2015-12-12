#TEST: print collision.collide(["TTh14301550&W10301120&MW16001720&MWF08300920&W09301020&MWF12301320&Th12301320&TTh10001120&F15301650&"])

#MAIN FUNCTION TO CALL
#Takes in an array of strings, one string per person
#Each string is a token in the form "TTh14301550&W10301120&MW16001720&" for when that person's activities take place
#Returns a 3D list
#1st dimension is the day of the week
#2nd dimension are time ranges for when all people have open times to meet up
#3rd dimension is the start time and end time of each time ranges
# Note that time is returned in the form of minutes, where 0 is 12:00am and 1439 is 11:59pm
def collide(tokens):
    tesseract = []
    for token in tokens:
        tesseract.append(sortCube(ingest(token)))
    cube = tesseract[0]
    for i in range(7):
        for j in range(1,len(tesseract)):
            cube[i] = fusePairSquares(cube[i],tesseract[j][i])
        cube[i] = invertSquare(cube[i])
    cube = sortCube(cube)
    return cube

# Take a time in the format hhmm and converts it to minutes
# Ex. 10:41pm would be 2241 and after conversion it would be 1361
def convertToMinutes(time):
    hours = int(time[0:2])
    minutes = int(time[2:4])
    totalMinutes = minutes + hours * 60
    return totalMinutes


# Cleans input of '-' and ':'
def deleteUselessChars(token):
    token = token.translate(None, "-:")
    return token


def addTimeRange(instCube, currentTimeRange, currentDayIndex):
    instCube[currentDayIndex].append(currentTimeRange)
    return instCube

# Does a bunch of stuff
# Also has a cool name
# Takes the data of multiple people and outputs a 3d array
# 1st dimension: Day of the Week
# 2nd dimension: Time Ranges
# 3rd dimension: One start time and one end time
def ingest(token):
    dayIndices = {"M":0,"T":1,"W":2,"Th":3,"F":4,"S":5,"Su":6}
    token = deleteUselessChars(token)
    cube = [[],[],[],[],[],[],[]] #3d array cuz 2 aint enough for dis bigboi
    timeRanges = token.split("&") # makes an array for each time range that person has
    del timeRanges[-1]
    numTimeRanges = len(timeRanges) # gets how many time ranges they have
    for j in range(numTimeRanges):
        timeRange = timeRanges[j]
        timeRangeLength = len(timeRange)
        endTime = timeRange[timeRangeLength - 4: timeRangeLength]
        startTime = timeRange[timeRangeLength - 8: timeRangeLength - 4]
        days = timeRange[0: timeRangeLength - 8] + "  "
        daysLength = len(days) - 2
        endMinutes = convertToMinutes(endTime)
        startMinutes = convertToMinutes(startTime)
        currentTimeRange = [startMinutes, endMinutes]
        # Parsing through days to figure out which days the time range is applicable to
        index = 0
        parsing = True
        while (parsing):
            currentChar = days[index: index + 1]
            nextChar = days[index + 1: index + 2]
            if (currentChar == " "):
                parsing = False
                break
            currentDay = ""
            if ((currentChar == "T" or currentChar == "S") and (nextChar == "h" or nextChar == "u")):
                currentDay = currentChar + nextChar
                index += 1 # Skips next char since it is a part of the current day and not the next day
            else:
                currentDay = currentChar
            currentDayIndex = dayIndices[currentDay]
            cube = addTimeRange(cube, currentTimeRange, currentDayIndex)
            index += 1
    return cube

#Sorts each time range in a list of time ranges according to the start time of each time range
def sortCube(cube):
    for i in range(7):
        cube[i].sort(key=lambda x: x[0])
    return cube

#Takes a list of time ranges for when there are activities
#Returns the open times for that list of time ranges
def invertSquare(square):
    start = 0
    end = 0
    currentIndex = 0
    arr = []
    while(end < 1440):
        if currentIndex == len(square):
            if start != 1439:
                arr.append([start,1439])
        if currentIndex >= len(square):
            break
        if (end == square[currentIndex][0]):
            arr.append([start,end])
            start = square[currentIndex][1]
            end = square[currentIndex][1]
            currentIndex += 1
        end += 1
    if (arr[0] == [0,0]):
        del(arr[0])
    return arr

#Combines two squares eliminating redundant time ranges
#Assumes squares are sorted
def fusePairSquares(sq1, sq2):
    dup1 = sq1
    dup2 = sq2
    arrRedundant = []
    for e1 in sq1:
        for e2 in sq2:
            if e1[1] >= e2[0]:
                arrRedundant.append([e1[0],e2[1]])
                del(e1)
                del(e2)
    return sq1.extend(sq2.extend(arrRedundant))

    
    
                



    
        
    

