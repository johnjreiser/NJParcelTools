from dataclasses import dataclass, field, asdict


@dataclass
class SR1ARecord:
    county_code: int = field(metadata={"start": 0, "len": 2})
    district_code: int = field(metadata={"start": 2, "len": 2})
    batch_number: int = field(metadata={"start": 4, "len": 5})
    dln: int = field(metadata={"start": 9, "len": 7})
    operator_initials: str = field(
        metadata={
            "start": 16,
            "len": 3,
        }
    )
    last_update_date: str = field(metadata={"start": 19, "len": 6, "datefmt": "YYMMDD"})
    questionnaire_status_code: str = field(metadata={"start": 25, "len": 1})
    questionnaire_date: str = field(
        metadata={"start": 26, "len": 6, "datefmt": "YYMMDD"}
    )
    questionnaire_who_code: str = field(metadata={"start": 32, "len": 1})
    u_n_type: str = field(metadata={"start": 33, "len": 1})
    sr_nu_code: str = field(metadata={"start": 34, "len": 3})
    reported_sales_price: int = field(metadata={"start": 37, "len": 9})
    verified_sales_price: int = field(metadata={"start": 46, "len": 9})
    assessed_value_land: int = field(metadata={"start": 55, "len": 9})
    assessed_value_bldg: int = field(metadata={"start": 64, "len": 9})
    assessed_value_total: int = field(metadata={"start": 73, "len": 9})
    sales_ratio: float = field(metadata={"start": 82, "len": 5, "numfmt": "3.2"})
    realty_transfer_fee: float = field(
        metadata={"start": 87, "len": 9, "numfmt": "7.2"}
    )
    rtf_error_flag: str = field(metadata={"start": 96, "len": 1})
    rtf_exempt_code: str = field(metadata={"start": 97, "len": 1})
    serial_number: int = field(metadata={"start": 98, "len": 7})
    grantor_nctl: str = field(metadata={"start": 105, "len": 4})
    grantor_name: str = field(metadata={"start": 109, "len": 35})
    grantor_street: str = field(metadata={"start": 144, "len": 25})
    grantor_city_state: str = field(metadata={"start": 169, "len": 25})
    grantor_zip: str = field(metadata={"start": 194, "len": 9})
    grantee_name: str = field(metadata={"start": 203, "len": 35})
    grantee_street: str = field(metadata={"start": 238, "len": 25})
    grantee_city_state: str = field(metadata={"start": 263, "len": 25})
    grantee_zip: str = field(metadata={"start": 288, "len": 9})
    property_location: str = field(metadata={"start": 297, "len": 25})
    aging_date: str = field(metadata={"start": 322, "len": 6, "datefmt": "YYMMDD"})
    deed_book: str = field(metadata={"start": 328, "len": 5})
    deed_page: str = field(metadata={"start": 333, "len": 5})
    deed_date: str = field(metadata={"start": 338, "len": 6, "datefmt": "YYMMDD"})
    date_recorded: str = field(metadata={"start": 344, "len": 6, "datefmt": "YYMMDD"})
    block_prefix: str = field(metadata={"start": 350, "len": 5})
    block_suffix: str = field(metadata={"start": 355, "len": 4})
    lot_prefix: str = field(metadata={"start": 359, "len": 5})
    lot_suffix: str = field(metadata={"start": 364, "len": 4})
    etc: str = field(metadata={"start": 368, "len": 1})
    addl_block1: str = field(metadata={"start": 369, "len": 9})
    addl_lot1: str = field(metadata={"start": 378, "len": 9})
    addl_qualifier1: str = field(metadata={"start": 387, "len": 5})
    addl_value_land1: int = field(metadata={"start": 392, "len": 9})
    addl_value_bldg1: int = field(metadata={"start": 401, "len": 9})
    addl_value_total1: int = field(metadata={"start": 410, "len": 9})
    addl_block2: str = field(metadata={"start": 419, "len": 9})
    addl_lot2: str = field(metadata={"start": 428, "len": 9})
    addl_qualifier2: str = field(metadata={"start": 437, "len": 5})
    addl_value_land2: int = field(metadata={"start": 442, "len": 9})
    addl_value_bldg2: int = field(metadata={"start": 451, "len": 9})
    addl_value_total2: int = field(metadata={"start": 460, "len": 9})
    addl_block3: str = field(metadata={"start": 469, "len": 9})
    addl_lot3: str = field(metadata={"start": 478, "len": 9})
    addl_qualifier3: str = field(metadata={"start": 487, "len": 5})
    addl_value_land3: int = field(metadata={"start": 492, "len": 9})
    addl_value_bldg3: int = field(metadata={"start": 501, "len": 9})
    addl_value_total3: int = field(metadata={"start": 510, "len": 9})
    addl_block4: str = field(metadata={"start": 519, "len": 9})
    addl_lot4: str = field(metadata={"start": 528, "len": 9})
    addl_qualifier4: str = field(metadata={"start": 537, "len": 5})
    addl_value_land4: int = field(metadata={"start": 542, "len": 9})
    addl_value_bldg4: int = field(metadata={"start": 551, "len": 9})
    addl_value_total4: int = field(metadata={"start": 560, "len": 9})
    addl_block5: str = field(metadata={"start": 569, "len": 9})
    addl_lot5: str = field(metadata={"start": 578, "len": 9})
    addl_qualifier5: str = field(metadata={"start": 587, "len": 5})
    addl_value_land5: int = field(metadata={"start": 592, "len": 9})
    addl_value_bldg5: int = field(metadata={"start": 601, "len": 9})
    addl_value_total5: int = field(metadata={"start": 610, "len": 9})
    qualification_codes: str = field(metadata={"start": 619, "len": 5})
    assess_year: int = field(metadata={"start": 624, "len": 2})
    property_class: str = field(metadata={"start": 626, "len": 3})
    class_4_type: int = field(metadata={"start": 629, "len": 3})
    date_typed: str = field(metadata={"start": 632, "len": 6, "datefmt": "YYMMDD"})
    assessor_nu_code: str = field(metadata={"start": 638, "len": 3})
    field_status_code: str = field(metadata={"start": 641, "len": 1})
    field_date: str = field(metadata={"start": 642, "len": 6, "datefmt": "YYMMDD"})
    critical_error_flag: str = field(metadata={"start": 648, "len": 1})
    condo: str = field(metadata={"start": 649, "len": 1})
    appeal_status: str = field(metadata={"start": 650, "len": 1})
    assessor_written_cd: str = field(metadata={"start": 651, "len": 1})
    year_built: int = field(metadata={"start": 652, "len": 4})
    living_space: int = field(metadata={"start": 656, "len": 7})
    block: str = None
    lot: str = None
    pams_pin: str = None

    def __post_init__(self):
        # define block
        vp = self.block_prefix.replace("'", "").replace('"', "")
        vs = self.block_suffix.replace("'", "").replace('"', "")
        if vs == "":
            self.block = str(vp.lstrip("0"))
        else:  ###### this needs to be fixed, probably just remove the digit formatting from suffix
            self.block = "{0}.{1}".format(vp.lstrip("0"), vs.rstrip())
        # define lot
        vp = self.lot_prefix.replace("'", "").replace('"', "")
        vs = self.lot_suffix.replace("'", "").replace('"', "")
        if vs == "":
            self.lot = str(vp.lstrip("0"))
        else:  ###### this needs to be fixed, probably just remove the digit formatting from suffix
            self.lot = "{0}.{1}".format(vp.lstrip("0"), vs.rstrip())
        # define pams_pin
        if not (
            isinstance(self.county_code, int) and isinstance(self.district_code, int)
        ):
            raise ValueError(
                "Unable to determine municipality code from county/district codes. Check input values."
            )
        mun = "{0:0>2d}{1:0>2d}".format(self.county_code, self.district_code)
        # mun = None
        self.pams_pin = "_".join(
            filter(None, (mun, self.block, self.lot, self.qualification_codes))
        )

    def as_dict(self, keep_keys: list = []):
        if keep_keys:
            reduced = {
                k: getattr(self, k) for k in keep_keys if k in self.__dataclass_fields__
            }
            return reduced
        else:
            return asdict(self)
