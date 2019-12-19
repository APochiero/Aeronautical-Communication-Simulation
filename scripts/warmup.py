import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import argparse

def main():
    parser = argparse.ArgumentParser(description='Split Data by K')
    parser.add_argument('path', help='path of .csv file to be splitted')
    parser.add_argument('rep', type=int, help='repetition')
    parser.add_argument('window', type=int, help='window size')
    parser.add_argument('k', help='k of csv file')
    args = parser.parse_args()

    delay = []
    simTime = []

    window = args.window
    k = args.k
    nRep = args.rep
    path = args.path
    df = pd.read_csv(path)
    responseTimeDF = df.filter(regex='^k=' + k +' responseTime',axis=1)

    for i in range(nRep):
        values = []
        # nth repetition of responseTime
        regex = '^k=' + k + ' responseTime ' + str(i) + '$'
        repetition = responseTimeDF.filter(regex=regex,axis=1)
       
        # nth time 
        regexTime = '^k=' + k + ' time ' + str(i) + "$"
        timeSeries = df.filter(regex=regexTime,axis=1)

        dfRep = timeSeries.merge(repetition, left_index=True, right_index=True)
        dfRep = dfRep.dropna()

        if i == 0:
            timeSeries = timeSeries.dropna()
            dfMeans = timeSeries
        
        mean = pd.Series(dfRep[regex[1:-1]]).rolling(window, 1).mean()
        dfMeans['mean ' + str(i)] = mean
        plt.figure(1)
        plt.plot(dfRep[regexTime[1:-1]], mean)
        plt.xlabel('simTime (s)')
        plt.ylabel('Delay (s)')
        plt.ticklabel_format(axis='x', style='sci')
        plt.grid(linestyle='--')

    dfMeans['Variance'] = dfMeans.filter(regex='^mean').var(axis=1)
    
    indexMin = dfMeans['Variance'].idxmin(axis=0)
    print('\nTime at minimum variance (window size: ' + str(window) + '): ' + str(dfMeans.loc[indexMin, 'k='+k+' time 0']) + ' with variance: ' + str(dfMeans.loc[indexMin, 'Variance']))
    plt.figure(2)
    plt.plot(dfMeans['k='+k+' time 0'], dfMeans['Variance'].apply(lambda x : math.log(x,10)))

    plt.xlabel('simTime (s)')
    plt.ylabel('Variance')
    plt.ticklabel_format(axis='x', style='sci')
    plt.grid(linestyle='--')
    plt.show()


if __name__ == "__main__":
    main()