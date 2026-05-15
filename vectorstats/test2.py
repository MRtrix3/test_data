#!/usr/bin/python3
# Script for testing element-wise design matrix columns
import pathlib
import sys
FWE = [ ]
for filename in [ 'fwe_1mpvalue_t1.csv', 'fwe_1mpvalue_t2.csv', 'fwe_1mpvalue_t3.csv', 'fwe_1mpvalue_t4.csv' ]:
  with open(pathlib.Path(sys.argv[1], filename), 'r') as f:
    for line in f.read().splitlines():
      line = line.split('#')[0]
      if line:
        FWE.append([float(value) for value in line.split(',')])
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
