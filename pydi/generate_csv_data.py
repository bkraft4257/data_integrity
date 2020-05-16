#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 18:55:19 2019
@author: krishnaparekh

https://github.com/Krishna-Parekh/pythonFaker/blob/master/CSVgenerateFaker.py
"""

import argparse
import sys
import csv
from faker import Faker
import datetime


def generate_data(records, filename, headers):
    fake = Faker('en_US')

    with open(filename, 'wt') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in range(records):
            full_name = fake.name()
            FLname = full_name.split(" ")
            Fname = FLname[0]
            Lname = FLname[1]
            domain_name = "@testDomain.com"
            userId = Fname + "." + Lname + domain_name

            writer.writerow({
                "Email Id": userId,
                "Prefix": fake.prefix(),
                "Name": fake.name(),
                "Birth Date": fake.date(pattern="%d-%m-%Y", end_datetime=datetime.date(2000, 1, 1)),
                "Phone Number": fake.phone_number(),
                "Additional Email Id": fake.email(),
                "Address": fake.address(),
                "Zip Code": fake.zipcode(),
                "City": fake.city(),
                "State": fake.state(),
                "Country": fake.country(),
                "Year": fake.year(),
                "Time": fake.time(),
                "Link": fake.url(),
                "Text": fake.word(),
            })


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


def _main():
    in_args = _argparse_command_line()

    records = in_args.n_records
    filename = in_args.filename
    headers = ["Email Id", "Prefix", "Name", "Birth Date", "Phone Number", "Additional Email Id",
               "Address", "Zip Code", "City", "State", "Country", "Year", "Time", "Link", "Text"]

    generate_data(records, filename, headers)
    print("CSV generation complete!")


if __name__ == '__main__':
    sys.exit(_main())
