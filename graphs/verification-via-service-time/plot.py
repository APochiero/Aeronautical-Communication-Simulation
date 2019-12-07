import matplotlib.pyplot as plt
import numpy as np
import csv

xv = []
yv = []

with open('../../src/simulations/results/General-#0.vec') as file:
    reader = csv.reader(file, delimiter="\t")

    for row in reader:
        if (len(row) != 4):   # skip headers
            continue

        if (int(row[0]) == 2):   # which vector am I interested in?
            x = float(row[2])
            y = float(row[3])
            if (x > 18920 and x < 19160):   # X range
                xv.append(x)
                yv.append(y)

plt.plot(xv, yv, ',', label="service time")
plt.xlabel('[s]')
plt.ylabel('[s]')

plt.title("Verification via Service Time")

plt.legend()

plt.show()
#plt.savefig("output.png")
