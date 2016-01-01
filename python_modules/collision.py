#TEST: print collision.collide(["TTh14301550&W10301120&MW16001720&MWF08300920&W09301020&MWF12301320&Th12301320&TTh10001120&F15301650&"])

from datetime import datetime

#MAIN FUNCTION TO CALL
#Takes in an array of strings, one string per person
#Each string is a token in the form "TTh14301550&W10301120&MW16001720&" for when that person's activities take place
#Returns a 3D list
#1st dimension is the day of the week
#2nd dimension are time ranges for when all people have open times to meet up
#3rd dimension is the start time and end time of each time ranges
# Note that time is returned in the form of minutes, where 0 is 12:00am and 1439 is 11:59pm
def collide(tokens):
    if tokens is None:
        return 'error69'
    tesseract = []
    for token in tokens:
        tesseract.append(sortCube(ingest(convertToMilitaryTime(token))))
    if tesseract is not None:
        cube = splice(tesseract)
    else:
        return 'error69'
    if cube is None:
        return 'error69'
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
    token = token.replace("-", "")
    token = token.replace(":", "")
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
    token = convertToMilitaryTime(token)
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
        if end == square[len(square)-1][1] and end != 1439:
            arr.append([end,1439])
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
    dup2 = sq2
    fuse = []
    arr = []
    for i in range(len(sq1)):
        fused = False
        for j in range(len(sq2)):
            if sq1[i][1] >= sq2[j][0] and sq1[i][0] <= sq2[j][0] and sq1[i][1] <= sq2[j][1]:
                fuse.append([sq1[i][0], sq2[j][1]])
                del(dup2[j])
                fused = True
            elif sq2[j][1] >= sq1[i][0] and sq2[j][0] <= sq1[i][0] and sq2[j][1] <= sq1[i][1]:
                fuse.append([sq2[j][0], sq1[i][1]])
                del(dup2[j])
                fused = True
            elif sq1[i][1] >= sq2[j][1] and sq1[i][0] <= sq2[j][0]:
                fuse.append([sq1[i][0], sq1[i][1]])
                del(dup2[j])
                fused = True
            elif sq2[j][1] >= sq1[i][1] and sq2[j][0] <= sq1[i][0]:
                fuse.append([sq2[j][0], sq2[j][1]])
                del(dup2[j])
                fused = True
        if not fused:
            arr.append(sq1[i])
    return fuse + arr + dup2

def fuse(sq1, sq2):
    arr1 = sorted(sq1+sq2, key=lambda x: x[0])
    arr2 = [arr1[0]]
    for i in range(1,len(arr1)):
        if arr1[i-1][1] < arr1[i][1]:
            arr2.append(arr1[i])
    arr1 = []
    for i in range(1,len(arr2)):
        if (arr2[i-1][1] >= arr2[i][0]):
            sq = [arr2[i-1][0],arr2[i][1]]
            for j in range(i,len(arr2)-1):
                print sq
                if (arr2[i][1] >= arr2[i+1][0]):
                    sq[1] = arr2[i+1][1]
                else:
                    break
            arr1.append(sq)
    return arr1

def splice(tesseract):
    length = len(tesseract)
    cube = []
    for i in range(7):
        square = []
        for j in range(length):
            square.extend(tesseract[j][i])
        arr = []
        for e in square:
            arr.extend(range(e[0],e[1]))
        arr = sorted(list(set(range(0,1440)) - set(arr)))
        cube.append(convertToTimeRanges(arr))
    return cube

def convertToTimeRanges(arr):
    start = 0
    sq = []
    for x in range(1,len(arr)):
        if arr[x] != arr[x-1] + 1:
            sq.append([start,arr[x-1]])
            start = arr[x]
    if arr[-1] == 1439:
        sq.append([start,1439])
    return sq

def convertToMilitaryTime(s):
    if not 'A' in s and not 'P' in s:
        return s
    length = len(s)
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    for i in range(length):
        if i >= len(s):
            break
        if s[i] == 'A' or s[i] == 'P':
            time = ""
            if s[i-4] not in numbers:
                time = '0' + s[i-3:i+2]
                time = datetime.strptime(time,'%I%M%p').strftime('%H%M')
                s = s[:i-3] + time + s[i+2:]
            else:
                time = s[i-4:i+2]
                time = datetime.strptime(time,'%I%M%p').strftime('%H%M')
                s = s[:i-4] + time + s[i+2:]
    s = s.replace("-", "")
    return s + '&'
    
    
# TEST: print collision.collide(["MWF830AM-920AM&F930AM-1020AM&TTh1000AM-1120AM&TTh230PM-350PM&MW1130AM-1220PM&F130PM-220PM&MWF230PM-320PM&W530PM-620PM","F1030AM-1120AM&TTh830AM-950AM&MWThF230PM-320PM&MWF930AM-1020AM&Th1030AM-1120AM&MW100PM-220PM&F330PM-450PM&TTh1230PM-220PM","F930AM-1020AM&TTh100PM-220PM&TTh1000AM-1120AM&MWF1130AM-1220PM&MWF1030AM-1120AM&W530PM-620PM&MW1230PM-220PM","F930AM-1020AM&MWF1130AM-1220PM&TTh1130AM-1250PM&TTh100PM-220PM&F130PM-220PM&MWF830AM-920AM&MWF1030AM-1120AM&Th1030AM-1120AM"])

# TEST: print collision.convertToMilitaryTime("MWF830AM-920AM&F930AM-1020AM&TTh1000AM-1120AM&TTh230PM-350PM&MW1130AM-1220PM&F130PM-220PM&MWF230PM-320PM&W530PM-620PM")
    
# TEST: print collision.collide(["M1000AM-1100AM&M1200PM-200PM","M1100AM-1200PM"])

# CMD LINE TEST: python run.py MWF830AM-920AM&F930AM-1020AM&TTh1000AM-1120AM&TTh230PM-350PM&MW1130AM-1220PM&F130PM-220PM&MWF230PM-320PM&W530PM-620PM F1030AM-1120AM&TTh830AM-950AM&MWThF230PM-320PM&MWF930AM-1020AM&Th1030AM-1120AM&MW100PM-220PM&F330PM-450PM&TTh1230PM-220PM F930AM-1020AM&TTh100PM-220PM&TTh1000AM-1120AM&MWF1130AM-1220PM&MWF1030AM-1120AM&W530PM-620PM&MW1230PM-220PM F930AM-1020AM&MWF1130AM-1220PM&TTh1130AM-1250PM&TTh100PM-220PM&F130PM-220PM&MWF830AM-920AM&MWF1030AM-1120AM&Th1030AM-1120AM

# python run.py MWF830AM-920AM&F930AM-1020AM&TTh1000AM-1120AM&TTh230PM-350PM&MW1130AM-1220PM&F130PM-220PM&MWF230PM-320PM&W530PM-620PM F1030AM-1120AM&TTh830AM-950AM&MWThF230PM-320PM&MWF930AM-1020AM&Th1030AM-1120AM&MW100PM-220PM&F330PM-450PM&TTh1230PM-220PM F930AM-1020AM&TTh100PM-220PM&TTh1000AM-1120AM&MWF1130AM-1220PM&MWF1030AM-1120AM&W530PM-620PM&MW1230PM-220PM F930AM-1020AM&MWF1130AM-1220PM&TTh1130AM-1250PM&TTh100PM-220PM&F130PM-220PM&MWF830AM-920AM&MWF1030AM-1120AM&Th1030AM-1120AM
    

