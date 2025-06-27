from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class MODIVRecord:
    muncode: str = field(metadata={"start": 0, "len": 4})
    block: str = field(metadata={"start": 4, "len": 9})
    lot: str = field(metadata={"start": 13, "len": 9})
    qual: str = field(metadata={"start": 22, "len": 11})
    transaction_date: str = field(
        metadata={"start": 37, "len": 6, "datefmt": "YYMMDD"}
    )  # , 2)
    transaction_update_number: int = field(metadata={"start": 43, "len": 4})  # , 1)
    tax_account_number: str = field(metadata={"start": 47, "len": 8})
    property_class: str = field(metadata={"start": 55, "len": 3})
    property_location: str = field(metadata={"start": 58, "len": 25})
    building_description: str = field(metadata={"start": 83, "len": 15})
    land_description: str = field(metadata={"start": 98, "len": 20})
    calc_acreage: Decimal = field(
        metadata={"start": 118, "len": 9}
    )  # , 3, "5.4")  # formatted as 12345(.)6789
    additional_lots: str = field(metadata={"start": 127, "len": 20})
    additional_lots2: str = field(metadata={"start": 147, "len": 20})
    zoning: str = field(metadata={"start": 167, "len": 4})
    tax_map_number: str = field(metadata={"start": 171, "len": 4})
    owner_name: str = field(metadata={"start": 175, "len": 35})
    owner_address: str = field(metadata={"start": 210, "len": 25})
    owner_city: str = field(metadata={"start": 235, "len": 25})
    owner_zip: str = field(metadata={"start": 260, "len": 9})
    number_of_owners: int = field(metadata={"start": 269, "len": 4})  # , 1)
    deduction: int = field(metadata={"start": 273, "len": 6})  # , 1)
    bank_code: str = field(metadata={"start": 280, "len": 5})
    mortgage_account_number: str = field(metadata={"start": 285, "len": 10})
    deed_book: str = field(metadata={"start": 295, "len": 5})
    deed_page: str = field(metadata={"start": 300, "len": 5})
    sales_price_code: str = field(metadata={"start": 305, "len": 1})
    sale_date: str = field(
        metadata={"start": 306, "len": 6, "datefmt": "YYMMDD"}
    )  # , 2)
    sale_price: int = field(metadata={"start": 312, "len": 9})  # , 1)
    sale_assessment: int = field(metadata={"start": 321, "len": 9})  # , 1)
    sale_sr1a: str = field(metadata={"start": 330, "len": 2})
    rebate_ssn: str = field(metadata={"start": 332, "len": 9})
    rebate_spouse: str = field(metadata={"start": 341, "len": 9})
    rebate_number_dwellings: str = field(metadata={"start": 350, "len": 2})
    rebate_number_commercial: str = field(metadata={"start": 352, "len": 2})
    rebate_multiple_occupancy: str = field(metadata={"start": 354, "len": 1})
    rebate_percent_owned: str = field(metadata={"start": 355, "len": 1})
    rebate_code: str = field(metadata={"start": 356, "len": 2})
    rebate_delinquent: str = field(metadata={"start": 358, "len": 1})
    exempt_own: str = field(metadata={"start": 359, "len": 2})
    exempt_use: str = field(metadata={"start": 361, "len": 2})
    exempt_desc: str = field(metadata={"start": 363, "len": 3})
    exempt_initial_date: str = field(
        metadata={"start": 366, "len": 6, "datefmt": "YYMMDD"}
    )  # , 2)
    exempt_further_date: str = field(
        metadata={"start": 372, "len": 6, "datefmt": "YYMMDD"}
    )  # , 2)
    exempt_statute: str = field(metadata={"start": 378, "len": 12})
    exempt_facility: str = field(metadata={"start": 390, "len": 20})
    building_class: str = field(metadata={"start": 410, "len": 5})
    year_constructed: str = field(metadata={"start": 415, "len": 4})
    assessment_code: int = field(metadata={"start": 419, "len": 1})  # , 0, 1)
    land_value: int = field(metadata={"start": 420, "len": 9})  # , 1)
    improvement_value: int = field(metadata={"start": 429, "len": 9})  # , 1)
    net_value: int = field(metadata={"start": 438, "len": 9})  # , 1)
    tax_code_1: str = field(metadata={"start": 447, "len": 3})
    tax_code_2: str = field(metadata={"start": 450, "len": 3})
    tax_code_3: str = field(metadata={"start": 453, "len": 3})
    tax_code_4: str = field(metadata={"start": 456, "len": 3})
    exemption_1_code: str = field(metadata={"start": 459, "len": 1})
    exemption_1_amt: int = field(metadata={"start": 460, "len": 8})  # , 1)
    exemption_2_code: str = field(metadata={"start": 468, "len": 1})
    exemption_2_amt: int = field(metadata={"start": 469, "len": 8})  # , 1)
    exemption_3_code: str = field(metadata={"start": 477, "len": 1})
    exemption_3_amt: int = field(metadata={"start": 478, "len": 8})  # , 1)
    exemption_4_code: str = field(metadata={"start": 486, "len": 1})
    exemption_4_amt: int = field(metadata={"start": 487, "len": 8})  # , 1)
    deduction_senior: int = field(metadata={"start": 495, "len": 4})  # , 1)
    deduction_veteran: int = field(metadata={"start": 499, "len": 4})  # , 1)
    deduction_widow: int = field(metadata={"start": 503, "len": 4})  # , 1)
    deduction_surv_spouse: int = field(metadata={"start": 507, "len": 3})  # , 1)
    deduction_disabled: int = field(metadata={"start": 510, "len": 3})  # , 1)
    user_field_1: str = field(metadata={"start": 513, "len": 4})
    user_field_2: str = field(metadata={"start": 517, "len": 4})
    old_property_id: str = field(metadata={"start": 521, "len": 29})
    census_tract: str = field(metadata={"start": 550, "len": 5})
    census_block: str = field(metadata={"start": 555, "len": 4})
    property_use_code: str = field(metadata={"start": 559, "len": 3})
    property_flags: str = field(metadata={"start": 562, "len": 10})
    tenant_response: str = field(metadata={"start": 572, "len": 1})
    tenant_base_year: str = field(metadata={"start": 573, "len": 4})
    tenant_base_tax: Decimal = field(metadata={"start": 577, "len": 9})  # , 3, "7.2")
    tenant_base_net_val: int = field(metadata={"start": 586, "len": 9})  # , 1)
    taxes_last_year: Decimal = field(metadata={"start": 600, "len": 9})  # , 3, "7.2")
    taxes_current_year: Decimal = field(
        metadata={"start": 609, "len": 9}
    )  # , 3, "7.2")
    non_municipal_half1: Decimal = field(
        metadata={"start": 618, "len": 9}
    )  # , 3, "7.2")
    non_municipal_half2: Decimal = field(
        metadata={"start": 627, "len": 9}
    )  # , 3, "7.2")
    municipal_half1: Decimal = field(metadata={"start": 636, "len": 9})  # , 3, "7.2")
    municipal_half2: Decimal = field(metadata={"start": 645, "len": 9})  # , 3, "7.2")
    non_municipal_half3: Decimal = field(
        metadata={"start": 654, "len": 9}
    )  # , 3, "7.2")
    municipal_half3: Decimal = field(metadata={"start": 663, "len": 9})  # , 3, "7.2")
    bill_status_flag: str = field(metadata={"start": 672, "len": 1})
    tax_estimated_qtr3: Decimal = field(
        metadata={"start": 673, "len": 9}
    )  # , 3, "7.2")
    net_value_prior_year: int = field(metadata={"start": 682, "len": 9})  # , 1)
    statement_aid_amt: Decimal = field(metadata={"start": 691, "len": 9})  # , 3, "7.2")

    def __post_init__(self):
        self.pams_pin = "_".join(
            filter(None, (self.muncode, self.block, self.lot, self.qual))
        )
