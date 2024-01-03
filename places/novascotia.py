#!/usr/bin/env python3

# Libraries
import os
import sys
import getopt
import csv
import pandas as pd


def novascotia(gender):

  years = []
  names = []
  numbers = []
  ranks = []
  total = 0

  yearsWomen = []
  namesWomen = []
  numbersWomen = []
  ranksWomen = []
  totalWomen = 0

  yearsMen = []
  namesMen = []
  numbersMen = []
  ranksMen = []
  totalMen = 0
  if(os.path.isfile("outputFiles/novaScotia"+gender+".csv")):
    return
  with open("inputFiles/NovaScotiaBabyNames.csv") as csvDataFile:

    next(csvDataFile)
    csvReader = csv.reader(csvDataFile, delimiter=',')
    for row in csvReader:

      #for both
      years.append(int(row[0]))
      tempName = row[2].strip()
      names.append(tempName.title())
      numbers.append(int(row[3]))
      total = total + 1
      ranks.append(total)

      #for woman
      if (row[1] == 'F'):
        #print(row)
        yearsWomen.append(int(row[0]))
        tempName = row[2].strip()
        namesWomen.append(tempName.title())
        numbersWomen.append(int(row[3]))
        totalWomen = totalWomen + 1
        ranksWomen.append(totalWomen)

      #for men
      if (row[1] == 'M'):
        #print(row)
        yearsMen.append(int(row[0]))
        tempName = row[2].strip()
        namesMen.append(tempName.title())
        numbersMen.append(int(row[3]))
        totalMen = totalMen + 1
        ranksMen.append(totalMen)

    if total > 0:
      people = {
        'Year': years,
        'Name': names,
        'Frequency': numbers,
        'Rank': ranks,
      }

      women = {
        'Year': yearsWomen,
        'Name': namesWomen,
        'Frequency': numbersWomen,
        'Rank': ranksWomen,
      }

      men = {
        'Year': yearsMen,
        'Name': namesMen,
        'Frequency': numbersMen,
        'Rank': ranksMen,
      }

      people_df = pd.DataFrame(people)

      women_df = pd.DataFrame(women)

      men_df = pd.DataFrame(men)

      people_df.sort_values(["Year","Frequency", "Name"],
                            axis=0,
                            ascending=[True,False, True],
                            inplace=True)

      women_df.sort_values(["Year","Frequency", "Name"],
                            axis=0,
                            ascending=[True,False, True],
                            inplace=True)

      men_df.sort_values(["Year","Frequency", "Name"],
                            axis=0,
                            ascending=[True,False, True],
                            inplace=True)

    rankedPeople_df = people_df.assign(Rank=ranks)

    rankedWomen_df = women_df.assign(Rank=ranksWomen)

    rankedMen_df = men_df.assign(Rank=ranksMen)

    rankedPeople_df.to_csv("outputFiles/novaScotiaBothGenders.csv",
                           sep=',',
                           index=False,
                           encoding='utf-8')

    rankedWomen_df.to_csv("outputFiles/novaScotiaFemale.csv",
                          sep=',',
                          index=False,
                          encoding='utf-8')

    rankedMen_df.to_csv("outputFiles/novaScotiaMale.csv",
                        sep=',',
                        index=False,
                        encoding='utf-8')

    #print(rankedWomen_df.head(10).to_string(index=False))

   #print(rankedMen_df.head(10).to_string(index=False))
