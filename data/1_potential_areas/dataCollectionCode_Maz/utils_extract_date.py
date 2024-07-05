import re
from typing import Union

import pandas as pd
from pandas._libs.tslibs.nattype import NaTType


def extract_date_from_string(input_string) -> Union[str, None]:
    # Use regular expression to find the date in the format YYYYMMDD from the input string
    date_match: re.Match[str] | None = re.search(r"\d{8}", input_string)
    if date_match:
        # Extract the matched date part
        date_part: str = date_match.group(0)
        # Use pandas to convert the extracted date part into a datetime object
        date: pd.Timestamp | NaTType = pd.to_datetime(
            date_part, format="%Y%m%d", errors="coerce"
        )
        # Check if the conversion was successful and format the date
        if pd.notna(date):
            return date.strftime("%Y-%m-%d")
    return None


def extract_month_from_date(date: str) -> str:
    return str(int(date[5:7]) - int(1)) if date else "Unknown"


# # Example usage
# input_string = "zone4_20230210T102049_20230210T102804_T32TNR"
# date_only = extract_date_from_string(input_string)
# print(f"Extracted Date: {date_only}")
