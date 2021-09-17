import pandas
import matplotlib
import numpy
import re
import sys

def main(argv):
    if(len(argv) < 2):
        print("Invalid number of arguments!\nUsage: " + argv[0] + " <inputfile>")
    else:
        pandas.set_option('display.max_rows', None)
        dataframe = pandas.read_csv(argv[1], usecols=["time[ms]"])
        #processData(dataframe)
        results = []
        #for column in ["Transfer[Bytes]","Bitrate[bits/sec]"]:
        for column in ["time[ms]"]:
            results += processDataFrame(dataframe, column)

def processDataFrame(dataframe, column):
    min = numpy.min(dataframe[column])
    max = numpy.max(dataframe[column])
    avg = numpy.average(dataframe[column])
    std_dev = numpy.std(dataframe[column])

    if(re.match(r"time.*",column)):
        label = "Time"
        unit = "ms"
    else:
        print("Invalid column! No analysis possible.")
        return

    print("Avg_%s: %.3f %s" %(label, avg, unit))
    print("StdDev_%s: %.3f %s" %(label, std_dev, unit))
    print("Max_%s: %.3f %s" %(label, max, unit))
    print("Min_%s: %.3f %s" %(label, min, unit))
    return [{column: [min, max, avg, std_dev]}]


if __name__ == "__main__":
    main(sys.argv)

