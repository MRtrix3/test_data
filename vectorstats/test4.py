#!/usr/bin/env python
import sys
with open('tmpoutfwe_1mpvalue.csv', 'r') as f:
  for line in f.read().splitlines():
    line = line.split('#')[0]
    if line:
      FWE = [float(value) for value in line.split()]
      break
# Cohort has positive effect in element 1
effect = [ 1, 0, 0, 0, 0 ]
for f, e in zip(FWE, effect):
  if e and f<0.95:
    sys.stderr.write('Error: Simluated effect did not reach significance')
    sys.exit(1)
  if not e and f>0.95:
    sys.stderr.write('Error: Cell with no simulated effect reached significance')
    sys.exit(1)
