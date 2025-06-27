from typing import Type, Any
from decimal import Decimal, InvalidOperation
from datetime import date

__all__ = ["sr1a", "modiv"]
date_threshold = (date.today().year + 2) - 2000


def _coerce(value: str, to_type: Type, meta: dict = {}) -> Any:
    value = value.strip()
    try:
        if "numfmt" in meta:
            np = [int(x) for x in meta["numfmt"].split(".")]
            np[1] = np[1] * -1
            dec_value = Decimal(f"{value[: np[0]]}.{value[np[1] :]}")
            return dec_value
        elif "datefmt" in meta:
            year_prefix = 2000
            if value == "000000":
                return ""  # for backwards/database compatibility
            first, second, third = (int(value[:2]), int(value[2:4]), int(value[-2:]))
            if meta["datefmt"] == "YYMMDD":
                if second > 12 or third > 31: # month or day is out of bound
                    # assume then that it's MMDDYY because there's data consistencies everywhere
                    # year, month, day   ->  year, month, day 
                    first, second, third = (third, first, second)
                if first >= date_threshold:
                    year_prefix = 1900
                return date(
                    year_prefix + first, second, third
                )
            elif meta["datefmt"] == "MMDDYY":
                if third >= date_threshold:
                    year_prefix = 1900
                return date(
                    year_prefix + third,
                    first,
                    second,
                )
        else:
            return to_type(value)
    except (ValueError, TypeError, InvalidOperation) as e:
        return value  # fallback to original string if coercion fails


def parse_line(line: str, cls):
    values = {}
    for f in cls.__dataclass_fields__.values():
        meta = f.metadata
        if meta:
            raw = line[meta["start"] : meta["start"] + meta["len"]]
            values[f.name] = _coerce(raw, f.type, meta)
    return cls(**values)
