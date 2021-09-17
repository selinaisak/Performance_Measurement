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
    csvHeader = "Iteration,Bytes,IP,icmp_seq,ttl,time[ms]"
    lines = fetchRelevantLines(file)
    lines = setIterationNumber(lines)
    csvFile = open(filename + ".csv", "w")
    csvFile.write(csvHeader + "\n")
    for line in lines:
        line = re.sub("\t+", ",", line)
        if(line[-1]==','):
            line = line[:-1]
        csvFile.write(line+"\n")
        print(line)
    csvFile.close()

# this method filters the Log-File for the relevant lines
# so only the data regarding sending/receiving data are saved
def fetchRelevantLines(file):
    lines = file.readlines()
    relevantLines = []
    for i in range(len(lines)):
        if(re.match(r"([-]+\s(ITERATION:)\s[0-9]+\s[-]+)|([0-9]+\s(bytes))", lines[i])):
            lines[i] = re.sub(r"[-]+\s|\s[-]+", "", lines[i])
            lines[i] = re.sub(r"\s+", "\t", lines[i])
            lines[i] = re.sub(r"[a-z|_|:]+[=]?", "", lines[i])    
            relevantLines += [lines[i]]
    return relevantLines


# this methods sets the iteration number for each line -->
def setIterationNumber(lines):
    new_lines = []
    iteration = 0
    for i in range(len(lines)):
        if(re.match(r"((ITERATION)\t[0-9]+)", lines[i])):
            iteration = int(lines[i].split("\t")[1])
        else:
            lines[i] = str(iteration) + "\t" + lines[i]
            new_lines.append(lines[i])
    return new_lines

if __name__ == "__main__":
    main(sys.argv)