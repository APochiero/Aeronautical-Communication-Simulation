import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math 
import argparse 
import seaborn as sns
matplotlib.rcParams['font.family'] = "serif"

t = [4.24, 7.42, 10.59, 13.77, 16.95]
k = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2]
colors = ['#944654','#08b2e3', '#9d8df1','#57a773','#484d6d']

plt.style.use('ggplot')
parser = argparse.ArgumentParser(description='Split Data by K')
parser.add_argument('dirPath', help='path of directory containing Results files')
parser.add_argument('distr', help='Distribution of Interarrival time [ exp | const ]')
args = parser.parse_args()
distribution = str(args.distr)
path = str(args.dirPath)
barWidth = 0.035
errorBarStyle = dict(lw=0.5, capsize=2, capthick=0.5)
for i in range(len(t)):
    with open(path + '/ResultT' + str(t[i]) + distribution + '.csv') as file:
        df = pd.read_csv(file, header=None)
        df = df.drop(columns=[0])

        nameDistr = 'Case Exponential interarrival time distribution' if distribution == 'exp' else 'Case Constant interarrival time distribution'

        print('Plotting T' + str(t[i]) + ' ' + distribution)
        responseTime = pd.to_numeric(df.iloc[5], errors='coerce')
        responseTimeCI = pd.to_numeric(df.iloc[6], errors='coerce')
        queueLength = pd.to_numeric(df.iloc[3], errors='coerce')
        queueLengthCI = pd.to_numeric(df.iloc[4], errors='coerce')
        waitingTime = pd.to_numeric(df.iloc[7], errors='coerce')
        waitingTimeCI = pd.to_numeric(df.iloc[8], errors='coerce')
        # Plot Delay
        plt.figure(1)
        plt.errorbar(k, responseTime , yerr=responseTimeCI, fmt="--x", markeredgecolor='red', linewidth=0.8, capsize=4, label = 't= ' + str(t[i]))
        plt.xlabel('Interarrival Time [s]')
        plt.ylabel('Delay [s]')
        plt.ticklabel_format(axis='x', style='sci')
        plt.title(nameDistr + '\nEnd-to-End Delay')
        plt.legend()
        plt.grid(linestyle='--')

        # Plot Queue Length
        plt.figure(2)
        plt.errorbar(k, queueLength, yerr=queueLengthCI, fmt="--x", markeredgecolor='red', linewidth=0.8, capsize=4, label = 't= ' + str(t[i]))
        plt.xlabel('Interarrival Time [s]')
        plt.ylabel('Queue Length')
        plt.ticklabel_format(axis='x', style='sci')
        plt.title(nameDistr + '\nQueue Length Analysis') 
        plt.legend()
        plt.grid(linestyle='--')

        # Bar plot Waiting Time Over Response Time
        plt.figure(3)
        x = [ x - 0.04*(2-i) for x in k ]
        plt.bar(x, responseTime, yerr=responseTimeCI, width=barWidth, error_kw=errorBarStyle, color='red' )
        plt.bar(x, waitingTime, yerr=waitingTimeCI, width=barWidth, error_kw=errorBarStyle, label='t=' + str(t[i]), color = colors[i])
        plt.xlabel('Interarrival Time [s]')
        plt.ylabel('Time [s]')
        plt.ticklabel_format(axis='x', style='sci')
        plt.title(nameDistr + '\nWaiting Time over Response Time')
        plt.legend()
        plt.grid(linestyle='--')

plt.show()