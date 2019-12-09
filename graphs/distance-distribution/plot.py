import matplotlib.pyplot as plt
import numpy as np
import csv

M = 25000
k = 1.6e-9

def fd(d):
    if d >= 0 and d <= M/2:
        return k*2*np.pi*d
    if d > M/2:
        return k*4*d*(np.pi/2 - 2*np.arccos(M/2/d))
    else:
        return 0

d = []
f = []

# compute fd in our interval of interest
d = np.arange(0, (M * 2**0.5 / 2))
for i in d:
    f.append(fd(i))

# compute integral of fd (TODO this is very very very very bad)
integral = []
for i in range(0, len(f)):
    integral.append(np.trapz(f[1:i]))

print(np.trapz(f))

# make plots
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('d [m]')
ax1.set_ylabel('fD(d)')
ax1.plot(d, f, 'c,', label="fD")

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('FD(d)')
ax2.plot(d, integral, 'b,', label="FD")



plt.legend()
plt.show()
#plt.savefig("output.png")
