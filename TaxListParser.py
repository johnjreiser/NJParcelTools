#!/usr/bin/env python
# TaxListParser.py - State of New Jersey certified tax list parser
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


import re, datetime

class TaxListParser:
    """convert a fixed-width string from MOD-IV to a dict"""
    def __init__(self,record):
        self.record = record
        self.source = ''
        self.numCheck = re.compile(r'[^\d.]+')
        """tags is a dict of tuples, with [0] as start, [1] as length, [2] as type ["string","int","date", "float"], [3] as float format"""
        self.tags = {"muncode": (0,4,0),
                "block": (4,9,0),
                "lot": (13,9,0),
                "qual": (22,11,0),
                "transaction_date": (37,6,2),
                "transaction_update_number": (43,4,1),
                "tax_account_number": (47,8,0),
                "property_class": (55,3,0),
                "property_location": (58,25,0),
                "building_description": (83,15,0),
                "land_description": (98,20,0),
                "calc_acreage": (118,9,3,"5.4"), # formatted as 12345(.)6789
                "additional_lots": (127,20,0),
                "additional_lots2":(147,20,0),
                "zoning": (167,4,0),
                "tax_map_number": (171,4,0),
                "owner_name": (175,35,0),
                "owner_address": (210,25,0),
                "owner_city": (235,25,0),
                "owner_zip": (260,9,0),
                "number_of_owners": (269,4,1),
                "deduction": (273,6,1),
                "bank_code": (280,5,0),
                "mortgage_account_number": (285,10,0),
                "deed_book": (295,5,0),
                "deed_page": (300,5,0),
                "sales_price_code": (305,1,0),
                "sale_date": (306,6,2),
                "sale_price":(312,9,1),
                "sale_assessment":(321,9,1),
                "sale_sr1a":(330,2,0),
                "rebate_ssn":(332,9,0),
                "rebate_spouse":(341,9,0),
                "rebate_number_dwellings":(350,2,0),
                "rebate_number_commercial":(352,2,0),
                "rebate_multiple_occupancy":(354,1,0),
                "rebate_percent_owned": (355,1,0),
                "rebate_code": (356,2,0),
                "rebate_delinquent": (358,1,0),
                "exempt_own": (359,2,0),
                "exempt_use": (361,2,0),
                "exempt_desc":(363,3,0),
                "exempt_initial_date":(366,6,2),
                "exempt_further_date":(372,6,2),
                "exempt_statute": (378,12,0),
                "exempt_facility":(390,20,0),
                "building_class":(410,5,0),
                "year_constructed":(415,4,0),
                "assessment_code":(419,1,0,1),
                "land_value":(420,9,1),
                "improvement_value": (429,9,1),
                "net_value":(438,9,1),
                "tax_code_1": (447,3,0),
                "tax_code_2": (450,3,0),
                "tax_code_3": (453,3,0),
                "tax_code_4": (456,3,0),
                "exemption_1_code":(459,1,0),
                "exemption_1_amt": (460,8,1),
                "exemption_2_code":(468,1,0),
                "exemption_2_amt": (469,8,1),
                "exemption_3_code":(477,1,0),
                "exemption_3_amt": (478,8,1),
                "exemption_4_code":(486,1,0),
                "exemption_4_amt": (487,8,1),
                "deduction_senior":(495,4,1),
                "deduction_veteran":(499,4,1),
                "deduction_widow":(503,4,1),
                "deduction_surv_spouse":(507,3,1),
                "deduction_disabled":(510,3,1),
                "user_field_1":(513,4,0),
                "user_field_2":(517,4,0),
                "old_property_id":(521,29,0),
                "census_tract":(550,5,0),
                "census_block":(555,4,0),
                "property_use_code":(559,3,0),
                "property_flags":(562,10,0),
                "tenant_response":(572,1,0),
                "tenant_base_year":(573,4,0),
                "tenant_base_tax":(577,9,3,"7.2"),
                "tenant_base_net_val":(586,9,1),
                "taxes_last_year":(600,9,3,"7.2"),
                "taxes_current_year":(609,9,3,"7.2"),
                "non_municipal_half1":(618,9,3,"7.2"),
                "non_municipal_half2":(627,9,3,"7.2"),
                "municipal_half1":(636,9,3,"7.2"),
                "municipal_half2":(645,9,3,"7.2"),
                "non_municipal_half3":(654,9,3,"7.2"),
                "municipal_half3":(663,9,3,"7.2"),
                "bill_status_flag":(672,1,0),
                "tax_estimated_qtr3":(673,9,3,"7.2"),
                "net_value_prior_year":(682,9,1),
                "statement_aid_amt":(691,9,3,"7.2")
                }
        self.fields = ['pams_pin', 'source']
        self.fields.extend(sorted(self.tags.keys()))
        if(len(self.record) != 701):
            self.record += ("0"*(701-len(self.record)))
        
    def getField(self,field):
        if field in self.tags:
            stri = self.tags[field][0]
            endi = self.tags[field][1]+self.tags[field][0]
            value = self.record[stri:endi].strip()
            if(field == "block" or field == "lot"):
                zeroStrip = re.compile(r'^[0]*(\w+$)') # this is a kludge and should probably be rewritten to match two groups of out the "00000SS00" format for decimalized blocks and lots
                if(len(value) == 5):
                    return zeroStrip.sub(r'\1', value)
                #    return str(int(value)) # drop padded zeroes
                else:
                    part = []
                    part.append(zeroStrip.sub(r"\1",value[:5]))
                    zeroStrip = re.compile(r'^[\s]*(\w+$)') # change the regex for the lot to only look for spaces.
                    part.append(zeroStrip.sub(r"\1",value[-4:]))
                    return ".".join(part)
                #    return str(int(value[:5]))+"."+value[-4:].strip() # return formatted decimal block/lot
            elif(self.tags[field][2] == 1):
                if(value != ''):
                    return int(value)
                else:
                    return ''
            elif(self.tags[field][2] == 2):
                value = self.numCheck.sub('', value)
                ds = '0000-00-00'
                if(len(value) == 6):
                    if(value == '000000' or value == '      '):
                        return '0000-00-00'
                    else:
                        if(int(value[-2:]) > 13):
                            ds = "19%s-%s-%s" % (value[-2:],value[:2],value[2:4])
                        else:
                            ds = "20%s-%s-%s" % (value[-2:],value[:2],value[2:4])
                else:                
                    return "0000-00-00"
