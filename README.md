# NJParcelTools
Tools to help work with cadastral data in New Jersey. 

## License
All code within this repository is licensed under the GPL, version 3. This is a "copyleft" license. Please review the GPLv3 prior to incorporating this code into your own work. 

## Contributions
Contributions to this repository are welcome and encouraged. Feel free to improve the code and submit a pull request. 

## About New Jersey's Cadastral Data
- GIS data available from [NJGIN](https://njgin.state.nj.us/NJ_NJGINExplorer/IW.jsp?DLayer=Parcels%20by%20County/Muni)
- Assessment Rolls available from [NJ Division of Taxation](http://www.state.nj.us/treasury/taxation/lpt/TaxListSearchPublicWebpage.shtml)
- [MOD IV Manual](http://www.state.nj.us/treasury/taxation/pdf/lpt/modIVmanual.pdf) - manual on how to use NJ's assessment rolls.
- [Sales Records](http://www.state.nj.us/treasury/taxation/lpt/grantors_listing.shtml), known as the "Grantor's Listing" or SR1A are also available.

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

### SR1AParser.py
Similar to the TaxListParser above, this will process the SR1A files allowing you to extract the data into CSV, PostgreSQL or MySQL. Supports current and 2012-and-prior SR1A file formats.  

### sr1a_csv.py 
Quick and dirty script to dump an SR1A file to standard output. 

*Last updated 2015-12-05*
