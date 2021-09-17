import pandas
import numpy
import re
import sys
import math
import glob

def main(argv):
    if(len(argv) < 2):
        print("Invalid number of arguments!\nUsage: " + argv[0] + " <inputfolder>")
    else:
        inputfolder = argv[1]
        files = glob.glob(inputfolder + "/delays*.csv")
        pandas.set_option('display.max_rows', None)
        results = []
        for file in files:
            dataframe = pandas.read_csv(file, usecols=["time","displayed_time"])
            #prevDisplayed = -1
            for index, row in dataframe.iterrows():
                time = timestampToSeconds(row["time"])
                displayed_time = timestampToSeconds(row["displayed_time"])
                #if(displayed_time == prevDisplayed):
                #    continue
                prevDisplayed = displayed_time
                results.append(time - displayed_time)
                if(time - displayed_time < 1):
                    print("%s %s" %(file, row))

        min = numpy.min(results)
        max = numpy.max(results)
        avg = numpy.average(results)
        std_dev = numpy.std(results)
        unit = "sec"
        print(results)
        print("Avg: %.3f %s" %(avg, unit))
        print("StdDev: %.3f %s" %(std_dev, unit))
        print("Max: %.3f %s" %(max, unit))
        print("Min: %.3f %s" %(min, unit))

def timestampToSeconds(timestamp):
    timestamp_parts = timestamp.split(":")
    seconds = 0
    for i in range(len(timestamp_parts)):
        seconds += math.pow(60,i) * float(timestamp_parts[(len(timestamp_parts)-1-i)])
    return seconds


if __name__ == "__main__":
    main(sys.argv)

