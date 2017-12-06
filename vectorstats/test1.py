#!/usr/bin/env python
import sys
FWE = [ ]
for filepath in [ 'tmpoutfwe_pvalue_0.csv', 'tmpoutfwe_pvalue_1.csv' ]:
  with open(filepath, 'r') as f:
    FWE.append([float(value) for value in f.read().split()])
# Cohort has effect in row 1, not in rows 2-5
# Two contrast rows:
  # - One-sample t-test of effect (effect should be present in data row 1)
  # - Random EV (should be absent)
effects = [ [ 1, 0, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ] ]
for line_FWE, line_effects in zip(FWE, effects):
  for f, e in zip(line_FWE, line_effects):
    if e and f<0.95:
      sys.stderr.write('Error: Simluated effect did not reach significance')
      sys.exit(1)
    if not e and f>0.95:
      sys.stderr.write('Error: Cell with no simulated effect reached significance')
      sys.exit(1)
