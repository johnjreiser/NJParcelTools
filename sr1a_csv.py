#!/usr/bin/python2.7
# sr1a_csv.py, Grantor's Listing (SR1A)
# author: John Reiser <jreiser@njgeo.org>
# parses NJ SR1A output from:
# http://www.state.nj.us/treasury/taxation/lpt/grantors_listing.shtml

import os, re, sys, datetime
import SR1AParser

outputfields = ["pams_pin", "property_location", "u_n_type", "sr_nu_code", "last_update_date",
    "reported_sales_price", "verified_sales_price", "assessed_value_land", "assessed_value_bldg",
    "assessed_value_total", "sales_ratio", "realty_transfer_fee", "serial_number",
    "grantor_name", "grantor_street", "grantor_city_state", "grantor_zip",
    "grantee_name", "grantee_street", "grantee_city_state", "grantee_zip",
    "deed_book", "deed_page", "deed_date", "date_recorded", "qualification_codes",
    "property_class", "class_4_type", "year_built", "living_space", "condo" ]

outputfields = None

fn = sys.argv[1]
if(len(sys.argv) == 3 and sys.argv[2] == 'old'):
    p = SR1AParser.SR1AParser
else:
    p = SR1AParser.SR1AParser2013

if fn == "schema":
    print p("").genCreateTablePG("SR1A", outputfields)
else:
    if not outputfields == None:
        print ",".join(outputfields)
    else:
        print ",".join(p("").fields)
    if(os.path.exists(fn)):
        with open(fn, "r") as sr1a:
            line = sr1a.readline().rstrip("\n")
            while line:
                parsed = p(line)
                print parsed.genCSVrecord( outputfields ),
                line = sr1a.readline()
    else:
        raise FileNotFound("Specified file does not exist.")
