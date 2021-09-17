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
        dataframe = pandas.read_csv(argv[1], usecols=["Transfer[Bytes]","Bitrate[bits/sec]","Receiver"])
        #processData(dataframe)
        rcv_results = []
        snd_results = []
        #for column in ["Transfer[Bytes]","Bitrate[bits/sec]"]:
        for column in ["Bitrate[bits/sec]"]:
            print("\nUPLOAD [Client --> Server]:")
            rcv_results += processDataFrame(dataframe[dataframe['Receiver'] == 1], column)
            print("\nDOWNLOAD [Server --> Client]:")
            snd_results += processDataFrame(dataframe[dataframe['Receiver'] == 0], column)

def processDataFrame(dataframe, column):
    min = numpy.min(dataframe[column])/1000000
    max = numpy.max(dataframe[column])/1000000
    avg = numpy.average(dataframe[column])/1000000
    std_dev = numpy.std(dataframe[column])/1000000

    if(re.match(r"Bitrate.*",column)):
        label = "Bitrate"
        unit = "Mbits/sec"
    elif(re.match(r"Transfer.*", column)):
        label = "Transfer"
        unit = "MBytes"
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

