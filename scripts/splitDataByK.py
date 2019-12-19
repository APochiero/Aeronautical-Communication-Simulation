import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import argparse
import os


nameOrder = ['serviceTime', 'queueLength', 'responseTime', 'waitingTime']
nameOrderTime = [ 'time', 'serviceTime', 'time', 'queueLength', 'time', 'responseTime', 'time', 'waitingTime']

k = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 2.0, 3.0, 5.0, 10.0]
# k = [2.0]


def main():
    parser = argparse.ArgumentParser(description='Split Data by K')
    parser.add_argument('path', help='path of .csv file to be splitted')
    parser.add_argument('rep', type=int, help='repetition')
    parser.add_argument('kst', type=bool, help='keep simTime columns')

    args = parser.parse_args()
    repetition = args.rep
    keepSimTime = args.kst 
    path = str(args.path)[:-4]
    df = pd.read_csv(path + '.csv', nrows = 10)
    if not 2*len(nameOrder)*len(k)*repetition == len(df.columns):
        print('\n\nVerify extraction or parameters, these numbers must be equal: ' + str(2*len(nameOrder)*len(k)*repetition) , len(df.columns))
        print('\n')
        return
    # print(df)

    if not os.path.exists(path):
        os.mkdir(path)
    # for h in range(len(k)):
    h = 8
    names = []
    if not keepSimTime:
        selectedColumns = [i*2-1 for i in range(1+len(nameOrder)*h*repetition, 1+len(nameOrder)*(h+1)*(repetition))]
    else:
        selectedColumns = [i for i in range(2*len(nameOrder)*h*repetition, 2*len(nameOrder)*(h+1)*(repetition))]
        print(selectedColumns)

    print('\n\nReading columns from ' + str(selectedColumns[0]) + ' to ' + str(selectedColumns[-1]) )
    df = pd.read_csv(path + '.csv', usecols=selectedColumns)
    for i in range(repetition):
        if keepSimTime:
            for j in range(len(nameOrderTime)):    
            # kValues + statisticName + repetition (example k=0.1 interarrivalTime 15)
                names.append('k=' + str(k[h]) + ' ' + nameOrderTime[j] + ' ' + str(i))
        else:
            for j in range(len(nameOrder)):    
                names.append('k=' + str(k[h]) + ' ' + nameOrder[j] + ' ' + str(i))

    df.columns = names
    dfK = df.filter(regex='^k=' + str(k[h]),axis=1)
    print(dfK.iloc[:10,[0,1,2,3,4,5,6,7,8]], '\n...')
    filename = 'K' + str(k[h]) + 'sWithTime.csv' if keepSimTime else 'K' + str(k[h]) + 's.csv'
    dfK.to_csv(path + '/' + filename, index=None)
    print('Created K' + str(k[h]) + 's.csv')


if __name__ == "__main__":
    main()