#!/usr/bin/env python
# SR1AParser - State of New Jersey Grantor's Listing (SR1A) parser
# parses the SR1A files from:
# http://www.state.nj.us/treasury/taxation/lpt/grantors_listing.shtml
# author: John Reiser <jreiser@njgeo.org>
# last modified: 2015-11-24
# license: GPLv3

import re
from datetime import datetime

class SR1AParser:
    """convert a fixed-width string from the SR1A output to a dict"""
    def __init__(self,record):
        self.record = record
        self.source = ''
        self.numCheck = re.compile(r'[^\d.]+')
        """tags is a dict of tuples, with [0] as start, [1] as length, [2] as type ["string","int","date", "float"], [3] as float format"""
        self.tags = {"county_code": [0, 2, 1],
                "district_code": [2, 2, 1],
                "batch_number": [4, 5, 1],
                "dln": [9, 7, 1],
                "operator_initials": [16, 3, 0],
                "last_update_date": [19, 6, 2, 'YYMMDD'],
                "questionnaire_status_code": [25, 1, 0],
                "questionnaire_date": [26, 6, 2, 'YYMMDD'],
                "questionnaire_who_code": [32, 1, 0],
                "u_n_type": [33, 1, 0],
                "sr_nu_code": [34, 3, 0],
                "reported_sales_price": [37, 9, 1],
                "verified_sales_price": [46, 9, 1],
                "assessed_value_land": [55, 9, 1],
                "assessed_value_bldg": [64, 9, 1],
                "assessed_value_total": [73, 9, 1],
                "sales_ratio": [82, 5, 3, '3.2'],
                "realty_transfer_fee": [87, 9, 3, '7.2'],
                "rtf_error_flag": [96, 1, 0],
                "rtf_exempt_code": [97, 1, 0],
                "serial_number": [98, 7, 1],
                "grantor_nctl": [105, 4, 0],
                "grantor_name": [109, 35, 0],
                "grantor_street": [144, 25, 0],
                "grantor_city_state": [169, 25, 0],
                "grantor_zip": [194, 9, 0],
                "grantee_name": [203, 35, 0],
                "grantee_street": [238, 25, 0],
                "grantee_city_state": [263, 25, 0],
                "grantee_zip": [288, 9, 0],
                "property_location": [297, 25, 0],
                "aging_date": [322, 6, 2, 'YYMMDD'],
                "deed_book": [328, 5, 0],
                "deed_page": [333, 5, 0],
                "deed_date": [338, 6, 2, 'YYMMDD'],
                "date_recorded": [344, 6, 2, 'YYMMDD'],
                "block_prefix": [350, 5, 0],
                "block_suffix": [355, 4, 0],
                "lot_prefix": [359, 5, 0],
                "lot_suffix": [364, 4, 0],
                "etc": [368, 1, 0],
                "addl_block1": [369, 9, 0],
                "addl_lot1": [378, 9, 0],
                "addl_qualifier1": [387, 5, 0],
                "addl_value_land1": [392, 9, 1],
                "addl_value_bldg1": [401, 9, 1],
                "addl_value_total1": [410, 9, 1],
                "addl_block2": [419, 9, 0],
                "addl_lot2": [428, 9, 0],
                "addl_qualifier2": [437, 5, 0],
                "addl_value_land2": [442, 9, 1],
                "addl_value_bldg2": [451, 9, 1],
                "addl_value_total2": [460, 9, 1],
                "addl_block3": [469, 9, 0],
                "addl_lot3": [478, 9, 0],
                "addl_qualifier3": [487, 5, 0],
                "addl_value_land3": [492, 9, 1],
                "addl_value_bldg3": [501, 9, 1],
                "addl_value_total3": [510, 9, 1],
                "addl_block4": [519, 9, 0],
                "addl_lot4": [528, 9, 0],
                "addl_qualifier4": [537, 5, 0],
                "addl_value_land4": [542, 9, 1],
                "addl_value_bldg4": [551, 9, 1],
                "addl_value_total4": [560, 9, 1],
                "addl_block5": [569, 9, 0],
                "addl_lot5": [578, 9, 0],
                "addl_qualifier5": [587, 5, 0],
                "addl_value_land5": [592, 9, 1],
                "addl_value_bldg5": [601, 9, 1],
                "addl_value_total5": [610, 9, 1],
                "qualification_codes": [619, 5, 0],
                "assess_year": [624, 2, 1],
                "property_class": [626, 2, 0],
                "class_4_type": [628, 3, 1],
                "date_typed": [631, 6, 2, 'YYMMDD'],
                "assessor_nu_code": [637, 3, 0],
                "field_status_code": [640, 1, 0],
                "field_date": [641, 6, 2, 'YYMMDD'],
                "critical_error_flag": [647, 1, 0],
                "condo": [648, 1, 0],
                "appeal_status": [649, 1, 0],
                "assessor_written_cd": [650, 1, 0],
                "year_built": [651, 4, 1],
                "living_space": [655, 7, 1]
                }
        self.fields = ['pams_pin', "county_code", "district_code", "batch_number", "dln", "operator_initials", "last_update_date", "questionnaire_status_code", "questionnaire_date", "questionnaire_who_code", "u_n_type", "sr_nu_code", "reported_sales_price", "verified_sales_price", "assessed_value_land", "assessed_value_bldg", "assessed_value_total", "sales_ratio", "realty_transfer_fee", "rtf_error_flag", "rtf_exempt_code", "serial_number", "grantor_nctl", "grantor_name", "grantor_street", "grantor_city_state", "grantor_zip", "grantee_name", "grantee_street", "grantee_city_state", "grantee_zip", "property_location", "aging_date", "deed_book", "deed_page", "deed_date", "date_recorded", "block_prefix", "block_suffix", "lot_prefix", "lot_suffix", "etc", "addl_block1", "addl_lot1", "addl_qualifier1", "addl_value_land1", "addl_value_bldg1", "addl_value_total1", "addl_block2", "addl_lot2", "addl_qualifier2", "addl_value_land2", "addl_value_bldg2", "addl_value_total2", "addl_block3", "addl_lot3", "addl_qualifier3", "addl_value_land3", "addl_value_bldg3", "addl_value_total3", "addl_block4", "addl_lot4", "addl_qualifier4", "addl_value_land4", "addl_value_bldg4", "addl_value_total4", "addl_block5", "addl_lot5", "addl_qualifier5", "addl_value_land5", "addl_value_bldg5", "addl_value_total5", "qualification_codes", "assess_year", "property_class", "class_4_type", "date_typed", "assessor_nu_code", "field_status_code", "field_date", "critical_error_flag", "condo", "appeal_status", "assessor_written_cd", "year_built", "living_space"]
