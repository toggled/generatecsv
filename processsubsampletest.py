__author__ = 'Naheed'

import os, sys
import csv
from operator import itemgetter
from sys import platform



def aggregateresults(sourcepath, outputfilename):
    assert os.path.isdir(sourcepath) == True
    flagmeaning = {0: 'Star', 1: 'Complete', 2: 'Wheel', 3: 'Circle'}
    algoht = {}
    for file in os.listdir(sourcepath):
        print file
        with open(sourcepath + "/" + file, 'r') as f:
            all = f.readlines()
            flag = -1
            numhg = -1
            for i, val in enumerate(range(len(all))):
                line = all[i]

                if numhg == -1:
                    if line.startswith("# hyperedges"):
                        numhg = int(line.split()[-1])

                if line.startswith("Star"):
                    flag = 0
                    algoht['Star'] = algoht.get('Star', [])

                if line.startswith("Complete"):
                    flag = 1
                    algoht['Complete'] = algoht.get('Complete', [])

                if line.startswith("Wheel"):
                    flag = 2
                    algoht['Wheel'] = algoht.get('Wheel', [])

                if line.startswith("Circle"):
                    flag = 3
                    algoht['Circle'] = algoht.get('Circle', [])

                if flag != -1:
                    # numint = all[i+1].split()[slice(2,5,2)]
                    # areprop = all[i+2].split()[slice(2,5,2)]
                    # concav = all[i+3].split()[slice(2,5,2)]


                    numint = [float(x) for x in all[i + 1].split()[slice(2, 5, 2)]]
                    areprop = [float(x) for x in all[i + 2].split()[slice(2, 5, 2)]]
                    concav = [float(x) for x in all[i + 3].split()[slice(2, 5, 2)]]

                    try:
                        uniformity = ' '.join(all[i + 4].split()[1:])
                    except:
                        print all[i], all[i + 1], all[i + 2], all[i + 3]
                        sys.exit(1)
                    # print flagmeaning[flag], algoht[flagmeaning[flag]],algoht['Star']
                    if algoht[flagmeaning[flag]] != []:
                        # print algoht
                        algoht[flagmeaning[flag]].append([numhg] + numint + areprop + concav)
                        algoht[flagmeaning[flag]][-1].append(uniformity)
                    else:
                        algoht[flagmeaning[flag]] = [[numhg] + numint + areprop + concav]
                        algoht[flagmeaning[flag]][-1].append(uniformity)
                    flag = -1
    #
    # for x in algoht['Star']:
    #     print x , len(x)

    for k, v in flagmeaning.items():
        algoht[v] = sorted(algoht[v], key=itemgetter(0), reverse=True)

    for k, v in flagmeaning.items():
        if platform == "darwin":
            csvf = open(sourcepath + "/" + v + "_" + outputfilename, 'wt')
        elif platform == 'win32':
            csvf = open(sourcepath + "\\" + v + "_" + outputfilename, 'wt')
        try:
            writer = csv.writer(csvf)
            writer.writerow(('NumHyperedges', 'IntersectionMean', 'IntersectionSD', 'AreaPropMean', 'AreaPropSD',
                             'ConcavityMean', 'ConcavitySD', 'Uniformity'))
            for line in algoht[v]:
                writer.writerow(line)
        finally:
            csvf.close()


def main():
    if platform == "darwin":
        rootpath = "/Users/naheed/Google Drive/Regularplacement_fuchterman_reingold_everything/datasets"
        suffixpath = "subsampletest"

        outputfilename = "res_agg.csv"
        aggregateresults(rootpath + "/" + suffixpath, outputfilename)

    elif platform == "win32":

        rootpath = "/Users/naheed/Google Drive/Regularplacement_fuchterman_reingold_everything/datasets"

        suffixpath = "subsampletest"

        outputfilename = "res_agg.csv"
        aggregateresults(rootpath + "/" + suffixpath, outputfilename)


if __name__ == "__main__":
    main()
