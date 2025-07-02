import argparse
import csv
from warnings import warn

from njparceltools import parse_line
from njparceltools.modiv import MODIVRecord
from njparceltools.sr1a import SR1ARecord

if __name__ == "__main__":
    default_fields = {
        "modiv": [
            "pams_pin",
            "muncode",
            "block",
            "lot",
            "qual",
            "property_location",
            "property_class",
            "building_description",
            "land_description",
            "calc_acreage",
            "additional_lots",
            "additional_lots2",
            "owner_name",
            "owner_address",
            "owner_city",
            "owner_zip",
            "sale_date",
            "sale_price",
            "sale_assessment",
            "assessment_code",
            "land_value",
            "improvement_value",
            "net_value",
            "net_value_prior_year",
            "taxes_last_year",
            "taxes_current_year",
            "zoning",
            "year_constructed",
            "deed_book",
            "deed_page",
        ],
        "sr1a": [
            "pams_pin",
            "property_location",
            "u_n_type",
            "sr_nu_code",
            "last_update_date",
            "reported_sales_price",
            "verified_sales_price",
            "assessed_value_land",
            "assessed_value_bldg",
            "assessed_value_total",
            "sales_ratio",
            "realty_transfer_fee",
            "serial_number",
            "grantor_name",
            "grantor_street",
            "grantor_city_state",
            "grantor_zip",
            "grantee_name",
            "grantee_street",
            "grantee_city_state",
            "grantee_zip",
            "deed_book",
            "deed_page",
            "deed_date",
            "date_recorded",
            "qualification_codes",
            "property_class",
            "class_4_type",
            "year_built",
            "living_space",
            "condo",
        ],
    }

    import os

    p = argparse.ArgumentParser(
        description="Tools to work with New Jersey parcel and assessment data."
    )
    p.add_argument("type", help="Type of input file [modiv, sr1a]")
    p.add_argument("input_file", help="Input flat file")
    p.add_argument("output_file", help="Output CSV file")
    p.add_argument("--source", help='Value for "source" column in output')
    p.add_argument(
        "--noheader", action="store_true", help="Do not include header in output CSV"
    )
    p.add_argument("--fields", help="Comma delimited list of fields to include in CSV")

    args = p.parse_args()
    if not os.path.exists(args.input_file):
        raise FileNotFoundError(f"Unable to open {args.input_file}")
    if os.path.exists(args.output_file):
        warn("Output file exists, overwriting...")

    header_row = []
    if args.type.lower() == "modiv":
        parser_class = MODIVRecord
        header_row = default_fields["modiv"]
    elif args.type.lower() == "sr1a":
        parser_class = SR1ARecord
        header_row = default_fields["sr1a"]
    else:
        raise Exception("Invalid type specified.")
    if args.source:
        header_row.insert(0, "source")

    # override fields based on user-provided argument
    if args.fields:
        header_row = args.fields.split(",")

    with open(args.input_file, "r") as infile:
        with open(args.output_file, "w") as outfile:
            csvw = csv.DictWriter(
                outfile, fieldnames=header_row, quoting=csv.QUOTE_NONNUMERIC
            )
            if not args.noheader:
                csvw.writeheader()
            for line in infile.readlines():
                parsed_data = parse_line(line, parser_class).as_dict(header_row)
                if args.source:
                    parsed_data["source"] = args.source
                csvw.writerow(parsed_data)
