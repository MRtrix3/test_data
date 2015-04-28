#!/bin/bash

LOGFILE=testing.log
echo logging to \""$LOGFILE"\" 

mrtrix3_folder=$(dirname $(readlink build))
echo MRtrix3 location: $mrtrix3_folder
echo MRtrix3 location: $mrtrix3_folder > $LOGFILE

if [ x$1 != 'x-nobuild' ]; then 
  
  echo -n "ensuring MRtrix3 is up to date... "
  ( 
    cd $mrtrix3_folder
    ./build
  ) >> $LOGFILE 2>&1 
  if [ $? != 0 ]; then 
    echo ERROR!
    exit 1
  else
    echo OK
  fi
  
fi

echo -n "building testing commands... "
./build >> $LOGFILE 2>&1
if [ $? != 0 ]; then 
  echo ERROR!
  exit 1
else
  echo OK
fi

for n in testing/*; do
  if [ -d $n ]; then continue; fi
  script=$(basename $n)
  rm -f testing/data/tmp.*

  cat >> $LOGFILE <<EOD
###########################################
  running ${script}...
###########################################
EOD

  echo -n "running ${script}... "
  ( 
    set -ex
    export PATH="$(pwd)/bin:${mrtrix3_folder}/bin:$PATH"; 
    cd testing/data/
    source ../$script
  ) > .__tmp.log 2>&1
  error=$?


  cat .__tmp.log >> $LOGFILE
  if [ $error != 0 ]; then 
    echo ERROR! 
    cat >> $LOGFILE <<EOD
##########################################
  ERROR!
##########################################
EOD
    exit 1
  else 
    echo OK
    cat >> $LOGFILE <<EOD
##########################################
  completed OK
##########################################
EOD

  fi
done


