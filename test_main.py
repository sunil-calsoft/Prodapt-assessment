import csv
import glob
import os

from main import read_from_csv, write_to_csv, get_bank_by_file_path
from banks_structure import BANKS_CONFIG


BANK1_DATA = [{'type': 'remove', 'amount': '99.20', 'from': '198', 'to': '182', 'date': '2019-10-01'}, {'type': 'add', 'amount': '2000.10', 'from': '188', 'to': '198', 'date': '2019-10-02'}]

def test_read_from_csv():
    """Test read from csv function for any one bank."""
    bank1="bank1"
    file_path_by_name = get_bank_by_file_path(dir="bankdata")
    bank_data = read_from_csv(bank1, file_path_by_name[bank1], BANKS_CONFIG[bank1])

    assert bank_data == BANK1_DATA

def test_write_to_csv(tmpdir):
    """Test write to csv function for any one bank."""
    file = (tmpdir / "unified.csv")
    write_to_csv(BANK1_DATA, unified_file=file)

    with open(file) as f:
        output = csv.DictReader(f)
        assert [data for data in output] == BANK1_DATA
        