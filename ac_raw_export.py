# Author: Eric Merlock
# Date: April 21, 2020
# Description: converts raw CSV from animal crossing fandom into usable JSON, adds start and end date Months.

import csv
import json

input_name = input("imported file name:")
export_name = input("exported file name:")

with open(input_name + '.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    new_csv = []
    for row in readCSV:
        new_csv.append(row)

    new_row = new_csv[0] + ["Start Date", "End Date"]

    new_csv[0] = new_csv[0] + ["Start Date", "End Date"]

    for index, row in enumerate(new_csv):
        if row != new_csv[0]:
            i = 5
            start_date = ""
            end_date = ""
            all_months = True
            while i < len(row):
                if row[i - 1] == '-' and row[i] == '?':
                    start_date = new_csv[0][i]
                    all_months = False
                if (i + 1) != len(row):
                    if row[i + 1] == '-' and row[i] == '?':
                        end_date = new_csv[0][i]
                        all_months = False
                i += 1
            if all_months:
                start_date = 'Jan'
                end_date = 'Dec'
            if start_date == '':
                start_date = 'Jan'
            if end_date == '':
                end_date = 'Dec'
            row = row + [start_date, end_date]
            new_csv[index] = row

    new_json = '['

    for index, row in enumerate(new_csv):
        if index != 0:
            new_json += '{ "'
            for i, c in enumerate(row):
                new_json += new_csv[0][i]
                new_json += '": "'
                new_json += c
                if (i + 1) < len(row):
                    new_json += '", "'
                else:
                    new_json += '"'
            new_json += '}'
            if (index + 1) < len(new_csv):
                new_json += ', '

    new_json += ']'

    data = json.loads(new_json)

    with open(export_name + '.json', 'w', encoding='utf-8') as json_write:
        json.dump(data, json_write, ensure_ascii=False, indent=4)

    with open(export_name + '.csv', 'w', newline='') as csv_write:
        writer = csv.writer(csv_write)
        writer.writerows(new_csv)
