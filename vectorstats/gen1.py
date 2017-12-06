#!/usr/bin/env python
import os, random, sys;
if not 'N' in os.environ or not 'SNR' in os.environ:
  sys.stderr.write('Script requires environment variables "N" and "SNR" to be set')
  sys.exit(1)
N = int(os.environ['N'])
SNR = int(os.environ['SNR'])
subj_files = []
for i in range(0,N):
  path = 'tmp' + str(i) + '.txt'
  # 5 data points per subject
  # Effect in row 1, not in rows 2-5
  data = [ random.normalvariate(SNR,1.0),
           random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0) ]
  with open(path, 'w') as f:
    f.write('\n'.join([str(f) for f in data]))
  subj_files.append(path)
with open('tmpdesign.csv', 'w') as f:
  for i in range(0,N):
    # Cohort mean, one random EV
    f.write('1,' + str(random.normalvariate(0.0,1.0)) + '\n')
with open('tmpcontrast.csv', 'w') as f:
  # Two contrast rows:
  # - One-sample t-test of effect
  # - Random EV (should be absent)
  f.write('1,0\n0,1\n')
with open('tmpsubjects.txt', 'w') as f:
  for path in subj_files:
    f.write(path + '\n')
