#!/usr/bin/env python3
# Libraries
import os
import sys
import getopt
import csv
import pandas as pd


def southAustralia(gender):
  if(os.path.isfile("outputFiles/australia"+gender+".csv")):
    return
  year = 1944
  yearorig = year
  name = []
  years = []
  num = []
  rank = []
  count = 0
  filename2 = "inputFiles/ausFemale.csv"
  
  if(gender == "Male" or "Both"):
    filename = "inputFiles/ausMale.csv"
  if(gender == "Female"):
    filename = "inputFiles/ausFemale.csv"

  with open(filename) as csvDataFile:
    csvReader = csv.reader(csvDataFile, delimiter='	')

    for row in csvReader:

      name.append(row[0])
      num.append(int(row[1]))
      rank.append(int(row[2]))
      years.append(year)
      if (int(row[2]) == 1 and rank[count - 1] != 1):
        year = year + 1

      count = count + 1
    if(gender == "Both"):
      year = yearorig
      with open(filename2) as csvDataFile2:
        csvReader2 = csv.reader(csvDataFile2, delimiter='	')

        for row in csvReader2:
          
          name.append(row[0])
          num.append(int(row[1]))
          rank.append(int(row[2]))
          years.append(year)
        if (int(row[2]) == 1 and rank[count - 1] != 1):
          year = year + 1

          
    people = {'Year': years, 'Name': name, 'Frequency': num, 'Rank': rank}
    people_df = pd.DataFrame(people)
    sorted_people = people_df.sort_values(by=['Year','Frequency'], ascending=[True,False])
    sorted_people.reset_index(drop=True, inplace=True)
    sorted_people['Rank'] = sorted_people.index + 1
    # print(sorted_people)

    outputFile = 'outputFiles/australia' + gender + '.csv'
    sorted_people.to_csv(outputFile, sep=',', index=False, encoding='utf-8')