#        self.fields.extend(sorted(self.tags.keys())) # replaced with the above
        if(len(self.record) != 665):
            self.record += ("0"*(665-len(self.record)))
    def getFieldRaw(self,field):
        stri = self.tags[field][0]
        endi = self.tags[field][1]+self.tags[field][0]
        value = self.record[stri:endi].strip()
        return value
    def getField(self,field):
        if((field == "block") or (field == "lot")):
            vp = self.getField(field+"_prefix").strip().replace("'","").replace('"',"")
            vs = self.getField(field+"_suffix").strip().replace("'","").replace('"',"")
            if(vs == ""):
                return str(vp.lstrip("0"))
            else: ###### this needs to be fixed, probably just remove the digit formatting from suffix
                return "{0}.{1}".format( vp.lstrip("0"), vs.rstrip() )
        elif field in self.tags:
            stri = self.tags[field][0]
            endi = self.tags[field][1]+self.tags[field][0]
            value = self.record[stri:endi].strip()
            if(self.tags[field][2] == 1):
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
                        if(self.tags[field][3] == "MMDDYY"):
                            if(int(value[-2:]) > 32):
                                ds = "19%s-%s-%s" % (value[-2:],value[:2],value[2:4])
                            else:
                                ds = "20%s-%s-%s" % (value[-2:],value[:2],value[2:4])
                        if(self.tags[field][3] == "YYMMDD"):
                            if(int(value[:2]) > 32):
                                ds = "19%s-%s-%s" % (value[:2],value[2:4],value[-2:])
                            else:
                                ds = "20%s-%s-%s" % (value[:2],value[2:4],value[-2:])
##                        return ds
                else:
                    return "0000-00-00"
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
                        print("record length:",len(self.record))
                        print("value:",value)
                        print("break:",brk)
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
            mun = "{0:0>2d}{1:0>2d}".format(self.getField("county_code"),self.getField("district_code"))
            block = self.getField("block")
            lot = self.getField("lot")
            qual = self.getField("qualification_codes").strip()
            if(qual == ''):
                return "_".join([mun, block, lot])
            else:
                return "_".join([mun, block, lot, qual])
        except:
            print(self.record)
            raise
    def genCreateTableMySQL(self, tablename, fields=None):
        text = "CREATE TABLE `" + tablename + "` ( `recordid` INT NOT NULL UNSIGNED AUTO_INCREMENT, \n" + \
               "`pams_pin` VARCHAR(30),\n"# + \
