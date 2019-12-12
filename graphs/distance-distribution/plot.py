import matplotlib.pyplot as plt
import numpy as np
import csv

M = 25000
k = 1.6e-9
T = 0.00000000425603

### Distribution of Distance
# PDF of distance
def fd(d):
    if d >= 0 and d <= M/2:
        return k*2*np.pi*d
    elif d > M/2:
        return k*4*d*(np.pi/2 - 2*np.arccos(M/2/d))
    else:
        return 0

d = []
f = []

# compute fd in our interval of interest
d = np.arange(0, (M * 2**0.5 / 2))
for i in d:
    f.append(fd(i))

# compute integral of fd
integral = []
last = 0
for i in range(0, len(f)):
    part = f[i]
    last = last + part
    integral.append(last)

print("normalization fd: ", np.trapz(f))

# make plots
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('d [m]')
ax1.set_ylabel('fD(d)')
ax1.plot(d, f, 'c,', label='fD')

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('FD(d)')
ax2.plot(d, integral, 'b,', label="FD")

plt.legend()
plt.show()

def fs(s):
    if s >= 0 and s <= (T * M**2 ) / 4:
        return np.pi / ( T * M**2 )
    elif s >= (T * M**2 ) / 4 and s <= (T * M**2) / 2:
        return (np.pi / (T * M**2)) - (4 / (T * M**2)) * np.arccos(M/2 * ((T / s)**0.5))
    else:
        return 0

### Distribution of Service Time
s = T * d**2
f = []
for i in s:
    f.append(fs(i))

print("normalization fs: ", np.trapz(f, s))

# compute integral of fs
integral = [ 0 ]
last = 0
for i in range(1, len(f)):
    part = f[i] * (s[i] - s[i - 1])
    last = last + part
    integral.append(last)

# make plots
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('s [s]')
ax1.set_ylabel('fS(s)')
ax1.plot(s, f, 'c,', label='fS')

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('FD(d)')
ax2.plot(s, integral, 'b,', label='FS')

plt.legend()
plt.show()
