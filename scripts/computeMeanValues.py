import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import argparse
# The following arrays must be set before running the script

# Order of statistics in the csv file
nameOrder = ['serviceTime', 'queueLength', 'responseTime', 'waitingTime']
k = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2]

'''
    Load and rename columnn using nameOrder list.
    CSV File must containt data with the following order:
    serviceTime, queueLength, responseTime, waitingTime 
    each repeated {repetition} times 
'''


def loadData(path, repetition):
    with open(path + '.csv') as file:
        df = pd.read_csv(file)
        names = []
        for i in range(repetition):
            for j in range(len(nameOrder)):
                names.append(nameOrder[j] + str(i))

        df.columns = names
        return df


'''
    For each repetition of the statistic compute the mean after 
    dropping NaN values of that column. 
    Return mean of all columns' means
'''


def computeMeanValues(df, repetition):
    means = pd.Series([])
    for i in range(repetition):
        series = df.iloc[:, [i]].dropna().mean()
        means = pd.concat([means, series], ignore_index=True)
        # print(means)

    return means.mean()


'''
    For each repetition of the statistic compute the variance after 
    dropping NaN values of that column. 
    Return mean of all columns' variances
'''


def computeAvgVariance(df, repetition):
    variances = pd.Series([])
    for i in range(repetition):
        series = df.iloc[:, [i]].dropna().var()
        variances = pd.concat([variances, series], ignore_index=True)
        # print(variances)
    return variances.mean()


def computeSampleVariance(df, repetition):
    sampleMean = computeMeanValues(df, repetition)
    sampleVariance = 0.0
    for i in range(repetition):
        mean = df.iloc[:, [i]].dropna().mean()
        d = mean - sampleMean
        sampleVariance += d.iloc[0]**2
    return sampleVariance/(repetition - 1)


def main():
    parser = argparse.ArgumentParser(description='Compute Mean Values')
    parser.add_argument('dirPath', help='path of dir containing .csv files')
    parser.add_argument('--rep', type=int, help='repetition', default=30)
    parser.add_argument('t', help='value of t ( check handover period)')
    parser.add_argument(
        'distr', help='type of arrival distribution ( const or exp )')

    args = parser.parse_args()
    repetition = args.rep
    path = str(args.dirPath)
    columnsNames = ['K = ' + str(x) + 's' for x in k]
    # Names of result's rows
    rowNames = ['Service Time Mean', 'Service Time Var', 'Queue Length Mean', 'Queue Length CI',
                'Response Time Mean', 'Response Time CI', 'Waiting Time Mean', 'Waiting Time CI']
    result = pd.DataFrame([])
    for h in range(len(k)):
        data = loadData(path + '/K' + str(k[h]) + 's', repetition)
        print('\n\nK = ' + str(k[h]))
        statList = []
        for i in range(len(nameOrder)):
            # select columns of that statistic ( i.e 30 columns of serviceTime )
            stat = data[data.columns[pd.Series(
                data.columns).str.startswith(nameOrder[i])]]
            mean = computeMeanValues(stat, repetition)
            statList.append(mean)
            # for the serviceTime compute also the variance
            if nameOrder[i] == 'serviceTime':
                stat = data[data.columns[pd.Series(
                    data.columns).str.startswith(nameOrder[i])]]
                var = computeAvgVariance(stat, repetition)
                statList.append(var)

            if nameOrder[i] == 'responseTime' or nameOrder[i] == 'queueLength' or nameOrder[i] == 'waitingTime':
                stat = data[data.columns[pd.Series(
                    data.columns).str.startswith(nameOrder[i])]]
                sampleVariance = computeSampleVariance(
                    stat, repetition)
                # 99% CI
                confidenceInterval = math.sqrt(sampleVariance/repetition)*2.326
                statList.append(confidenceInterval)
                # print(confidenceInterval)

        # add series to the final result
        series = pd.Series(statList)
        series.index = rowNames
        result[columnsNames[h]] = series
        print(result[columnsNames[h]])

    # save results in a new csv file
    result.to_csv(path + '/ResultT' + str(args.t) + str(args.distr) + '.csv')
    print(result)


if __name__ == "__main__":
    main()