#               "`source` VARCHAR(20),\n" + \
#               "`timeinserted` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \n"
        #### if fields parameter is not passed, all possible fields will be returned in alphabetical order
        if(fields != None):
            keysource = []
            for f in fields:
                if f in list(self.tags.keys()):
                    keysource.append( [f, self.tags[f]] )
        else:
            keysource = self.fields # sorted(self.tags.iteritems())
        for key in keysource:
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
        for key in sorted(self.tags.items()):
            if(key[1][2] == 1 or key[1][2] == 2):
                text += "`%s` = %s, " % (key[0], self.getField(key[0]))
            else:
                text += """`%s` = '%s', """ % (key[0], self.getField(key[0]))
        text = text[:-2]
        text += ";\n"
        return text
    def genCSVheader(self, df): # df: desired fields
        fields = ["pams_pin"]
        for key in sorted(self.tags.items()):
            if(key[0] in df):
                fields.append( key[0] )
        return ",".join( fields ) + "\n"
    def genCSVrecord(self, fields=None):
        pams = self.getPAMSpin()
        values = ['"{0}"'.format(pams)]
        if fields == None:
            fields = self.fields
        for f in fields:
            if f in list(self.tags.keys()):
                if(self.tags[f][2] == 0):
                    values.append( '"{0}"'.format( str(self.getField(f)).replace('"', "'").replace(r"\'", "'").replace(r"\\", "\\") ) )
                elif(self.tags[f][2] == 2):
                    if(self.getField(f) == "0000-00-00"):
                        values.append( '' )
                    else:
                        values.append( '"{0}"'.format( str(self.getField(f)).replace('"', "'") ) )
                else:
                    if self.getField(f) == None:
                        values.append( '' )
                    else:
                        values.append( str( self.getField(f) ).replace('"', "'") )
        return ",".join(values) + "\n"

        #### old alpha below
    def genCSVrecordAlpha(self, fields):
        pams = self.getPAMSpin()
        values = ['"{0}"'.format(pams)]
        for key in sorted(self.tags.items()):
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
                if f in list(self.tags.keys()):
                    keysource.append( [f, self.tags[f]] )
        else:
            keysource = sorted(self.tags.items())
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
        sql += ", ".join(["`%s`"%x for x in self.fields]) # map/lambda to wrap keys in MySQL field delimiters
        sql += ") VALUES (" + (r" %s,"*len(self.fields))[:-1]
        sql += ")"
        return sql
    def dateTest(self, datestr):
        dateOk = False
        format = '%Y-%m-%d'
        try:
            result = datetime.strptime(datestr, format)
            dateOk = (datestr == result.strftime(format)) # this makes sure the parsed date matches the original string
        except Exception as e:
            pass
#            print str(e)
        if dateOk:
            return datestr
        else:
            return '0000-00-00'

