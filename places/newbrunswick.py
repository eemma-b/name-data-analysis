#!/usr/bin/env python3
import csv
import pandas as pd
import os
def NewBrunswick(filename, outputFilename):
    years = []
    names = []
    frequency = []
    if(os.path.isfile(outputFilename)):
      return

    try:
        with open(filename) as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=',')
            next(csvReader)
            for row in csvReader:
                years.append(int(row[0]))
                names.append(row[1].strip())
                frequency.append(int(row[2]))
    except Exception as error:
        print(f"An error occurred: {error}")

    data = {'Year': years, 'Name': names, 'Frequency': frequency}
    df = pd.DataFrame(data)
    sorted_df = df.sort_values(["Year", "Frequency", "Name"], axis=0, ascending=[True, False, True])

    sorted_df.reset_index(drop=True, inplace=True)
    sorted_df['Rank'] = sorted_df.groupby('Year')['Frequency'].rank(ascending=False, method='min').astype(int)

    sorted_df.to_csv(outputFilename, sep=',', index=False)