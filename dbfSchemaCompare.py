#!/usr/bin/env python
# dbfSchemaCompare.py
# author:   John Reiser <jreiser@njgeo.org>
# purpose:  Generates a simple report showing matching schemas from a list of DBF files.
#           Helpful for determining if Shapefiles contain the same or similar structures. 
# requires: dbfpy (http://sourceforge.net/projects/dbfpy/files/)
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

import sys, os, glob
from dbfpy import dbf

files = []
for maybe_glob in sys.argv[1:]:
    for filename in glob.iglob(maybe_glob):
        if(os.path.exists(filename)):
            files.append(filename)

fns = 0
schemas = {}
for file in files:
    db = dbf.Dbf(file)
    fd = "\t".join(map(lambda x: str(x).split()[0], db.fieldDefs))
    if fns == 0:
        fns = set(map(lambda x: str(x).split()[0], db.fieldDefs))
    else:
        if not fns == None:
            fns &= set(map(lambda x: str(x).split()[0], db.fieldDefs))
    if fd in schemas.keys():
        schemas[fd].append(file)
    else:
        schemas[fd] = [file]

# print schemas

for sd in schemas.keys():
    if(len(schemas[sd]) == 1):
        print schemas[sd][0], "has the following unique schema:"    
    else:
        print ", ".join(schemas[sd]), "share the following schema:"
    print "\n".join(map(lambda x: "  "+x, sd.split("\t")))
if not fns == None:
    print "These field names are shared amongst all:", ", ".join(fns)