class SR1AParser2013(SR1AParser):
    """convert a fixed-width string from the SR1A (2013 and later layout) output to a dict"""
    def __init__(self,record):
        self.record = record
        self.source = ''
        self.numCheck = re.compile(r'[^\d.]+')
        """tags is a dict of tuples, with [0] as start, [1] as length, [2] as type ["string","int","date", "float"], [3] as float format"""
        self.tags = {"county_code": [0, 2, 1],
            "district_code": [2, 2, 1],
            "batch_number": [4, 5, 1],
            "dln": [9, 7, 1],
            "operator_initials": [16, 3, 0],
            "last_update_date": [19, 6, 2, 'YYMMDD'],
            "questionnaire_status_code": [25, 1, 0],
            "questionnaire_date": [26, 6, 2, 'YYMMDD'],
            "questionnaire_who_code": [32, 1, 0],
            "u_n_type": [33, 1, 0],
            "sr_nu_code": [34, 3, 0],
            "reported_sales_price": [37, 9, 1],
            "verified_sales_price": [46, 9, 1],
            "assessed_value_land": [55, 9, 1],
            "assessed_value_bldg": [64, 9, 1],
            "assessed_value_total": [73, 9, 1],
            "sales_ratio": [82, 5, 3, '3.2'],
            "realty_transfer_fee": [87, 9, 3, '7.2'],
            "rtf_error_flag": [96, 1, 0],
            "rtf_exempt_code": [97, 1, 0],
            "serial_number": [98, 7, 1],
            "grantor_nctl": [105, 4, 0],
            "grantor_name": [109, 35, 0],
            "grantor_street": [144, 25, 0],
            "grantor_city_state": [169, 25, 0],
            "grantor_zip": [194, 9, 1],
            "grantee_name": [203, 35, 0],
            "grantee_street": [238, 25, 0],
            "grantee_city_state": [263, 25, 0],
            "grantee_zip": [288, 9, 1],
            "property_location": [297, 25, 0],
            "aging_date": [322, 6, 2, 'YYMMDD'],
            "deed_book": [328, 5, 0],
            "deed_page": [333, 5, 0],
            "deed_date": [338, 6, 2, 'YYMMDD'],
            "date_recorded": [344, 6, 2, 'YYMMDD'],
            "block_prefix": [350, 5, 0],
            "block_suffix": [355, 4, 0],
            "lot_prefix": [359, 5, 0],
            "lot_suffix": [364, 4, 0],
            "etc": [368, 1, 0],
            "addl_block1": [369, 9, 0],
            "addl_lot1": [378, 9, 0],
            "addl_qualifier1": [387, 5, 0],
            "addl_value_land1": [392, 9, 1],
            "addl_value_bldg1": [401, 9, 1],
            "addl_value_total1": [410, 9, 1],
            "addl_block2": [419, 9, 0],
            "addl_lot2": [428, 9, 0],
            "addl_qualifier2": [437, 5, 0],
            "addl_value_land2": [442, 9, 1],
            "addl_value_bldg2": [451, 9, 1],
            "addl_value_total2": [460, 9, 1],
            "addl_block3": [469, 9, 0],
            "addl_lot3": [478, 9, 0],
            "addl_qualifier3": [487, 5, 0],
            "addl_value_land3": [492, 9, 1],
            "addl_value_bldg3": [501, 9, 1],
            "addl_value_total3": [510, 9, 1],
            "addl_block4": [519, 9, 0],
            "addl_lot4": [528, 9, 0],
            "addl_qualifier4": [537, 5, 0],
            "addl_value_land4": [542, 9, 1],
            "addl_value_bldg4": [551, 9, 1],
            "addl_value_total4": [560, 9, 1],
            "addl_block5": [569, 9, 0],
            "addl_lot5": [578, 9, 0],
            "addl_qualifier5": [587, 5, 0],
            "addl_value_land5": [592, 9, 1],
            "addl_value_bldg5": [601, 9, 1],
            "addl_value_total5": [610, 9, 1],
            "qualification_codes": [619, 5, 0],
            "assess_year": [624, 2, 1],
            "property_class": [626, 3, 0],
            "class_4_type": [629, 3, 1],
            "date_typed": [632, 6, 2, 'YYMMDD'],
            "assessor_nu_code": [638, 3, 0],
            "field_status_code": [641, 1, 0],
            "field_date": [642, 6, 2, 'YYMMDD'],
            "critical_error_flag": [648, 1, 0],
            "condo": [649, 1, 0],
            "appeal_status": [650, 1, 0],
            "assessor_written_cd": [651, 1, 0],
            "year_built": [652, 4, 1],
            "living_space": [656, 7, 1]
        }
        self.fields = ['pams_pin', "county_code", "district_code", "batch_number", "dln", "operator_initials", "last_update_date", "questionnaire_status_code", "questionnaire_date", "questionnaire_who_code", "u_n_type", "sr_nu_code", "reported_sales_price", "verified_sales_price", "assessed_value_land", "assessed_value_bldg", "assessed_value_total", "sales_ratio", "realty_transfer_fee", "rtf_error_flag", "rtf_exempt_code", "serial_number", "grantor_nctl", "grantor_name", "grantor_street", "grantor_city_state", "grantor_zip", "grantee_name", "grantee_street", "grantee_city_state", "grantee_zip", "property_location", "aging_date", "deed_book", "deed_page", "deed_date", "date_recorded", "block_prefix", "block_suffix", "lot_prefix", "lot_suffix", "etc", "addl_block1", "addl_lot1", "addl_qualifier1", "addl_value_land1", "addl_value_bldg1", "addl_value_total1", "addl_block2", "addl_lot2", "addl_qualifier2", "addl_value_land2", "addl_value_bldg2", "addl_value_total2", "addl_block3", "addl_lot3", "addl_qualifier3", "addl_value_land3", "addl_value_bldg3", "addl_value_total3", "addl_block4", "addl_lot4", "addl_qualifier4", "addl_value_land4", "addl_value_bldg4", "addl_value_total4", "addl_block5", "addl_lot5", "addl_qualifier5", "addl_value_land5", "addl_value_bldg5", "addl_value_total5", "qualification_codes", "assess_year", "property_class", "class_4_type", "date_typed", "assessor_nu_code", "field_status_code", "field_date", "critical_error_flag", "condo", "appeal_status", "assessor_written_cd", "year_built", "living_space"]
#        self.fields.extend(sorted(self.tags.keys()))
        if(len(self.record) != 665):
            self.record += ("0"*(665-len(self.record)))
