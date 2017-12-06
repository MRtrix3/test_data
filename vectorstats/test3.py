#!/usr/bin/env python
import sys
FWE = [ ]
for filepath in [ 'tmpoutfwe_pvalue_c1.csv', 'tmpoutfwe_pvalue_c2.csv' ]:
  with open(filepath, 'r') as f:
    FWE.append([float(value) for value in f.read().split()])
# Cohort has positive effect in element 1, negative effect in element 2
# Two contrast rows:
  # - Positive One-sample t-test (effect should be present in data element 1)
  # - Negative One-sample t-test (effect should be present in data element 2)
effects = [ [ 1, 0, 0, 0, 0 ],
            [ 0, 1, 0, 0, 0 ] ]
for line_FWE, line_effects in zip(FWE, effects):
  for f, e in zip(line_FWE, line_effects):
    if e and f<0.95:
      sys.stderr.write('Error: Simluated effect did not reach significance')
      sys.exit(1)
    if not e and f>0.95:
      sys.stderr.write('Error: Cell with no simulated effect reached significance')
      sys.exit(1)