#                return ds
                return self.dateTest(ds)
            elif(self.tags[field][2] == 3):
                if(value == ''):
                    return 0
                else:
                    try:
                        brk = self.tags[field][3].split(".")
                        value = value[:int(brk[0])] + "." + value[-1*int(brk[1]):]
                        value = self.numCheck.sub("",value)
                        if(len(value) == 1):
                            return 0
                        else:
                            return float(value)
                    except:
                        print "record length:",len(self.record)
                        print "value:",value
                        print "break:",brk
                        raise
            else:
                return value.replace("\\", r"\\").replace("'","\\'")
        elif(field == 'pams_pin'):
            return self.getPAMSpin()
        elif(field == 'source'):
            return self.source
        else: 
            return "invalid record"
            raise

    def getPAMSpin(self):
        try:
            mun = self.getField("muncode")
            block = self.getField("block")
            lot = self.getField("lot")
            qual = self.getField("qual")
            if(qual == ''):
                return "_".join([mun, block, lot])
            else:
                return "_".join([mun, block, lot, qual])
        except:
            print self.record
            raise

    def genCreateTableMySQL(self, tablename):
        text = "CREATE TABLE `" + tablename + "` ( `recordid` INT NOT NULL UNSIGNED AUTO_INCREMENT, \n" + \
               "`pams_pin` VARCHAR(30),\n" + \
               "`source` VARCHAR(20),\n" + \
               "`timeinserted` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \n"
        for key in sorted(self.tags.iteritems()):
            if(key[1][2] == 0):
                text += "`%s` VARCHAR(%s),\n" % (key[0],str(key[1][1]))
            elif(key[1][2] == 1):
                text += "`%s` INT,\n" % (key[0])
            elif(key[1][2] == 2):
                text += "`%s` DATE,\n" % (key[0])
            elif(key[1][2] == 3):
                precision = key[1][3].split(".")
                precision[0] = str(int(precision[0]) + int(precision[1]))
                text += "`%s` DECIMAL(%s),\n" % (key[0], ",".join(precision))
        text = text + "PRIMARY KEY (`recordid`));"
        return text

    def genInsertMySQL(self, table, source):
        self.source = source
        pams = self.getPAMSpin()
        text = "INSERT INTO %s SET `pams_pin` = '%s', `source` = '%s', " % (table, pams, source)
        for key in sorted(self.tags.iteritems()):
            if(key[1][2] == 1 or key[1][2] == 2):
                text += "`%s` = %s, " % (key[0], self.getField(key[0]))
            else:
                text += """`%s` = '%s', """ % (key[0], self.getField(key[0]))
        text = text[:-2]
        text += ";\n"
        return text

    def genCSVheader(self, df): # df: desired fields
        fields = ["pams_pin"]
        for key in sorted(self.tags.iteritems()):
            if(key[0] in df):
                fields.append( key[0] )
        return ",".join( fields ) + "\n"

    def genCSVrecord(self, fields):
        pams = self.getPAMSpin()
        values = ['"{0}"'.format(pams)]        
        for f in fields:
            if f in self.tags.keys():
                if(self.tags[f][2] == 0):
                    values.append( '"{0}"'.format( str(self.getField(f)).replace('"', "'") ) )
                elif(self.tags[f][2] == 2):
                    if(self.getField(f) == "0000-00-00"):
                        values.append( '' )
                    else: 
                        values.append( '"{0}"'.format( str(self.getField(f))) )
                else:
                    if self.getField(f) == None:
                        values.append( '' )
                    else:
                        values.append( str( self.getField(f) ).replace('"', "'") )
        return ",".join(values) + "\n"
        
        #### old alphanumerically sorted output below
    def genCSVrecordAlpha(self, fields):
        pams = self.getPAMSpin()
        values = ['"{0}"'.format(pams)]
        for key in sorted(self.tags.iteritems()):
            if(key[0] in fields):
                if(key[1][2] == 0):
                    values.append( '"{0}"'.format( str(self.getField(key[0])) ) )
                elif(key[1][2] == 2):
                    if(self.getField(key[0]) == "0000-00-00"):
                        values.append( '' )
                    else: 
                        values.append( '"{0}"'.format( str(self.getField(key[0])) ) )
                else:
    #                print key[0]+":"+str(self.getField(key[0]))+" - "+str(type(self.getField(key[0])))
                    if self.getField(key[0]) == None:
                        values.append( '' )
                    else:
                        values.append( str( self.getField(key[0]) ) )
        return ",".join(values) + "\n"

    def genCreateTablePG(self, tablename, fields=None):
        text = "CREATE TABLE " + tablename + " (recordid serial primary key, \n" + \
            "pams_pin varchar(30), \n" + \
            "source varchar(20), \n"
        #### if fields parameter is not passed, all possible fields will be returned in alphabetical order
        if(fields != None):
            keysource = []
            for f in fields:
                if f in self.tags.keys():
                    keysource.append( [f, self.tags[f]] )
        else:
            keysource = sorted(self.tags.iteritems())
        for key in keysource:
            if(key[1][2] == 0):
                text += "%s VARCHAR(%s),\n" % (key[0].replace("-","_"),str(key[1][1]))
            elif(key[1][2] == 1):
                text += "%s INT,\n" % (key[0].replace("-","_"))
            elif(key[1][2] == 2):
                text += "%s DATE,\n" % (key[0].replace("-","_"))
            elif(key[1][2] == 3):
                precision = key[1][3].split(".")
                precision[0] = str(int(precision[0]) + int(precision[1]))
                text += "%s DECIMAL(%s),\n" % (key[0].replace("-","_"), ",".join(precision))
        text = text + "timeinserted timestamp default 'now' );"
        return text

    def getAllFields(self):
        fs = {}
        for key in self.fields:
            fs[key] = self.getField(key)
        return fs

    def getAllFieldsTuple(self):
        fs = []
        for key in self.fields:
            fs.append(self.getField(key))
        return fs

    def genExecuteManyInsert(self, tablename):
        sql = r"INSERT INTO " + tablename + " ("
        sql += ", ".join(map(lambda x: "`%s`"%x,self.fields)) # map/lambda to wrap keys in MySQL field delimiters
        sql += ") VALUES (" + (r" %s,"*len(self.fields))[:-1]
        sql += ")"
        return sql

    def dateTest(self, datestr):
        dateOk = False
        format = '%Y-%m-%d'
        try:
            result = datetime.datetime.strptime(datestr, format)
            dateOk = (datestr == result.strftime(format)) # this makes sure the parsed date matches the original string
        except:
#            print "Date did not match: {0}".format(datestr)
            pass
        if dateOk:
            return datestr
        else:
            return '0000-00-00'
