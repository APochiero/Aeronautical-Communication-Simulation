import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import uniform as unif
from scipy.stats import linregress as regr

M = 25000
T = 0.00000000425603
nameOrder = ['interarrival', 'serviceTime', 'queueLength', 'responseTime', 'waitingTime']

'''
    Load and rename columnn using nameOrder list.
    CSV File must containt data with the following order:
    time, interarrival, time, serviceTime, time, queueLength, time, responseTime, time, waitingTime 
    repeated {repetition} times 

    columns of time are deleted
'''
def loadData(path, repetition) :
    df = pd.read_csv(path + '.csv')
    names = []
    for i in range(repetition):
        for j in range(len(nameOrder)):
            names.append('time') 
            names.append(nameOrder[j] + str(i))

    df.columns = names
    df = df.drop(columns='time')
    df = df[:math.floor(len(df)*0.7)]
    return df

'''
    Find every column of dataframe that starts with "stat"
'''
def splitStat(df, stat):
    statDf = df[df.columns[pd.Series(df.columns).str.startswith(stat)]]
    return statDf

'''
    Sort every column of dataframe and perform a mean per row
'''
def meanPerRow(df, stat):
    orderedStat = df.apply(lambda x: x.sort_values().values)
    return pd.DataFrame(orderedStat.mean(axis=1), columns = [stat])
 
def histogram(  df, nbin, path, name, k ) :
    plt.figure()
    n, bins, patches = plt.hist(df['Mean_' + name ], nbin, density=True, facecolor='g', alpha=0.75)
    plt.title('Histogram of ' + name + ' ' + k + 's')
    plt.grid(True)
    plt.savefig(path + '.png')

'''
    Service Time Cumulative Distribution Function F(s)
'''
def serviceTimeCDF(s):
    if s < 0:
        Fs = 0
    elif s <= T*M**2/4:
        Fs = math.pi * s/(T*M**2)
    elif s <= T*M**2/2:
        Fs = math.pi * s/(T*M**2) - 4*s/(T*M**2)*math.acos(M/2*math.sqrt(T/s)) + math.sqrt(4*s/(T*M**2)-1)
    else:
        Fs = 1.0
    return Fs

'''
    Distance Cumulative Distribution Function F(d)
'''
def distanceCDF(d):
    if d < 0:
        Fd = 0
    elif d <= M/2:
        Fd = math.pi*d**2/M**2
    elif d <= M/2*math.sqrt(2):
        Fd = math.pi*d**2/M**2 - 4/M**2*d**2*math.acos(M/(2*d)) + d/M*math.sqrt((4*d**2-M**2)/d**2)
    else:
        Fd = 1.0
    return Fd

'''
    look for x such that F(x) = P{X < x} = quantile, with an error of maxError
'''
def findQuantile(quantile, name, maxError):
    x = 0.0
    if name == 'serviceTime':
        error = quantile - serviceTimeCDF(x)
        while error > maxError:
            x += 0.1*error 
            error = quantile - serviceTimeCDF(x)
    elif name == 'distance' :
        error = quantile - distanceCDF(x)
        while error > maxError:
            x += 0.1*error 
            error = quantile - distanceCDF(x)
    return x

'''
     find every quantile for both theoretical and sample distribution
'''
def fitDistribution(df, name, maxError):
    theoreticalQ = []
    sampleQ = []
    for i in range(1, len(df)):
        quantile = (i-0.5)/len(df)
        sq = df[name].quantile(quantile)
        tq = findQuantile(quantile, name, maxError)
        sampleQ.append(sq)
        theoreticalQ.append(tq)
        print(quantile, tq, sq)
    return [theoreticalQ, sampleQ]

'''
     draw a qq plot
'''
def qqPlot(theoreticalQ, sampleQ, name ):
    slope, intercept, r_value, p_value, std_err = regr(theoreticalQ, sampleQ)

    plt.figure()
    plt.scatter(theoreticalQ, sampleQ, s=0.8, label=name)
    y = [ x*slope + intercept for x in theoreticalQ ]
    plt.plot(theoreticalQ, y, 'r', label='Trend line')
    plt.text(0, max(sampleQ)*0.6, '\n\nR^2 = ' + str('%.6f'%r_value**2))
    plt.text(0, max(sampleQ)*0.55, 'y = ' + str('%.6f'%slope) + 'x + ' + str('%.6f'%intercept))
    plt.xlabel('Theoretical Quantile')
    plt.ylabel('Sample Quantile')
    plt.title('QQ plot ' + name)
    plt.grid(True)
    plt.legend()

def main():
    '''
        Service Time fitting
    '''
    data = loadData('K2s', 30)
    serviceTime30Rep = splitStat(data, 'serviceTime')
    serviceTime = meanPerRow(serviceTime30Rep, 'serviceTime')

    serviceTime = serviceTime.sample(n=1000)
    
    theoreticalQ, sampleQ = fitDistribution(serviceTime, 'serviceTime', 0.0001)
    qqPlot(theoreticalQ, sampleQ, 'serviceTime' )

    '''
        Distance Time fitting
    '''
    distance30Rep = pd.read_csv('distance.csv')
    names = []
    for i in range(30):
        names.append('time')
        names.append('distance' + str(i))
    
    distance30Rep.columns = names
    distance30Rep = distance30Rep.drop(columns='time')
    distance = meanPerRow(distance30Rep, 'distance')
    distance = distance.sample(n=1000)
    
    theoreticalQ, sampleQ = fitDistribution(distance, 'distance', 0.0001)
    qqPlot(theoreticalQ, sampleQ, 'distance' )

    plt.show()

if __name__ == "__main__":
    main()


