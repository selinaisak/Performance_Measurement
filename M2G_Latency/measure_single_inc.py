import math
import os

BUFFER_LENGTH = 0.133
#QUALITIES = [1, 2]

'''used to parse the wanted lines from log-file'''


def getContent(filePath):
    file = open(filePath)
    lines = file.readlines()
    file.close()
    values = []
    maxMatches = 0
    for index in range(len(lines)):
        # and lines[index+1].__contains__("[TILE_Q]")
        if (lines[index].__contains__("[HEAD_VD]")):
            line_parts = lines[index].split(': ')
            tag = line_parts[0]
            timestamp = line_parts[1]
            visibleTiles = line_parts[2].strip('\n').split(',')
            values.append([tag, timestamp, visibleTiles])
            maxMatches = maxMatches + 1
        elif (lines[index].__contains__("[TILE_Q]")):
            line_parts = lines[index].split(': ')
            tag = line_parts[0]
            timestamp = line_parts[1]
            visibleTiles = line_parts[2].split(',')
            quality = line_parts[3].strip('\n')
            values.append([tag, timestamp, visibleTiles, quality])
    return [values, maxMatches]


def getAvg(list):
    sum = 0
    for element in list:
        sum += element
    return sum / len(list)


def getStdDev(list):
    avg = getAvg(list)
    squared_error = 0
    for element in list:
        squared_error += math.pow((element - avg), 2)

    return math.sqrt(squared_error / len(list))


def getMax(list):
    max = list[0]
    for index in range(1, len(list)):
        if (list[index] > max):
            max = list[index]
    return max


def getMin(list):
    min = list[0]
    for index in range(1, len(list)):
        if (list[index] < min):
            min = list[index]
    return min


''' search for the timestamp where the passed
    values match AND the quality level also matches'''


def getNextTileQualityTimestamp(current_index, tiles, values, minLatency):
    start_index = None
    start_time = values[current_index][1]
    for index in range(current_index, len(values)):
        if (values[index][0] == '[TILE_Q]'):
            start_index = index
            break
    if (start_index == None):
        return None

    for value in values[start_index:]:
        if (value[0] == '[HEAD_VD]'):
            break
        else:
             if (value[2] == tiles and (int(value[1]) - int(start_time)) / (
             #if (all(item in tiles for item in value[2]) and (int(value[1]) - int(start_time)) / (
                    1000 * 1000 * 1000) >= minLatency):
                print("tiles " + str(tiles))
                print("value[2] " + str(value[2]))
                return [value[1], int(value[3])]

    return None


''' go through all files of a folder and 
    calculate the latency for each head movement if possible'''


def getLatenciesDir(directoryPath):
    latencies = []
    files = os.listdir(directoryPath)
    maxMatches = 0
    for file in files:
        value_pair = getLatencies(directoryPath + "/" + file)
        latencies.extend(value_pair[0])
        maxMatches = maxMatches + value_pair[1]
    return [latencies, maxMatches]


def getLatencies(filePath):
    latencies = []

    value_pair = getContent(filePath)
    values = value_pair[0]
    maxMatches = value_pair[1]
    prevQuality = 0
    for index in range(len(values)):
        if (values[index][0] == '[HEAD_VD]'):
            time_start = values[index][1]
            datapair = getNextTileQualityTimestamp(index, values[index][2], values, BUFFER_LENGTH)

            if (datapair != None):
                time_end = datapair[0]
                quality = datapair[1]
                if (quality == 2 or quality > prevQuality):
                    latency = (int(time_end) - int(time_start)) / (1000 * 1000 * 1000)
                    latencies.append(latency)
                prevQuality = quality

    return [latencies, maxMatches]


def printStats(latencies):
    print(latencies[0])
    print("Avg: %.3f sec" % round(getAvg(latencies[0]), 3))
    print("StdDev: %.3f sec" % round(getStdDev(latencies[0]), 3))
    print("Max: %.3f sec" % round(getMax(latencies[0]), 3))
    print("Min: %.3f sec" % round(getMin(latencies[0]), 3))
    print("success: %.3f%s" % ((len(latencies[0])/latencies[1])*100, "%"))


if __name__ == '__main__':
    latencies = getLatenciesDir("D://Data/Measurements/Lat_new/tiled/2K/GOP4/UCVR")
    printStats(latencies)