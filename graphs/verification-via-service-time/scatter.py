import matplotlib.pyplot as plt
import numpy as np
import csv

xv = []
yv = []
count = 0

with open('input.csv') as file:
    reader = csv.reader(file, delimiter="\t")
    for row in reader:
        x = float(row[2])
        y = float(row[3])
        if (x > 18920 and x < 19160):   # X range
            xv.append(x)
            yv.append(y)

plt.plot(xv, yv, ',', label="service time")
#plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d s'))
#plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%d s'))
plt.xlabel('[s]')
plt.ylabel('[s]')

plt.title("Verification via Service Time")

plt.legend()

plt.show()
#plt.savefig("output.png")
