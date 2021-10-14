import pandas
import numpy
import re
import sys
import math
import glob

def main(argv):
    if(len(argv) < 3 or (argv[2] != "up" and argv[2] != "down")):
        print("Invalid arguments!\nUsage: " + argv[0] + " <inputfolder> + <up/down>")
    else:
        inputfolder = argv[1]
        link = argv[2]
        linkfolder = "tcp_" + link + "link"
        files = glob.glob(linkfolder + "/" + inputfolder + "/*.csv")
        if(link == "up"):
            column = "TCPUL"
        else:
            column = "TCPDL"
        pandas.set_option('display.max_rows', None)
        results = []
        for file in files:
            dataframe = pandas.read_csv(file, usecols=[column])
            #prevDisplayed = -1
            for index, row in dataframe.iterrows():
                throughput = row[column]
                results.append(throughput)
                
        min = numpy.min(results)
        max = numpy.max(results)
        avg = numpy.average(results)
        std_dev = numpy.std(results)
        unit = "Mbit/s"
        print(results)
        print("Avg: %.3f %s" %(avg, unit))
        print("StdDev: %.3f %s" %(std_dev, unit))
        print("Max: %.3f %s" %(max, unit))
        print("Min: %.3f %s" %(min, unit))




if __name__ == "__main__":
    main(sys.argv)

