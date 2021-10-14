import sys
import re

def main(argv):
    if(len(argv) < 2):
        print("Invalid number of arguments!\nUsage: " + argv[0] + " <inputfile>")
    else:
        file = open(argv[1], "r")
        filename = extractFilename(argv[1])
        toCSV(file, filename)
        file.close()

# this methods extracts the file name from the given path to
# the Log-File --> we want the CSV-File to have the same name
# as the Log-File except for the file extension of course
def extractFilename(path):
    path_parts = path.split("\\")
    file_parts = path_parts[len(path_parts)-1].split(".")
    filename = file_parts[0]
    return filename

# this method generates a CSV-File out of the produced Log-File
def toCSV(file, filename):
    csvHeader = "ID,Interval[sec],Transfer[Bytes],Bitrate[bits/sec],Retr,Cwnd[Bytes],Receiver"
    lines = fetchRelevantLines(file)
    lines = setSndRcvFlags(lines)
    csvFile = open(filename + ".csv", "w")
    csvFile.write(csvHeader + "\n")
    for line in lines:
        line = re.sub("\t+", ",", line)
        if(line[0]==','):
            line = line[1:]
        if(fullSecond(line.split(",")[1])):
            csvFile.write(line+"\n")
            print(line)
    csvFile.close()

# this method filters the Log-File for the relevant lines
# so only the data regarding sending/receiving data are saved
def fetchRelevantLines(file):
    lines = file.readlines()
    relevantLines = []
    for i in range(len(lines)):
        if(re.match(r"^\[[\s]*([0-9]+|ID)\][\s]*[0-9]+", lines[i])):
            lines[i] = re.sub(r"[\[\]]", "", lines[i])
            lines[i] = re.sub(r"\s+", "\t", lines[i])    
            lines[i] = processLine(lines[i])
            relevantLines += [lines[i]]
    return relevantLines

# this method is used for transforming all data in a uniform format
# --> results must be in the same unit
def processLine(line):
    line_parts = line.split("\t")
    processed_line = ""
    # convert everything to bits/sec and Bytes
    for i in range(len(line_parts)):
        if(line_parts[i] == "KBytes" or line_parts[i]=="Kbits/sec"):
            line_parts[i-1] = str(float(line_parts[i-1])*1000)
            line_parts[i] = line_parts[i][1:]
        elif(line_parts[i] == "MBytes" or line_parts[i]=="Mbits/sec"):
            line_parts[i-1] = str(float(line_parts[i-1])*1000000)
            line_parts[i] = line_parts[i][1:]
        elif(line_parts[i] == "GBytes" or line_parts[i]=="Gbits/sec"):
            line_parts[i-1] = str(float(line_parts[i-1])*1000000000)
            line_parts[i] = line_parts[i][1:]
    # remove units from lines because we only keep the numbers for the
    # resulting CSV-File
    for new_part in line_parts:
        processed_line += (new_part + "\t")
    processed_line = re.sub(r"(Bytes|bits/sec|sec)", "", processed_line)
    return processed_line

# this methods sets the receiver flags for each line -->
# removes the one line in the end that contains this information
# --> therefore we need to travel through the lines in reverse 
def setSndRcvFlags(lines):
    flagged_lines = []
    for i in range(len(lines)):
        reverse_index = len(lines)-1-i
        if(re.match(r".*sender", lines[reverse_index])):
            flag = "0"
        elif(re.match(r".*receiver", lines[reverse_index])):
            flag = "1"
        else:
            # when the server receives data there are no 'Retr'
            # and 'Cwnd[Bytes]' values
            if(flag == "1"):
                lines[reverse_index] += "-\t-\t"
            flagged_lines = [lines[reverse_index] + flag] + flagged_lines
  
    return flagged_lines

def fullSecond(intervallString):
    start = float(intervallString.split("-")[0])
    end = float(intervallString.split("-")[1])
    return (end - start)==1

if __name__ == "__main__":
    main(sys.argv)