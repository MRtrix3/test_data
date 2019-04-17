#!/usr/bin/env python
import sys
with open('tmpoutfwe_pvalue.csv', 'r') as f:
  FWE = [float(value) for value in f.read().split()]
# Cohort has positive effect in element 1
effect = [ 1, 0, 0, 0, 0 ]
for f, e in zip(FWE, effect):
  if e and f<0.95:
    sys.stderr.write('Error: Simluated effect did not reach significance')
    sys.exit(1)
  if not e and f>0.95:
    sys.stderr.write('Error: Cell with no simulated effect reached significance')
    sys.exit(1)
