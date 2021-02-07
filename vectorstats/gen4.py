#!/usr/bin/python3
# Script for testing per-element design matrix row exclusion based on presence of NaNs in input data
import os, random, sys
if not 'N' in os.environ or not 'SNR' in os.environ:
  sys.stderr.write('Script requires environment variables "N" and "SNR" to be set')
  sys.exit(1)
N = int(os.environ['N'])
SNR = float(os.environ['SNR'])
subj_files = []
for i in range(0,N):
  path = 'tmp' + str(i) + '.txt'
  # 5 data points per subject
  # Positive effect in element 1
  data = [ random.normalvariate(SNR,1.0),
           random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0),
           random.normalvariate(0.0,1.0) ]
  # Make data for this subject NaN in one out of the five elements
  data[random.randint(0,4)] = float('nan')
  with open(path, 'w') as f:
    f.write('\n'.join([str(f) for f in data]))
  subj_files.append(path)
with open('tmpdesign.csv', 'w') as f:
  for i in range(0,N):
    # Cohort mean, no nuisance variables
    f.write('1\n')
with open('tmpcontrast.csv', 'w') as f:
  # One contrast row:
  # - Positive one-sample t-test
  f.write('1\n')
with open('tmpsubjects.txt', 'w') as f:
  for path in subj_files:
    f.write(path + '\n')
