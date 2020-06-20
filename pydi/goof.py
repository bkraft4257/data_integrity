#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 18:55:19 2019
@author: krishnaparekh

https://github.com/Krishna-Parekh/pythonFaker/blob/master/CSVgenerateFaker.py
"""

import argparse
import datetime
import pandas as pd
import sys

import numpy as np
from faker import Faker

DATA_HEADERS = ["Email Id", "Prefix", "Name", "Birth Date", "SSN", "Phone Number",
               "Address", "Zip Code", "City", "State", "Country",
               "Number of Children", "Annual Salary"]


def generate_fake_data_set(n_records, seed=0):

    if n_records < 0:
        raise ValueError

    _set_seeds(seed)
    fake = Faker('en_US')

    full_data = []
    for ii in range(n_records):
        full_data.append(generate_full_data_dictionary(fake))

    print(full_data)
    return pd.DataFrame(data=full_data)


def _set_seeds(seed):
    np.random.seed(seed)
    Faker.seed(seed)


def write_to_csv_file(data, filename, headers=None):

    if headers is None:
        headers = DATA_HEADERS

    data[headers].to_csv(filename, index=False)


def _argparse_command_line():
    """
    Parse parameters from the command line.
    """

    parser = argparse.ArgumentParser(prog='generate_csv_data')

    parser.add_argument("filename", type=str, default='faker.csv')
    parser.add_argument("-n", "--n_records", type=int, default=10)
    parser.add_argument("-v", "--verbose", help="Verbose flag", action="store_true", default=False)

    in_args = parser.parse_args()

    return in_args


def generate_full_data_dictionary(fake):
    return {
        "Email Id": fake.first_name() + "." + fake.last_name() + "@testDomain.com",
        "Prefix": fake.prefix(),
        "Name": fake.name(),
        "Birth Date": fake.date(pattern="%d-%m-%Y", end_datetime=datetime.date(2000, 1, 1)),
        "SSN": fake.ssn(),
        "Phone Number": fake.phone_number(),
        "Address": fake.address(),
        "Zip Code": fake.zipcode(),
        "City": fake.city(),
        "State": fake.state(),
        "Country": fake.country(),
        "Number of Children": np.random.randint(low=0, high=6, size=1)[0],
        "Annual Salary": int(max(14000, np.random.normal(loc=60000, scale=10000, size=1))),
    }


def _main():
    in_args = _argparse_command_line()

    records = in_args.n_records
    filename = in_args.filename

    fake_data = generate_fake_data_set(records)
    write_to_csv_file(fake_data, filename, headers=None )


if __name__ == '__main__':
    sys.exit(_main())

