#!/usr/bin/env python
import os, random, sys
if (not 'N' in os.environ) or (not 'SNR' in os.environ):
  sys.stderr.write('Script requires environment variables \'N\' and \'SNR\' to be set')
  sys.exit(1)
N = int(os.environ['N'])
SNR = int(os.environ['SNR'])
subj_files = []
for i in range(0, 2*N): # 2 groups
  path = 'tmp' + str(i) + '.txt'
  # 5 data points per subject
  if i < N:
    # First group has effect in element 1, not in elements 2-5
    data = [ random.normalvariate(SNR,1.0),
             random.normalvariate(0.0,1.0),
             random.normalvariate(0.0,1.0),
             random.normalvariate(0.0,1.0),
             random.normalvariate(0.0,1.0) ]
  else:
    # Second group has effect in element 2, not in element 1 or 3-5
    data = [ random.normalvariate(0.0,1.0),
             random.normalvariate(SNR,1.0),
             random.normalvariate(0.0,1.0),
             random.normalvariate(0.0,1.0),
             random.normalvariate(0.0,1.0) ]
  with open(path, 'w') as f:
    f.write('\n'.join([str(f) for f in data]))
  subj_files.append(path)
with open('tmpdesign.csv', 'w') as f:
  for i in range(0,2*N):
    group = '1' if i < N else '0'
    # Group ID, then one random EV
    f.write('1,' + group + ',' + str(random.normalvariate(0.0,1.0)) + '\n')
with open('tmpcontrast.csv', 'w') as f:
  # Three contrast rows:
  # - Group difference (effect should be present in data element 1)
  # - Inverse group difference (effect should be present in data element 2)
  # - Random EV (should be absent)
  f.write('0,1,0\n0,-1,0\n0,0,1\n')
with open('tmpsubjects.txt', 'w') as f:
  for path in subj_files:
    f.write(path + '\n')
# Also perform F-tests:
  # - First contrast only; should have an effect in elements 1 and 2 (since it's unsigned)
  # - First and third contrasts; tests for effect in both group and random EV
with open('tmpftests.csv', 'w') as f:
  f.write('1 0 0\n1 0 1\n')
