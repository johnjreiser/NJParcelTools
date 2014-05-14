# NJParcelTools
Tools to help work with cadastral data in New Jersey. 

## About New Jersey's Cadastral Data
- GIS data available from [NJGIN](https://njgin.state.nj.us/NJ_NJGINExplorer/IW.jsp?DLayer=Parcels%20by%20County/Muni)
- Assessment Rolls available from [NJ Division of Taxation](http://www.state.nj.us/treasury/taxation/lpt/TaxListSearchPublicWebpage.shtml)
- [MOD IV Manual](http://www.state.nj.us/treasury/taxation/pdf/lpt/modIVmanual.pdf) - manual on how to use NJ's assessment rolls.


## Tools in this Repository
### dbfSchemaCompare.py
A python script to help you compare .dbf file structures. Helpful when you're trying to make sense of a group of shapefiles. 

### DownloadExtractParcels.py
A python script to download the available spatial and tabular data from NJGIN, New Jersey's spatial data clearinghouse.

### DownloadMODIV.sh
A shell script to download, extract and convert MOD-IV flat files to CSV. 

### convertMODIVtoCSV.py
A python script to convert MOD-IV flat files to CSV format. 

### processCertifiedTaxLists.py
Downloads, extracts and converts the flat-file assessment rolls to CSV. 

### TaxListParser.py
Module to process NJ's Certified Tax Lists in flat-file text format. Can produce CSVs or SQL to import into PostgreSQL or MySQL.

*Last updated 2014-05-14*