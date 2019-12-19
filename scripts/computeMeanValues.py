import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import argparse

nameOrder = ['serviceTime', 'queueLength', 'responseTime', 'waitingTime']
k = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 2.0, 3.0, 5.0, 10.0]
# k = [0.2]
def loadData(path, repetition):
    df = pd.read_csv(path + '.csv')
    names = []
    for i in range(repetition):
        for j in range(len(nameOrder)):
            names.append(nameOrder[j] + str(i))

    df.columns = names
    return df

def computeMeanValues(df, name, repetition):
    means = pd.Series([])
    for i in range(repetition):
        series = df.iloc[:,[i] ].dropna().mean()
        means = pd.concat([means, series], ignore_index=True)
        # print(means)

    return means.mean()

def computeVariance(df, name, repetition):
    variances = pd.Series([])
    for i in range(repetition):
        series = df.iloc[:,[i] ].dropna().var()
        variances = pd.concat([variances, series], ignore_index=True)
        # print(variances)     
    return variances.mean()

def main():
    parser = argparse.ArgumentParser(description='Compute Mean Values')
    parser.add_argument('path', help='path of .csv file')
    parser.add_argument('rep', type=int, help='repetition')

    args = parser.parse_args()
    repetition = args.rep
    path = str(args.path)
    columnsNames = ['K = ' + str(x) + 's' for x in k ]
    rowNames = ['Service Time Mean', 'Service Time Var', 'Queue Length Mean', 'Response Time Mean', 'Waiting Time Mean']
    result = pd.DataFrame([])
    for h in range(len(k)):
        data = loadData(path + '/K' + str(k[h]) + 's', repetition )
        print('\n\nK = ' + str(k[h]))
        statList = [] 
        for i in range(len(nameOrder)):
            stat = data[data.columns[pd.Series(data.columns).str.startswith(nameOrder[i])]]
            mean = computeMeanValues(stat, nameOrder[i], repetition)
            statList.append(mean)
            if nameOrder[i] == 'serviceTime':
                stat = data[data.columns[pd.Series(data.columns).str.startswith(nameOrder[i])]]
                var = computeVariance(stat, nameOrder[i], repetition)
                statList.append(var)
        series = pd.Series(statList)
        series.index = rowNames
        result[columnsNames[h]] = series
        print(result[columnsNames[h]])

    result.to_csv(path + '/Result.csv')
    print(result)

if __name__ == "__main__":
    main()