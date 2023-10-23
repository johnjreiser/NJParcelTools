#!/usr/bin/env python
# DownloadExtractParcels.py
# author:  John Reiser <jreiser@njgeo.org>
# purpose: Downloads and extracts the available parcel GIS data from NJGIN.
# license: Copyright (C) 2014, John Reiser
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------

#############################################################
# Deprecation Notice
# NJ has moved to providing this data in a Statewide format
# https://njogis-newjersey.opendata.arcgis.com/documents/newjersey::parcels-composite-of-nj-download/about
#############################################################

import urllib.request, urllib.parse, urllib.error, os, sys, zipfile

def download(url,name=""):
    if(name == ""):
        name = url.split('/')[-1]
    webFile = urllib.request.urlopen(url)
    localFile = open(name, 'w')
    fname = localFile.name
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()
    return fname

baseurls = {'parcels': r"http://njgin.state.nj.us/download2/parcels/parcels_mdb_{COUNTY}.zip" }
## to grab NJGIN's copy of MODIV (assessment) data, comment out above and uncomment below.
#baseurls = {'parcels': r"http://njgin.state.nj.us/download2/parcels/parcels_mdb_{COUNTY}.zip", 'taxlist': "http://njgin.state.nj.us/download2/parcels/parcels_taxlist_{COUNTY}.zip"}


counties = ["Atlantic", "Bergen", "Burlington", "Camden", "CapeMay", "Cumberland", "Essex", "Gloucester", "Hudson", "Hunterdon", "Mercer", "Middlesex", "Monmouth", "Morris", "Ocean", "Passaic", "Salem", "Somerset", "Sussex", "Union", "Warren"]
for dt in list(baseurls.keys()):
    for county in counties:
        url = baseurls[dt].replace("{COUNTY}", county)
        fn = url.split('/')[-1]
        if(os.path.exists(fn)):
            print(county, dt, "zip file already downloaded.")
        else:
            fn = download(url)
            print(county, "downloaded.")

        zipf = zipfile.ZipFile(fn, "r")
        names = zipf.namelist()
        if(len(names)==1):
            if(not os.path.exists(dt+names[0])):
                outz = open(dt+names[0], "wb")
                outz.write(zipf.read(names[0]))
                outz.close()
                print(county, dt, "extracted.")
            else:
                print(dt+names[0], "already exists. Skipped.")

