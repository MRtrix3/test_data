#!/bin/bash

LOGFILE=testing.log
echo logging to \""$LOGFILE"\" 

mrtrix3_folder=$(dirname $(readlink -f build))
echo MRtrix3 location: $mrtrix3_folder
cat > $LOGFILE <<EOD
-------------------------------------------
  Testing MRtrix3 installation
-------------------------------------------

  testing folder: $(pwd)
  MRtrix3 folder: ${mrtrix3_folder}
EOD

if [ x$1 != 'x-nobuild' ]; then 
  
  echo -n "ensuring MRtrix3 is up to date... "
  cat >> $LOGFILE <<EOD

-------------------------------------------

## building MRtrix3 (from $mrtrix3_folder)

EOD
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
cat >> $LOGFILE <<EOD

-------------------------------------------

## building test commands... 

EOD
./build >> $LOGFILE 2>&1
if [ $? != 0 ]; then 
  echo ERROR!
  exit 1
else
  echo OK
fi

for n in tests/*; do
  script=$(basename $n)
  rm -f data/tmp.*

  cat >> $LOGFILE <<EOD
-------------------------------------------

## running ${script}...

EOD

  echo -n "running ${script}... "
  ( 
    export PATH="$(pwd)/bin:${mrtrix3_folder}/bin:$PATH"; 
    cd data/
    echo PATH is set to $PATH
    set -ex
    source ../tests/$script
  ) > .__tmp.log 2>&1
  error=$?


  cat .__tmp.log >> $LOGFILE
  if [ $error != 0 ]; then 
    echo ERROR! 
    cat >> $LOGFILE <<EOD

## ERROR!

EOD
    exit 1
  else 
    echo OK
    cat >> $LOGFILE <<EOD

## completed OK

EOD

  fi
done


