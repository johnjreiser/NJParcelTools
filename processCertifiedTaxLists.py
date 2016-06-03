#!/usr/bin/python2.7
# processCertifiedTaxLists.py - State of New Jersey certified tax list processing tool
# 
# modified: 2016-06-02
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
# 20140514 dfahey@alumni.nd.edu Added command line arguments of year to process 
# and destination directory 
#
# usage: ./processCertifiedTaxLists.py [2009-2013] [destination directory] [--outputall]
# example: ./processCertifiedTaxLists.py 2009 OutputFor2009 --outputall
# if no arguments are supplied, the defaults of 2013, ./TMP/ and abbreviated output
# will be assumed
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

counties = ["Atlantic", "Bergen", "Burlington", "Camden", "Cape May", "Cumberland", "Essex", "Gloucester", "Hudson", "Hunterdon", "Mercer", "Middlesex", "Monmouth", "Morris", "Ocean", "Passaic", "Salem", "Somerset", "Sussex", "Union", "Warren"]

## URL pattern is not consistent across years
## for 2013: s/CapeMay/Cape May/
## see below for another 2013 kludge
## will probably rewrite both once I see how they post 2014's lists
baseurl = r"http://www.state.nj.us/treasury/taxation/lpt/MODIV-Counties/{0}/{1}"

if (len(sys.argv) == 1 or sys.argv[1] in ("2013", "2014", "2015", "2016")):
    year = sys.argv[1]
    counties[4] = "CapeMay"
    baseurl = baseurl+year[-2:]+".zip"
elif (sys.argv[1] in ["2009", "2010", "2011", "2012"]):
    year = sys.argv[1]
    baseurl = baseurl+".zip"
else:
    print "invalid argument: input a year between 2009 and 2013"
    exit(0)        
    
source = year
if(len(sys.argv) < 3):
    #default Output directory is CWD/TMP/
    outputdir = os.path.join(os.getcwd(),"TMP/")
else:
    outputdir = sys.argv[2]

if(len(sys.argv) < 4):
    #default output fields
    outputfields = ["pams_pin", "muncode", "block", "lot", "qual", "property_location", 
        "property_class", "building_description", "land_description", "calc_acreage", 
        "additional_lots", "additional_lots2", 
        "owner_name", "owner_address", "owner_city", "owner_zip", 
        "sale_date", "sale_price", "sale_assessment", "assessment_code", 
        "land_value", "improvement_value", "net_value", "net_value_prior_year", 
        "taxes_last_year", "taxes_current_year", "zoning", "year_constructed", 
        "deed_book", "deed_page", "old_property_id"]
elif(sys.argv[3] == "--outputall"):
    outputfields = ["pams_pin", "muncode", "block", "lot", "qual", "transaction_date", 
        "transaction_update_number", "tax_account_number", "property_class", "property_location", 
        "building_description", "land_description", "calc_acreage", "additional_lots", "additional_lots2", 
        "zoning", "tax_map_number", "owner_name", "owner_address", "owner_city", "owner_zip", 
        "number_of_owners", "deduction", "bank_code", "mortgage_account_number", "deed_book", 
        "deed_page", "sales_price_code", "sale_date", "sale_price", "sale_assessment", "sale_sr1a", 
        "rebate_ssn", "rebate_spouse", "rebate_number_dwellings", "rebate_number_commercial", 
        "rebate_multiple_occupancy", "rebate_percent_owned", "rebate_code", "rebate_delinquent", 
        "exempt_own", "exempt_use", "exempt_desc", "exempt_initial_date", "exempt_further_date", 
        "exempt_statute", "exempt_facility", "building_class", "year_constructed", "assessment_code", 
        "land_value", "improvement_value", "net_value", "tax_code_1", "tax_code_2", "tax_code_3", 
        "tax_code_4", "exemption_1_code", "exemption_1_amt", "exemption_2_code", "exemption_2_amt", 
        "exemption_3_code", "exemption_3_amt", "exemption_4_code", "exemption_4_amt", "deduction_senior", 
        "deduction_veteran", "deduction_widow", "deduction_surv_spouse", "deduction_disabled", 
        "user_field_1", "user_field_2", "old_property_id", "census_tract", "census_block", 
        "property_use_code", "property_flags", "tenant_response", "tenant_base_year", 
        "tenant_base_tax", "tenant_base_net_val", "taxes_last_year", "taxes_current_year", 
        "non_municipal_half1", "non_municipal_half2", "municipal_half1", "municipal_half2", 
        "non_municipal_half3", "municipal_half3", "bill_status_flag", "tax_estimated_qtr3", 
        "net_value_prior_year", "statement_aid_amt"]


for county in counties:
# SQL-ready CSV output:
    countyfile = os.path.join(outputdir,county+".csv")
    if(not os.path.exists(outputdir)):
       os.makedirs(outputdir)
# Download ZIP file name
    fn = os.path.join(outputdir, county+"-"+year[-2:]+".zip")
    if(os.path.exists(fn)):
        print county, "ZIP file already downloaded."
    else:
        ## for 2013: s/county/county+year[-2:]/
        url = baseurl.format(year, county) ## baseurl+county+".zip"
        print "downloading", county, "..."
        fn = download(url, fn)
        print county, "downloaded."
# Extract ZIP file
    if(not os.path.exists(countyfile)):
        modivfn = county+year[-2:]+".txt"
        if not (os.path.exists(os.path.join(outputdir,modivfn))): 
            zipf = zipfile.ZipFile(fn, "r")
            names = zipf.namelist()
            if(len(names)==1):
###           print "zipfile:",os.path.join(outputdir,names[0])
                outz = open(os.path.join(outputdir,names[0]), "wb")
                outz.write(zipf.read(names[0]))
                outz.close()
                modivfn = names[0]
            else:
                print "Not sure what to do with these files."
                print "\n".join(names)

        if(os.path.exists(os.path.join(outputdir, modivfn))):
            print "Processing {}".format(modivfn), "..."
            vals = []
            modiv = open(os.path.join(outputdir,modivfn), "r")
            outfile = open(countyfile, "w")
            record = modiv.readline()          
            firstline = True
            while record:
# Process MODIV flat file record            
                parsed = TaxListParser.TaxListParser(record)
                parsed.source = source
                if firstline:
#                    outfile.write( parsed.genCSVheader(outputfields) )
                    outfile.write(",".join(outputfields)+"\n")
                    firstline = False
#                print "Processing", parsed.getPAMSpin()
#                print parsed.genCSVrecord(outputfields)
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
        
