import csv
import glob
import json
import os
import sys
from datetime import datetime, date

# sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../")))
from banks_structure import banks_structure

converted_data = []


def read_csv(bank_name, bank_file, bank_spec):
    """Read csv file and create a list of data for each file"""
    with open(bank_file) as csv_file:
        csv_data = csv.DictReader(csv_file)
        for dict_data in csv_data:
            new_dict = {}
            for field in bank_spec[bank_name]['fields']:
                name = field['name']
                csv_value = dict_data[name]
                new_dict["bank_name"] = bank_name
                try:
                    if field['type'] == 'int':
                        new_dict[name] = int(csv_value)
                    elif field['type'] == 'float':
                        new_dict[name] = float(csv_value)
                    elif field['type'] == 'date':
                        dt_temp = datetime.strptime(csv_value, field['format'])
                        new_dict[name] = date(dt_temp.year,
                                              dt_temp.month,
                                              dt_temp.day)
                    else:
                        new_dict[name] = csv_value
                except:
                    continue
            converted_data.append(new_dict)
    return converted_data


def transform(data, transform_to, bank_name):
    """Transform the data to another value"""
    for data_dict in data:
        if data_dict["bank_name"] == bank_name:
            for rule in transform_to:
                name = rule[1]
                if rule[0] == 'add_fields':
                    data_dict[name] = data_dict[name] + data_dict[rule[2]]
                elif rule[0] == 'divide':
                    data_dict[name] = data_dict[name] / rule[2]


def to_csv_file(bank_data, csv_spec, file_path_by_name):
    """Write converted data to csv file"""
    with open("unified_csv.csv", 'w') as csv_file:
        header = []
        bank_name = list(file_path_by_name.keys())[0]
        for field in csv_spec[bank_name]["to_csv"]:
            header.append(field['name'])

        csv_output = csv.writer(csv_file)
        csv_output.writerow(header)

        for bank_name in file_path_by_name.keys():
            for dict_fields in bank_data:
                data_list = []
                if bank_name == dict_fields["bank_name"]:
                    for field in csv_spec[bank_name]["to_csv"]:
                        data_list.append(dict_fields[field['field']])
                    csv_output.writerow(data_list)


if __name__ == '__main__':
    file_path_by_name = {os.path.basename(file).split(".")[0]: file for file in glob.glob("bankdata" + '/*.csv')}

    for bank_name, bank_file in file_path_by_name.items():
        # Read CSV file
        read_csv(bank_name, bank_file, banks_structure)

        # Do conversions if required
        bank_info = banks_structure[bank_name]
        if 'transform' in bank_info:
            transform(converted_data, bank_info['transform'], bank_name)
    
    # Write to unified csv file
    to_csv_file(converted_data, banks_structure, file_path_by_name)