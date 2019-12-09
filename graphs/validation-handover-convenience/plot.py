# TODO ok it always shows positive values only
# but is this complaint with what Amedeo found? He told me that sometimes there are some negatives, while I never have them
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse
import csv
import re

parser = argparse.ArgumentParser(description='Validate Handover Convenience')
parser.add_argument('N', type=int, help='number of aircrafts')

args = parser.parse_args()
n = args.N
#negativeValues = False
#differences = pd.Series([])

sBefore = []
sAfter = []

negative = 0
positive = 0

for i in range(0, n):
  with open('../../src/simulations/results/General-#' + str(i) + '.vec') as file:
    reader = csv.reader(file, delimiter='\t')

    vn_before = -1
    vn_after = -1

    # search for vector number in file
    while True:
      line = file.readline()
      if (re.match('^vector.*serviceTimeBeforeHandover', line)):
        vn_before = int(line.split()[1])
      if (re.match('^vector.*serviceTimeAfterHandover', line)):
        vn_after = int(line.split()[1])
      if (vn_after != -1 and vn_before != -1):
        break

    for row in reader:
      if (len(row) != 4): # skip header
        continue

      if (int(row[0]) == vn_before):  # serviceTimeBeforeHandover
        sBefore.append(float(row[3]))
      if (int(row[0]) == vn_after):  # serviceTimeAfterHandover
        sAfter.append(float(row[3]))

    # print(len(sAfter), len(sBefore))
    assert len(sAfter) == len(sBefore)

    for i in range(0, len(sBefore)):
      difference = sBefore[i] - sAfter[i]
      if (difference < 0):
        negative += 1
      else:
        positive += 1

print('negative: ', negative)
print('positive: ', positive)
