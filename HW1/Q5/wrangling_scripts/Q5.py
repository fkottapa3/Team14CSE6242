"""
Q5.py - utilities to supply data to the templates.

This file contains a pair of functions for retrieving and manipulating data
that will be supplied to the template for generating the table.
"""

import csv
import os


def username():
    return "fkottapa3"


def data_wrangling(filter_class: str = None):
    print("File exists:", os.path.exists("data/q5.csv"))
    """
    Args:
        - filter_class (str): Optional parameter that specifies the animal class
            to filter the data for.
    """
    with open("data/q5.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        table = list()
        # Feel free to add any additional variables
        ...

        # Read in the header
        for header in reader:
            break

        # Read in each row
        for row in reader:
            # print(row)
            row_data = [row[0], row[1], int(row[2])]
            table.append(row_data)

        print(f"Total rows read from CSV: {len(table)}")

        # Programmatically get unique classes and sort alphabetically for dropdown - [2 point] Q5.4.a
        # dropdown_options = []
        dropdown_options = sorted({row[1] for row in table})

        # Filter, sort, and limit the table - [3 points] Q5.4.b
        # Filter the data by the class column (second column)
        # if filter_class:
        #    ...
        # if filter_class:
        #    table = filter(lambda row: row[1] == filter_class, table)
        #    table = list(table)

        if filter_class:
            filter_class_lower = filter_class.lower()

            filtered_table = [
                row for row in table if row[1].lower() == filter_class_lower
            ]

            table = filtered_table

        def get_count(row):
            return row[2]

        # Order table by the count column (last column) - don't need to worry about tiebreaks
        # table.sort(key=lambda x: x[2], reverse=True)
        # sorted_table = sorted(table, key=get_count, reverse=True)
        table = sorted(table, key=get_count, reverse=True)
        # print("After sorting:", table)
        # ...
        # Take only the first 10 rows
        table = table[:10]
        # ...

    return header, table, dropdown_options
