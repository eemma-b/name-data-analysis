#!/usr/bin/env python3
# Libraries
import os
import sys
import getopt
import csv
import pandas as pd


def newfoundland(gender):
  year = 2003
  rank = []
  years = []
  num = []
  names = []
  genders = []
  if(os.path.isfile("outputFiles/newfoundland"+gender+".csv")):
    return

  if(gender != "Both"):
    with open("inputFiles/Newfoundland.csv") as csvDataFile:
      csvReader = csv.reader(csvDataFile, delimiter=',')

      for row in csvReader:
        if (gender == 'Male'):
          names.append(row[0].title())
        rank.append(int(row[1]))
        if (gender == 'Female'):
          names.append(row[2].title())
        years.append(year)
        num.append('not given')
        if (int(row[1]) == 100):
          year = year + 1

  if(gender == "Both"):
    with open("inputFiles/Newfoundland.csv") as csvDataFile:
      csvReader = csv.reader(csvDataFile, delimiter=',')
  
      for row in csvReader:
        names.append(row[0].title())
        rank.append(int(row[1]))
        years.append(year)
        genders.append('boy')
        num.append('not given')
        names.append(row[2].title())
        rank.append(int(row[1]))
        years.append(year)
        genders.append('girl')
        num.append('not given')
        if (int(row[1]) == 100):
          year = year + 1
  if(gender != "both"): 
      people = {'Year': years, 'Name': names, 'Frequency': num, 'Rank': rank}
  else:
      people = {'Year': years, 'Name': names, 'Frequency': num, 'Rank': rank, 'Gender': genders}
  people_df = pd.DataFrame(people)
  sorted_people = people_df.sort_values(by=['Year','Rank'], ascending=[True,True])
  sorted_people.reset_index(drop=True, inplace=True)
   
  # print(sorted_people)

  outputFile = 'outputFiles/newfoundland'+gender+'.csv'
  sorted_people.to_csv(outputFile, sep=',', index=False, encoding='utf-8')



