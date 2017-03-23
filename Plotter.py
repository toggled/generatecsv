__author__ = 'Naheed'

from pylab import *
from sys import platform, exit
import os
from operator import itemgetter
import matplotlib.pyplot as plt
# import plotly.plotly as py
# import plotly.tools as tls

# tls.set_credentials_file(username='naheed', api_key='na5KlFFjjN7siIq1IL4K')

class Plotter:
    def __init__(self,rootpath,suffixpath,outputfilepath, real):
        self.rootpath = rootpath
        self.suffixpath = suffixpath
        self.outputfilepath = outputfilepath
        self.sourcepath  = rootpath + "/" + suffixpath
        assert os.path.isdir(self.sourcepath) == True
        self.flagmeaning = {0: 'Star', 1: 'Complete', 2: 'Wheel', 3: 'Cycle'}
        self.algoht = {}
        self.real = real
        self.delta = 0.0000001
        self.generateres()

    def generateres(self):
        for file in os.listdir(self.sourcepath):
            # print file
            if file.find("txt") == -1:
                continue
            # print file
            with open(self.sourcepath + "/" + file, 'r') as f:
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
                        self.algoht['Star'] = self.algoht.get('Star', [])

                    if line.startswith("Complete"):
                        flag = 1
                        self.algoht['Complete'] = self.algoht.get('Complete', [])

                    if line.startswith("Wheel"):
                        flag = 2
                        self.algoht['Wheel'] = self.algoht.get('Wheel', [])

                    if line.startswith("Circle"):
                        flag = 3
                        self.algoht['Cycle'] = self.algoht.get('Cycle', [])

                    if flag != -1:
                        # numint = all[i+1].split()[slice(2,5,2)]
                        # areprop = all[i+2].split()[slice(2,5,2)]
                        # concav = all[i+3].split()[slice(2,5,2)]


                        numint = [float(x) for x in all[i + 1].split()[slice(2, 5, 2)]]
                        areprop = [float(x)/100 for x in all[i + 2].split()[slice(2, 5, 2)]]
                        concav = [float(x) for x in all[i + 3].split()[slice(2, 5, 2)]]

                        # try:
                        listofstaff = all[i + 4].split()[1:]
                        key = []
                        val = []
                        for x,y in zip(listofstaff[0::2],listofstaff[1::2]):
                            if int(x.split('x')[0]) != 0:
                                key.append(int(x.split('x')[0]))
                                if float(y) <self.delta:
                                    val.append(0.0)
                                else:
                                    val.append(float(y))


                        uniformity = dict(zip(key, val))
                        # print uniformity

                        # except:
                        #     print "Error" , all[i], all[i + 1], all[i + 2], all[i + 3]


                        # print flagmeaning[flag], algoht[flagmeaning[flag]],algoht['Star']

                        if self.algoht[self.flagmeaning[flag]] != []:
                            # print algoht
                            self.algoht[self.flagmeaning[flag]].append([numhg] + numint + areprop + concav)
                            self.algoht[self.flagmeaning[flag]][-1].append(uniformity)
                        else:
                            self.algoht[self.flagmeaning[flag]] = [[numhg] + numint + areprop + concav]
                            self.algoht[self.flagmeaning[flag]][-1].append(uniformity)
                        flag = -1

        # for x in self.algoht['Star']:
        #     print x , len(x)
        # print self.algoht
        for k, v in self.flagmeaning.items():
            self.algoht[v] = sorted(self.algoht[v], key=itemgetter(0), reverse=True)

    def plot(self):
        fig = plt.figure()
        plt.rc('font', family='serif')
        plt.rc('font', size ='10')
        plt.rc('xtick', labelsize='x-small')
        plt.rc('ytick', labelsize='x-small')

        Xaxis = []
        for key, val in self.algoht.items():
            Xaxis = [i[0] for i in val]

        ab = 1
        for key,val in self.algoht.items():
            # ax = fig.add_subplot(2,2,ab)  # top left
            plotname = key + " associated graph"
            # print plotname, val
            Inters = [i[1] for i in val]
            Intersvar = [i[2] for i in val]
            plt.errorbar(Xaxis, Inters, yerr=Intersvar,label=plotname)
            # if self.suffixpath == "subsampletest":

            plt.xlabel('Number of hyperedges')
            plt.ylabel('Mean number of intersection')

            ab+=1

            # fig.suptitle('Intersecting hyperedges on different sample of' + ["Real","Synthetic"][self.real]+ 'graph')
        legend(loc=2)
        savefig(self.sourcepath+'/Intersection.pdf', bbox_inches='tight')
        # plt.show()
        plt.close()

        fig = plt.figure()

        ab = 1
        for key, val in self.algoht.items():
            # ax = fig.add_subplot(2, 2, ab)  # top left
            plotname = key + " associated graph"
            # print plotname, val
            areaprop = [i[3] for i in val]
            areapropvar = [i[4] for i in val]
            plt.errorbar(Xaxis, areaprop, yerr=areapropvar,label=plotname)
            # if self.suffixpath == "subsampletest":

            plt.xlabel('Number of hyperedges')
            plt.ylabel('Mean number of intersection')

            ab += 1

            # fig.suptitle('Intersecting hyperedges on different sample of' + ["Real","Synthetic"][self.real]+ 'graph')
        legend(loc = 2)
        savefig(self.sourcepath + '/Areaproportion.pdf', bbox_inches='tight')
        # plt.show()
        plt.close()


        fig = plt.figure()
        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.99, top=0.99, wspace=0.2)

        ab = 1
        for key, val in self.algoht.items():
            ax = fig.add_subplot(2, 2, ab)  # top left
            plotname = key + " associated graph"
            # print plotname, val
            areaprop = [i[5] for i in val]
            areapropvar = [i[6] for i in val]
            plt.errorbar(Xaxis, areaprop, yerr=areapropvar, label=plotname)
            # if self.suffixpath == "subsampletest":

            ax.set_xlabel('Number of hyperedges')
            ax.set_ylabel('Mean number of concave shapes')
            ax.legend(loc=2, fontsize = 10)
            ab += 1

            # fig.suptitle('Intersecting hyperedges on different sample of' + ["Real","Synthetic"][self.real]+ 'graph')

        savefig(self.sourcepath + '/Concavity.pdf', bbox_inches='tight')
        # plt.show()
        plt.close()

        fig = plt.figure()
        fig.subplots_adjust(left=0.1, bottom=0.1, right=0.99, top=0.99, wspace=0.2)

        ab = 1
        for key, val in self.algoht.items():
            ax = fig.add_subplot(2,2,ab)
            column_labels = Xaxis

            plotname = key + " associated graph"
            # print plotname
            maxx = max([len(x[7]) for x in val])
            row_labels = []
            for i in val:
                for key in i[7].keys():
                    if key not in row_labels:
                        row_labels.append(key)
            row_labels.sort()


            probdict = [i[7].items() for i in val]
            another = []
            print probdict

            for i in probdict:
                ht = {}
                for gridsize,prob in i:
                    ht[gridsize] = prob
                whatever = []

                if len(i) == maxx:
                    # whatever = [self.delta if x<self.delta else x for x in i]
                    for gr in row_labels:
                        if ht.get(gr) < self.delta:
                            whatever.append(self.delta)
                        else:
                            whatever.append(ht.get(gr))

                    another.append(whatever)
                else:
                    for gr in row_labels:
                        if ht.get(gr,-1)!=-1:
                            if ht.get(gr) < self.delta:
                                whatever.append(self.delta)
                            else:
                                whatever.append(ht.get(gr))
                        else:
                            whatever.append(self.delta)
                    # temp = [self.delta]*(maxx-len(i))
                    # whatever = [self.delta if x < self.delta else x for x in i]
                    # whatever.extend(temp)
                    # another.append(whatever)

            probdict = np.log(np.array(another))


            ax.set_xlabel('Grid Size')
            ax.set_ylabel('Number of hyperedge')
            ax.legend(loc=2, fontsize=10)

            ax.set_yticks(np.arange(probdict.shape[0]) + 0.5, minor=False)
            ax.set_xticks(np.arange(probdict.shape[1]) + 0.5, minor=False)
            row_labels = [str(v)  for v in row_labels]
            ax.set_yticklabels(column_labels, minor=False)
            ax.set_xticklabels(row_labels, minor=False)

            ab += 1

            # fig.suptitle('Intersecting hyperedges on different sample of' + ["Real","Synthetic"][self.real]+ 'graph')
            # print probdict
            plt.pcolor(probdict, cmap=plt.cm.Reds)

        savefig(self.sourcepath + '/Regularity.pdf', bbox_inches='tight')
        # plt.show()
        plt.close()


if __name__ == "__main__":

    if platform == "darwin":
        rootpath = "/Users/naheed/Google Drive/Regularplacement_fuchterman_reingold_everything/datasets/realgraph-grid"
        suffixpath1 = "subsampletest"
        suffixpath2 = "randomsampletest"

        outputfilename = "res_agg.csv"

        p = Plotter(rootpath, suffixpath1, outputfilename,real = True)
        p.plot()
        p = Plotter(rootpath, suffixpath2, outputfilename, real = True)
        p.plot()

    elif platform == "win32":
        rootpath = "C:\\Users\\workshop\\Google Drive\\Regularplacement_fuchterman_reingold_everything\\datasets\\synthetic"

        suffixpath1 = "subsampletest"
        suffixpath2 = "randomsampletest"

        outputfilename = "res_agg.csv"

        p = Plotter(rootpath , suffixpath1, outputfilename,real = False)
        p.plot()
        p = Plotter(rootpath, suffixpath2, outputfilename,real = False)
        p.plot()