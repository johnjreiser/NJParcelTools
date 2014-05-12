#!/usr/bin/python2.7
# convertMODIVtoCSV.py
# author:  John Reiser <jreiser@njgeo.org>
# purpose: converts a NJ Certified Tax List to CSV for loading into a database
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
# ---------------------------------------------------------------------------
# RELEASE NOTES
# Usage: 
# $ convertMODIVtoCSV.py input.txt output.csv [source_text]
# An input MOD-IV flat file will be processed and exported to CSV. The contents of a 
# source field can be optionally specified to add an additional text column to the output.
# - OR - 
# $ convertMODIVtoCSV.py schema
# Prints PostgreSQL friendly CREATE TABLE query. Can be used as the main table for a 
# partition scheme. Use the "source" above to populate a field that can be used in the 
# partitioned tables. 
#
# This initial public release r01 incorporates several fixes that were required when
# processing historic MOD-IV tables. If you haven't worked with MOD-IV before, be prepared
# for non-conforming data. These tools attempt to handle some of the formatting issues,
# but it is up to the user of these tools to validate the data produced. -reiser

from TaxListParser import TaxListParser
import os, sys, re, datetime, traceback

outputfields = ["pams_pin", "muncode", "block", "lot", "qual", "property_location", 
	"property_class", "building_description", "land_description", "calc_acreage", 
	"additional_lots", "additional_lots2", 
	"owner_name", "owner_address", "owner_city", "owner_zip", 
	"sale_date", "sale_price", "sale_assessment", "assessment_code", 
	"land_value", "improvement_value", "net_value", "net_value_prior_year", 
	"taxes_last_year", "taxes_current_year", "zoning", "year_constructed", 
	"deed_book", "deed_page"]

fi = sys.argv[1]
if fi == "schema":
    print TaxListParser("").genCreateTablePG("table_name", outputfields)
    sys.exit(0)

fo = sys.argv[2]    

source = None
if(len(sys.argv) == 4):
    source = sys.argv[3]
    outputfields.extend(["source"])

with open(fi, "r") as fh:
    firstline = True
    record = fh.readline()
    rc = 1
    with open(fo, "w") as outfile:
        try:
            while record:
                if(source == None):
                    parsed = TaxListParser(record)
                else:
                    parsed = TaxListParser(record, source)                
                if firstline:
                    # outfile.write(",".join(outputfields)+"\n")
                    outfile.write( parsed.genCSVheader(outputfields) )
                    firstline = False
                outfile.write( parsed.genCSVrecord(outputfields) )        
                record = fh.readline()
                rc = rc + 1
        except Exception as e:
            print e
            print traceback.format_exc()
            print rc