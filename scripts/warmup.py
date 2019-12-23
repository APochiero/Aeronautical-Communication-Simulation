import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import argparse
import seaborn as sns
import matplotlib
matplotlib.rcParams['font.family'] = "serif"
plt.style.use('ggplot')


def main():
    parser = argparse.ArgumentParser(description='Split Data by K')
    parser.add_argument('path', help='path of .csv file to be splitted')
    parser.add_argument('--rep', type=int, help='repetition', default=10)
    parser.add_argument('window', type=int, help='window size')
    parser.add_argument('k', help='k of csv file')
    args = parser.parse_args()

    delay = []
    simTime = []

    window = args.window
    k = args.k
    nRep = args.rep
    path = args.path
    with open(path) as file:
        df = pd.read_csv(path)
    responseTimeDF = df.filter(regex='^k=' + k + ' responseTime', axis=1)

    for i in range(nRep):
        values = []
        # nth repetition of responseTime
        regex = '^k=' + k + ' responseTime ' + str(i) + '$'
        repetition = responseTimeDF.filter(regex=regex, axis=1)

        # nth time
        regexTime = '^k=' + k + ' time ' + str(i) + "$"
        timeSeries = df.filter(regex=regexTime, axis=1)

        # dataframe with [ time , responseTime ]
        dfRep = timeSeries.merge(repetition, left_index=True, right_index=True)
        dfRep = dfRep.dropna()

        # use the Time 0 columns as time of dfMeans
        # (  structure of dfMeans : time 0 | mean 0 | mean 1 | mean 2 | .... | mean {repetition -1 } | variance by row | )
        if i == 0:
            timeSeries = timeSeries.dropna()
            dfMeans = timeSeries

        # compute means using the sliding window for ith repetition
        mean = pd.Series(dfRep[regex[1:-1]]).rolling(window, 1).mean()
        # add to dfMeans dataframe
        dfMeans['mean ' + str(i)] = mean
        plt.figure(1)
        plt.plot(dfRep[regexTime[1:-1]], mean)
        plt.xlabel('simTime [s]')
        plt.ylabel('Delay [s]')
        plt.title('Warm Up Analysis\n Window Size =' + str(window))
        plt.ticklabel_format(axis='x', style='sci')
        plt.grid(linestyle='--')

    # add variance series, computed by row ( axis = 1 )
    dfMeans['Variance'] = dfMeans.filter(regex='^mean').var(axis=1)
    dfMeans['Mean of Means'] = dfMeans.filter(regex='^mean').mean(axis=1)
    plt.figure(3)
    plt.plot(dfMeans['k='+k+' time 0'], dfMeans['Mean of Means'])
    print(len(dfMeans))

    # find the index of minimum variance
    indexMin = dfMeans.loc[100:, 'Variance'].idxmin(axis=0)
    print('\nTime at minimum variance (window size: ' + str(window) + '): ' +
          str(dfMeans.loc[indexMin, 'k='+k+' time 0']) + ' with variance: ' + str(dfMeans.loc[indexMin, 'Variance']))
    plt.figure(2)
    plt.plot(dfMeans['k='+k+' time 0'],
             dfMeans['Variance'].apply(lambda x: math.log(x, 10)))

    plt.xlabel('simTime (s)')
    plt.ylabel('Variance')
    plt.ticklabel_format(axis='x', style='sci')
    plt.grid(linestyle='--')
    plt.show()


if __name__ == "__main__":
    main()
