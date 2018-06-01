#!/bin/bash

set -e

scriptdir=$( dirname "$0" )
echo $scriptdir

names=(Atlantic Bergen Burlington Camden CapeMay Cumberland Essex Gloucester Hudson Hunterdon Mercer Middlesex Monmouth Morris Ocean Passaic Salem Somerset Sussex Union Warren)

if [[ -z "$1" ]] || [[ ${#1} -ne 4 ]] ; then
    echo "USAGE: $0 YYYY"
    echo "Specify the four digit year to download."
    exit 2
else
    year="$1"
    year2=${year:(-2)}
fi

for n in "${names[@]}"
do
  if [[ "${n}" = "CapeMay" ]] && [[ ${year} -eq 2013 ]] ; then
      n="Cape May"
  fi
  echo $n

  if [[ -f "${n}${year2}.zip" ]] ; then
      echo File exists, skipping download...
  else 
      echo "Downloading ${n} County..."
      wget "http://www.state.nj.us/treasury/taxation/lpt/MODIV-Counties/${year}/${n}${year2}.zip"
  fi

  if [[ -f "${n}${year2}.txt" ]] ; then
      echo File exists, skipping extract...
  else 
      unzip "${n}${year2}.zip"
  fi

  if [[ -f "${n}.csv" ]] ; then
      echo File exists, skipping conversion...
  else
      ${scriptdir}/convertMODIVtoCSV.py "${n}${year2}.txt" "${n}.csv" "${year}"
  fi
done
