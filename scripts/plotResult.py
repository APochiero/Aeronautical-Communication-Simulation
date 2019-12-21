import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math 
import argparse 
import seaborn as sns
matplotlib.rcParams['font.family'] = "serif"

t = [4.24, 7.42, 10.59, 13.77, 32.84]
k = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2]

plt.style.use('ggplot')
parser = argparse.ArgumentParser(description='Split Data by K')

parser.add_argument('distr', help='Distribution of Interarrival time [ exp | const ]')
args = parser.parse_args()
distribution = str(args.distr)

for i in range(len(t)):
    with open('ResultT' + str(t[i]) + distribution + '.csv') as file:
        df = pd.read_csv(file, header=None)
        df = df.drop(columns=[0])

        print('Plotting T' + str(t[i]) + ' ' + distribution)
        responseTime = pd.to_numeric(df.iloc[5], errors='coerce')
        responseTimeCI = pd.to_numeric(df.iloc[6], errors='coerce')
        queueLength = pd.to_numeric(df.iloc[3], errors='coerce')
        queueLengthCI = pd.to_numeric(df.iloc[4], errors='coerce')
        waitingTime = pd.to_numeric(df.iloc[7], errors='coerce')
        waitingTimeCI = pd.to_numeric(df.iloc[8], errors='coerce')

        plt.figure(1)
        plt.errorbar(k, responseTime , yerr=responseTimeCI, fmt="--x", markeredgecolor='red', linewidth=0.8, capsize=4, label = 't= ' + str(t[i]))

        plt.xlabel('Interarrival Time [s]')
        plt.ylabel('Delay [s]')
        plt.ticklabel_format(axis='x', style='sci')
        plt.title('End-to-End Delay Analysis')
        plt.legend()
        plt.grid(linestyle='--')

        plt.figure(2)
        plt.errorbar(k, queueLength, yerr=queueLengthCI, fmt="--x", markeredgecolor='red', linewidth=0.8, capsize=4, label = 't= ' + str(t[i]))
        plt.xlabel('Interarrival Time [s]')
        plt.ylabel('Queue Length')
        plt.ticklabel_format(axis='x', style='sci')
        plt.title('Queue Length Analysis')
        plt.legend()
        plt.grid(linestyle='--')

        plt.figure(10-i)
        plt.bar(k, responseTime, yerr=responseTimeCI, width=0.05, capsize=4, label='E[R]@t=' + str(t[i]) )
        plt.bar(k, waitingTime, yerr=waitingTimeCI, width=0.05,capsize=4, label='E[W]@t=' + str(t[i]))
        plt.xlabel('Interarrival Time [s]')
        plt.ylabel('Time [s]')
        plt.ticklabel_format(axis='x', style='sci')
        plt.title('Waiting Time over Response Time')
        plt.legend()
        plt.grid(linestyle='--')


plt.show()