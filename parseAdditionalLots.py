#!/usr/bin/env python
import csv, sys, re

def expandRange(s):
    nonnum = re.compile(r'[^\d.]+')
    remsla = re.compile(r'\-.*\/.*\-')
    if ('-' not in s) and ('&' not in s):
        return (s.replace("LOT ",'').replace("L",'').replace(" ",''),)
    else:
        s = remsla.sub('', s)
        if '.' not in s:
            s = s.replace("LOT ",'').replace("L","").replace(" ", "").replace("&","-")
            part = map(lambda x: nonnum.sub('',x), s.split('-'))
            part = [(x and int(x)) or 0 for x in part]
            if len(part) == 1:
                return s
            return map(lambda x: str(x), range(part[0], part[1]+1, 1))
        else:
            s = s.replace("LOT ",'').replace("L","").replace(" ", "").replace("&","-")
            base = s.split('.')
            part = map(lambda x: nonnum.sub('',x), base[1].split('-'))
            part = [(x and int(x)) or 0 for x in part] 
            if len(part) == 1:
                return s
            rng  = range(part[0], part[1]+1, 1)
            return map(lambda x: base[0]+'.'+str(x).zfill(2), rng)

# def expandRange(s):
#     if '-' not in s:
#         return (s,)
#     else:
#         if '.' not in s:
#             part = map(lambda x: int(x), s.split('-'))
#             return map(lambda x: str(x), range(part[0], part[1]+1, 1))
#         else:
#             base = s.split('.')
#             part = map(lambda x: int(x), base[1].split('-'))
#             rng  = range(part[0], part[1]+1, 1)
#             return map(lambda x: '.'+str(x).zfill(2), rng)

ifn = sys.argv[1]
ofn = sys.argv[2]
with open(ifn, "rb") as infile:
    reader = csv.DictReader(infile, delimiter=',', quotechar='"')
    fields = reader.fieldnames
    with open(ofn, "wb") as csvf:
        csvw = csv.writer(csvf, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)  # QUOTE_NONNUMERIC     
#        fields = map(lambda x: x.name, arcpy.ListFields(parameters[0].valueAsText))
#        fields.remove("pams_pin_X")
#        fields.remove("pams_pin_Y")
        csvw.writerow(fields)
        for row in reader:
            csvout = []
            if row.get("additional_lots") == '' or row.get("additional_lots") == None:
                csvout = ( [row.get(f) for f in fields] ,)
            else:
                csvout = [ [row.get(f) for f in fields] ,]
                s = row.get("additional_lots")
                lots = []
                if '.' in s:
                    ### because additional_lots is limited to 20 characters, 
                    ### this expands out some of the shorthand used before parsing the string
                    ### a check for a period after a comma should be put in place to make sure
                    ### there isn't any overzealous parsing
                    pass
                for l in s.split(','):
                    parsedlist = expandRange(l)
##                        try: ## kludge
##                            if(parsedlist[0][0] == '.'):
##                                parsedlist = map(lambda x: "{0}{1}".format(l.split('.')[0], x), parsedlist)
##                        except:
##                            pass
                    lots.extend( parsedlist )
                print lots
                for l in lots:
                    r = []
                    for f in fields:
                        if len(l) >= 10:
                            l = l[:8]
                        if f == 'pams_pin':
                            pin = "_".join( (str(row.get("muncode")), str(row.get("block")), str(l), str(row.get("qual"))) ) 
                            r.append(pin.strip("_"))
                            print pin.strip("_")
                        elif f == 'lot':
                            r.append(str(l))
                        elif f == 'source':
                            r.append("Expanded")
                        else:
                            r.append(str(row.get(f)))
                    csvout.append(r)
                print csvout
            csvw.writerows( csvout )
