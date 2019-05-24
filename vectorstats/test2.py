#!/usr/bin/env python
# Script for testing element-wise design matrix columns
import sys
FWE = [ ]
for filepath in [ 'tmpoutfwe_1mpvalue_t1.csv', 'tmpoutfwe_1mpvalue_t2.csv', 'tmpoutfwe_1mpvalue_t3.csv', 'tmpoutfwe_1mpvalue_t4.csv' ]:
  with open(filepath, 'r') as f:
    FWE.append([float(value) for value in f.read().split()])
# Cohort has positive effect (first contrast) in element 1, negative effect (second contrast) in element 2
effects = [ [ 1, 0, 0, 0, 0 ],
            [ 0, 1, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ] ]
for line_FWE, line_effects in zip(FWE, effects):
  for f, e in zip(line_FWE, line_effects):
    if e and f<0.95:
      sys.stderr.write('Error: Simluated effect did not reach significance')
      sys.exit(1)
    if not e and f>0.95:
      sys.stderr.write('Error: Cell with no simulated effect reached significance')
      sys.exit(1)
