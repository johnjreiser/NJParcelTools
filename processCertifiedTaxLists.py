#!/usr/bin/python2.7
# processCertifiedTaxLists.py - State of New Jersey certified tax list processing tool
# 
# modified: 2013-06-03
# author:   John Reiser <jreiser@njgeo.org>
# purpose:  parses NJ MOD IV certified task lists from:
#           http://www.state.nj.us/treasury/taxation/lpt/TaxListSearchPublicWebpage.shtml
# license:  Copyright (C) 2014, John Reiser
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

import TaxListParser
import zipfile, urllib, os, re, sys, datetime #, MySQLdb, time

def download(url,name=""):
    if(name == ""):
        name = url.split('/')[-1]
    webFile = urllib.urlopen(url)
    localFile = open(name, 'w')
    fname = localFile.name
    localFile.write(webFile.read())
    webFile.close()
    localFile.close()
    return fname

year = "2013"
source = "CertifiedList"+year
baseurl = r"http://www.state.nj.us/treasury/taxation/lpt/MODIV-Counties/{0}/{1}"+year[-2:]+".zip"
counties = ["Atlantic", "Bergen", "Burlington", "Camden", "Cape May", "Cumberland", "Essex", "Gloucester", "Hudson", "Hunterdon", "Mercer", "Middlesex", "Monmouth", "Morris", "Ocean", "Passaic", "Salem", "Somerset", "Sussex", "Union", "Warren"]
## URL pattern is not consistent across years
## for 2013: s/CapeMay/Cape May/
## see below for another 2013 kludge
## will probably rewrite both once I see how they post 2014's lists
## dfahey - 2013 URL did not work, maybe NJ moved the files

for county in counties:
# SQL-ready CSV output:
    countyfile = os.path.join(os.getcwd(),county+".csv")
# Downloaded ZIP file name
    fn = os.path.join(os.getcwd(), county+"-"+year+".zip")
    if(os.path.exists(fn)):
        print county, "zip file already downloaded."
    else:
        ## for 2013: s/county/county+year[-2:]/
        url = baseurl.format(year, county) ## baseurl+county+".zip"
        fn = download(url, fn)
        print county, "downloaded."
    if(not os.path.exists(countyfile)):
        zipf = zipfile.ZipFile(fn, "r")
        names = zipf.namelist()
        modivfn = county+year[-2:]+".txt"
        if(len(names)==1):
            outz = open(names[0], "wb")
            outz.write(zipf.read(names[0]))
            outz.close()
            modivfn = names[0]
        else:
            print "Not sure what to do with these files."
            print "\n".join(names)
        if(os.path.exists(os.path.join(os.getcwd(), modivfn))):
            print "Processing {}".format(modivfn)
            vals = []
            modiv = open(os.path.join(os.getcwd(),modivfn), "r")
            outfile = open(countyfile, "w")
            record = modiv.readline()
            outputfields = ["pams_pin", "muncode", "block", "lot", "qual", "property-location", 
                "property-class", "building-description", "land-description", "calc-acreage", 
                "additional-lots", "additional-lots2", 
                "owner-name", "owner-address", "owner-city", "owner-zip", 
                "sale-date", "sale-price", "sale-assessment", "assessment-code", 
                "land-value", "improvement-value", "net-value", "net-value-prior-year", 
                "taxes-last-year", "taxes-current-year", "zoning", "year-constructed", 
                "deed-book", "deed-page"]
            firstline = True
            while record:
# dfahey - when I run the code, I get and error: TypeError: 'module' object is not callable                
                parsed = TaxListParser.TaxListParser(record)
                parsed.source = source
                if firstline:
#                    outfile.write( parsed.genCSVheader(outputfields) )
                    outfile.write(",".join(outputfields)+"\n")
                    firstline = False
#                print "Processing", parsed.getPAMSpin()
                outfile.write( parsed.genCSVrecord(outputfields) )
### # code below was to generate Insert statements for MySQL
#                break
#            if(skipping == 1):
#                if(parsed.getPAMSpin() == skipuntil):
#                    skipping = 0
#                else:
#                    print "Skipping", parsed.getPAMSpin()
#            if(skipping == 0):
#                print "Loading", parsed.getPAMSpin()
#                try:
###                    sql = parsed.genInsertMySQL("taxlist", source)
#                    vals.append(parsed.getAllFieldsTuple())
#                except:
#                    print parsed.record
#                    raise
#                try:
#                    if(len(vals) == 50):
#                        cursor.executemany(parsed.genExecuteManyInsert("taxlist"), vals)
#                        vals = []
###                        time.sleep(60)
###                        sys.exit(0)
###                    cursor.execute(sql)
#                    # should probably refactor code to take advantage of executemany using the string formatting method
#                    # see: http://mysql-python.sourceforge.net/MySQLdb.html
#                except:
#                    print parsed.record
#                    print vals
#                    raise
                record = modiv.readline()
            outfile.close()
            print "{} complete.".format(county)
        else:
            print "MODIV flat file not found for {}".format(county)
        
