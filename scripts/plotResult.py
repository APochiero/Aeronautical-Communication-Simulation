import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math 
# t = [4.24, 7.42, 10.59, 13.77, 16.95]
t = [4.24, 7.42, 13.77, 16.95]
k = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2]

distribution = 'exp'


for i in range(len(t)):
    with open('ResultT' + str(t[i]) + distribution + '.csv') as file:
        df = pd.read_csv(file, header=None)
        df = df.drop(columns=[0])

        print('Plotting T' + str(t[i]) + ' ' + distribution)
        plt.figure(1)
        plt.errorbar(k, pd.to_numeric(df.iloc[5], errors='coerce'), yerr=df.iloc[6], fmt='-x', label = 't= ' + str(t[i]))

        plt.xlabel('Interarrival Time [s]')
        plt.ylabel('Delay [s]')
        plt.ticklabel_format(axis='x', style='sci')
        plt.title('End-to-End Delay Analysis')
        plt.legend()
        plt.grid(linestyle='--')

        plt.figure(2)
        plt.errorbar(k, pd.to_numeric(df.iloc[3], errors='coerce'), yerr=df.iloc[4], fmt='-x', label = 't= ' + str(t[i]))
        plt.xlabel('Interarrival Time [s]')
        plt.ylabel('Queue Length')
        plt.ticklabel_format(axis='x', style='sci')
        plt.title('Queue Length Analysis')
        plt.legend()
        plt.grid(linestyle='--')

plt.show()