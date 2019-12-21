import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import argparse
import os

# The following arrays must be set before running the script

# Order of statistics in the csv file 
nameOrder = ['serviceTime', 'queueLength', 'responseTime', 'waitingTime']
nameOrderTime = [ 'time', 'serviceTime', 'time', 'queueLength', 'time', 'responseTime', 'time', 'waitingTime']

# Values of k in th csv file
k = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2]


def main():
    parser = argparse.ArgumentParser(description='Split Data by K')
    parser.add_argument('path', help='path of .csv file to be splitted')
    parser.add_argument('--rep', type=int, help='repetition', default=30)
    parser.add_argument('--keepSimTime', help='keep simTime columns', action='store_true')

    args = parser.parse_args()
    repetition = args.rep
    keepSimTime = args.keepSimTime 
    path = str(args.path)[:-4]
    with open(path + '.csv') as file:
        df = pd.read_csv( file, nrows = 10)
        
        # Test if csv file has the expected number of columns 
        if not 2*len(nameOrder)*len(k)*repetition == len(df.columns):
            print('\n\nVerify extraction or parameters, these numbers must be equal: ' + str(2*len(nameOrder)*len(k)*repetition) , len(df.columns))
            print('\n')
            return
        # print(df)

    if not os.path.exists(path):
        os.mkdir(path)

    # for every k value of the csv file
    for h in range(len(k)):
        names = []
    
        if not keepSimTime:
            # select just odd of columns, the even ones are those for the time
            selectedColumns = [i*2-1 for i in range(1+len(nameOrder)*h*repetition, 1+len(nameOrder)*(h+1)*(repetition))]
        else:
            selectedColumns = [i for i in range(2*len(nameOrder)*h*repetition, 2*len(nameOrder)*(h+1)*(repetition))]

        print('\n\nReading columns from ' + str(selectedColumns[0]) + ' to ' + str(selectedColumns[-1]) )
        with open(path + '.csv') as file:
            df = pd.read_csv(file, usecols=selectedColumns)
            for i in range(repetition):
                if keepSimTime:
                    for j in range(len(nameOrderTime)):    
                    # kValues + statisticName + repetition (example k=0.1 interarrivalTime 15)
                        names.append('k=' + str(k[h]) + ' ' + nameOrderTime[j] + ' ' + str(i))
                else:
                    for j in range(len(nameOrder)):    
                        names.append('k=' + str(k[h]) + ' ' + nameOrder[j] + ' ' + str(i))

            df.columns = names
            # filter by column name 
            dfK = df.filter(regex='^k=' + str(k[h]),axis=1)
            print(dfK.iloc[:10,[0,1,2,3,4,5,6,7,8]], '\n...')
            filename = 'K' + str(k[h]) + 'sWithTime.csv' if keepSimTime else 'K' + str(k[h]) + 's.csv'
            # save a new csv file for this K value
            dfK.to_csv(path + '/' + filename, index=None)
            print('Created K' + str(k[h]) + 's.csv')


if __name__ == "__main__":
    main()