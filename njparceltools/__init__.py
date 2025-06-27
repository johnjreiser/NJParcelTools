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
            if meta["datefmt"] == "YYMMDD":
                if int(value[:2]) >= date_threshold:
                    year_prefix = 1900
                return date(
                    year_prefix + int(value[:2]), int(value[2:4]), int(value[-2:])
                )
            elif meta["datefmt"] == "MMDDYY":
                if int(value[-2:]) >= date_threshold:
                    year_prefix = 1900
                return date(
                    year_prefix + int(value[-2:]),
                    int(value[:2]),
                    int(value[2:4]),
                )
        else:
            return to_type(value)
    except (ValueError, TypeError, InvalidOperation) as e:
        #print(e)
        print(meta, value)
        return value  # fallback to original string if coercion fails


def parse_line(line: str, cls):
    values = {}
    for f in cls.__dataclass_fields__.values():
        meta = f.metadata
        if meta:
            raw = line[meta["start"] : meta["start"] + meta["len"]]
            values[f.name] = _coerce(raw, f.type, meta)
    return cls(**values)
