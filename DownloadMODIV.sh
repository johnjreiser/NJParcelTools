#!/bin/sh

names=(Atlantic Bergen Burlington Camden CapeMay Cumberland Essex Gloucester Hudson Hunterdon Mercer Middlesex Monmouth Morris Ocean Passaic Salem Somerset Sussex Union Warren)

for n in "${names[@]}"
do
  echo "${n} County"
  wget "http://www.state.nj.us/treasury/taxation/lpt/MODIV-Counties/2014/${n}14.zip"
  unzip "${n}14.zip"
  if [ "${n}" = "CapeMay" ] 
  then
    convertMODIVtoCSV.py "Cape May14.txt" "${n}.csv" "2014"
  else
	convertMODIVtoCSV.py "${n}14.txt" "${n}.csv" "2014"
  fi
done
