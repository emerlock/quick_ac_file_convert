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

            # check to see if a preceding column is false (-) and if the current column is true (?)
            # if above check is true, this is the start date.
            # in AC:NH if a fish or bug is in season, it has a clear range, no spottiness in schedule
            # so likewise, check to see if current column is true (?) and next is false (-)
            # to see if its the end of the date range for the critter
            while i < len(row):
                if row[i - 1] == '-' and row[i] == '?':
                    start_date = new_csv[0][i]
                    all_months = False
                if (i + 1) != len(row):
                    if row[i + 1] == '-' and row[i] == '?':
                        end_date = new_csv[0][i]
                        all_months = False
                i += 1

            # If no months are set, we can assume the critter is year-round
            if all_months:
                start_date = 'Jan'
                end_date = 'Dec'
            # if only one is set, we can assume that it's either Jan or Dec, since the month columns are linear
            if start_date == '':
                start_date = 'Jan'
            if end_date == '':
                end_date = 'Dec'
            row = row + [start_date, end_date]
            new_csv[index] = row

    # start json building
    new_json = '['

    # bunch of terrible bs that is probably way easier to do, but just wanted a quick hack job
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

    # move to json to dump (is this necessary?)
    data = json.loads(new_json)


    # write files based on input file name
    with open(export_name + '.json', 'w', encoding='utf-8') as json_write:
        json.dump(data, json_write, ensure_ascii=False, indent=4)

    with open(export_name + '.csv', 'w', newline='') as csv_write:
        writer = csv.writer(csv_write)
        writer.writerows(new_csv)
