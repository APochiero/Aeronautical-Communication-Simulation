import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


lifo = pd.read_csv('LIFO.csv')
fifo = pd.read_csv('FIFO.csv')
gi = pd.read_csv('GI.csv')
li = pd.read_csv('LI.csv')

tail = 1000

total = fifo.merge(lifo, on='time', how='outer').merge(gi, on='time', how='outer').merge(li, on='time', how='outer')
# total.rename(columns={'time' , 'serviceTimeFifo', 'serviceTimeLifo', 'serviceTimeGreaterIndexFirst', 'serviceTimeLessIndexFirst'})
total.columns = ['time' , 'serviceTimeFifo', 'serviceTimeLifo', 'serviceTimeGreaterIndexFirst', 'serviceTimeLessIndexFirst']
print(total.describe())

plt.plot(total['time'][:tail], total['serviceTimeGreaterIndexFirst'][:tail] ,color="r",marker="^", linewidth=0.5, markersize=3)
plt.plot(total['time'][:tail], total['serviceTimeLessIndexFirst'][:tail] ,color="g",marker="s", linewidth=0.5, markersize=3)
plt.plot(total['time'][:tail], total['serviceTimeLifo'][:tail] ,color="y",marker="x", linewidth=0.5, markersize=3)
plt.plot(total['time'][:tail], total['serviceTimeFifo'][:tail] ,color="b",marker="o", linewidth=0.5, markersize=3)

plt.ylabel('Time')
plt.legend(loc='upper right')
plt.grid(True)
plt.show()

labels = ['mean', 'std', 'min', '25%', '50%', '75%', 'max']
fifoStats = total.describe()['serviceTimeFifo'][1:]
lifoStats = total.describe()['serviceTimeLifo'][1:]
giStats = total.describe()['serviceTimeGreaterIndexFirst'][1:]
liStats = total.describe()['serviceTimeLessIndexFirst'][1:]


x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(x - 2*width, fifoStats, width, label='FIFO')
rects2 = ax.bar(x - width, lifoStats, width, label='LIFO')
rects3 = ax.bar(x, giStats, width, label='GI')
rects4 = ax.bar(x + width, liStats, width, label='LI')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('Service Time per Queue Policy')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()
plt.show()

