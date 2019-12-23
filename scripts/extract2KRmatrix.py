import pandas as pd
import math
import argparse

# The following arrays must be set before running the script
# Order of statistics in the csv file 
nameOrder = ['serviceTime', 'queueLength', 'responseTime', 'waitingTime']
K = [0.5, 2]
T = [4.24, 16.95]
P = [1, 2]

def loadData(path, repetition):
    with open(path + '.csv') as file:
        df = pd.read_csv(file)
        names = []
        for i in range(repetition):
            for j in range(len(nameOrder)):
                names.append(nameOrder[j] + str(i))
        df.columns = names
        return df

def main():
    parser = argparse.ArgumentParser(description='Compute Mean Values')
    parser.add_argument('dirPath', help='path of dir containing .csv files')
    parser.add_argument('--rep', type=int, help='repetition', default=30)    

    args = parser.parse_args()
    repetition = args.rep
    path = str(args.dirPath)
    
    columnsNames = []
    for p in P:
        for t in T:
            for k in K:
                columnsNames.append('p' + str(p) + 't' + str(t) + 'k' + str(k))

    result = pd.DataFrame([])
    for p in range(len(P)):
        for t in range(len(T)):
            for k in range(len(K)):
                data = loadData(path + '/p' + str(P[p]) + 't' + str(T[t]) + 'k' + str(K[k]), repetition)
                # print('\n\np' + str(P[p]) + 't' + str(T[t]) + 'k' + str(K[k]))
                stat = data.filter(regex='^queueLength', axis=1)
                statSeries = pd.Series([])
                for r in range(repetition):
                    mean = stat.iloc[:,[r]].dropna().mean()
                    statSeries = pd.concat([statSeries, mean])              
                print(statSeries)
                result[columnsNames[k + t*len(T) + p*len(T)*len(P)]] = statSeries

    # save results in a new csv file
    result.to_csv(path + '/2KRmatrixQL' + '.csv')
    print(result)

if __name__ == "__main__":
    main()