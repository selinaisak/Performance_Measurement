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
        files = glob.glob(inputfolder + "/*-latency.csv")
        pandas.set_option('display.max_rows', None)
        results = []
        for file in files:
            dataframe = pandas.read_csv(file, usecols=["LATENCY_USEC"])
            #prevDisplayed = -1
            for index, row in dataframe.iterrows():
                time = timeToMilliSeconds(row["LATENCY_USEC"])
                results.append(time)
                
        min = numpy.min(results)
        max = numpy.max(results)
        avg = numpy.average(results)
        std_dev = numpy.std(results)
        unit = "ms"
        print(results)
        print("Avg: %.3f %s" %(avg, unit))
        print("StdDev: %.3f %s" %(std_dev, unit))
        print("Max: %.3f %s" %(max, unit))
        print("Min: %.3f %s" %(min, unit))

def timeToMilliSeconds(time):
    return time/1000


if __name__ == "__main__":
    main(sys.argv)

