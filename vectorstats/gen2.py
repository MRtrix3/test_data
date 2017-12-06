#!/usr/bin/env python
# Script for testing element-wise design matrix columns
import os, random, sys
if (not 'N' in os.environ) or (not 'SNR' in os.environ):
  sys.stderr.write('Script requires environment variables \'N\' and \'SNR\' to be set')
  sys.exit(1)
N = int(os.environ['N'])
SNR = int(os.environ['SNR'])
subj_input_files = []
subj_column_files = []
for i in range(0, 2*N): # 2 groups
  path = 'tmpin' + str(i) + '.txt'
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
  subj_input_files.append(path)
  path = 'tmpcolumn' + str(i) + '.txt'
  # Element-wise regressor of no interest
  data = [ random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0) ]
  with open(path, 'w') as f:
    f.write('\n'.join([str(f) for f in data]))
  subj_column_files.append(path)
with open('tmpdesign.csv', 'w') as f:
  for i in range(0,2*N):
    group = '1' if i < N else '0'
    # Group ID, then the element-wise column
    f.write('1,' + group + '\n')
with open('tmpcontrast.csv', 'w') as f:
  # Four contrast rows:
  # - Group difference (effect should be present in data element 1)
  # - Inverse group difference (effect should be present in data element 2)
  # - Positive effect of column-wise EV (should be none)
  # - Negative effect of column-wise EV (should be none)
  f.write('0,1,0\n0,-1,0\n0,0,1\n0,0,-1\n')
with open('tmpsubjects.txt', 'w') as f:
  for path in subj_input_files:
    f.write(path + '\n')
with open('tmpcolumn.txt', 'w') as f:
  for path in subj_column_files:
    f.write(path + '\n')
# Let's create rank-deficient F-tests and make sure they work
with open('tmpftests.txt', 'w') as f:
  f.write('1 1 0 0\n1 1 1 1\n')
