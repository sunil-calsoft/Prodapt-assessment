"""Script to parse the different bank's data and write to a single file in unified form."""
import csv
from collections import OrderedDict
from datetime import datetime, date
import glob
import json
import os
import sys
import typing as t

from banks_structure import BANKS_CONFIG, UNIFIED_BANK_HEADER

UNIFIED_FILE = "unified_csv.csv"


def get_bank_by_file_path(dir: str) -> dict:
    """This function return bank by its file path."""
    return {
        os.path.basename(file).split(".")[0]: file for file in glob.glob(dir + "/*.csv")
    }


def read_from_csv(
    bank_name: str, bank_file: str, bank_spec: dict
) -> t.List[OrderedDict[t.Any, t.Any]]:
    """Read csv file and create a list of data for each file."""
    with open(bank_file) as csv_file:
        csv_data = csv.DictReader(csv_file)
        unified_data: t.List[OrderedDict[t.Any, t.Any]] = []
        for bank_data in csv_data:
            # Combine fields if required as per calculation
            for rule in bank_spec["transform_to"]:
                ops, field1, field2 = rule
                if ops == "add_fields":
                    bank_data[field1] = float(bank_data[field1]) + float(
                        bank_data.pop(field2)
                    )
                elif ops == "divide":
                    bank_data[field1] = int(bank_data[field1]) / field2

            # Replace the key name as per unified csv
            for key, value in bank_spec["replace_keys"].items():
                bank_data[value] = bank_data.pop(key)

            # Convert the date format in required form
            dt_temp = datetime.strptime(bank_data["date"], bank_spec["date_format"])
            bank_data["date"] = str(date(dt_temp.year, dt_temp.month, dt_temp.day))
            unified_data.append(bank_data)
    return unified_data


def write_to_csv(
    unified_data: t.List[OrderedDict[t.Any, t.Any]], unified_file: str = UNIFIED_FILE
) -> None:
    """Write converted data to csv file."""
    with open(unified_file, "a", newline="\n") as csv_file:
        csv_output = csv.DictWriter(csv_file, fieldnames=UNIFIED_BANK_HEADER)
        if csv_file.tell() == 0:
            csv_output.writeheader()
        csv_output.writerows(unified_data)


if __name__ == "__main__":
    # Remove the existing output file if exists.
    if os.path.exists(UNIFIED_FILE):
        os.remove(UNIFIED_FILE)

    file_path_by_name = get_bank_by_file_path(dir="bankdata")
    for bank_name, file_path in file_path_by_name.items():
        # Read bank's CSV file
        try:
            unified_data = read_from_csv(bank_name, file_path, BANKS_CONFIG[bank_name])
        except Exception as exc:
            print(f"Error while reading bank {bank_name!r} data from its csv: {exc}")

        # Write to unified csv file
        try:
            write_to_csv(unified_data)
        except Exception as exc:
            print(f"Error while writing bank {bank_name!r} data to unified CSV: {exc}")
