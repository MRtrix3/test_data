#!/usr/bin/python3
import sys
FWE = [ ]
for filepath in [ 'tmpoutfwe_1mpvalue_t1.csv', 'tmpoutfwe_1mpvalue_t2.csv', 'tmpoutfwe_1mpvalue_t3.csv', 'tmpoutfwe_1mpvalue_F1.csv', 'tmpoutfwe_1mpvalue_F2.csv' ]:
  with open(filepath, 'r') as f:
    for line in f.read().splitlines():
      line = line.split('#')[0]
      if line:
        FWE.append([float(value) for value in line.split(',')])
# First group has effect in row 1, not in rows 2-5
# Second group has effect in row 2, not in rows 1 or 3-5
# Four outputs:
  # - Group difference (effect should be present in data element 1)
  # - Inverse group difference (effect should be present in data element 2)
  # - Random EV (should be absent)
  # - F-test containing rows 1 and 2 (effect should be present in data elements 1 and 2)
effects = [ [ 1, 0, 0, 0, 0 ],
            [ 0, 1, 0, 0, 0 ],
            [ 0, 0, 0, 0, 0 ],
            [ 1, 1, 0, 0, 0 ],
            [ 1, 1, 0, 0, 0 ] ]
for line_FWE, line_effects in zip(FWE, effects):
  for f, e in zip(line_FWE, line_effects):
    if e and f<0.95:
      sys.stderr.write('Error: Simluated effect did not reach significance')
      sys.exit(1)
    if not e and f>0.95:
      sys.stderr.write('Error: Cell with no simulated effect reached significance')
      sys.exit(1)
