#!/usr/bin/env python3

# Libraries
import os
import sys
import getopt
import csv
import pandas as pd


def saskatchewan(gender):
  if(os.path.isfile("outputFiles/saskatchewan"+gender+".csv")):
    return
  

  years = []
  names = []
  numbers = []
  ranks = []
  total = 0

  girl = False
  boy = False

  yearsWomen = []
  namesWomen = []
  numbersWomen = []
  ranksWomen = []

  yearsMen = []
  namesMen = []
  numbersMen = []
  ranksMen = []

  with open("inputFiles/saskatchewan.csv") as csvDataFile:

    next(csvDataFile)
    csvReader = csv.reader(csvDataFile, delimiter=',')
    for row in csvReader:

      #Check if row is not a header
      if (row[0].isdigit()):

        #for both
        years.append(int(row[3]))
        tempName = row[1].strip()
        names.append(tempName)
        numbers.append(int(row[4]))
        total = total + 1
        ranks.append(int(row[0]))

        #for girls
        if (girl == True):

          yearsWomen.append(int(row[3]))
          tempName = row[1].strip()
          namesWomen.append(tempName)
          numbersWomen.append(int(row[4]))
          #totalWomen = totalWomen + 1
          ranksWomen.append(int(row[0]))

        #for boys
        if (boy == True):

          yearsMen.append(int(row[3]))
          tempName = row[1].strip()
          namesMen.append(tempName)
          numbersMen.append(int(row[4]))
          ranksMen.append(int(row[0]))
      #change boolean value to correct gender
      elif (row[1] == 'Baby Girl Names'):
        boy = False
        girl = True

      elif (row[1] == 'Baby Boy Names'):
        boy = True
        girl = False

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
                           ascending=[True, False, True],
                           inplace=True)

      men_df.sort_values(["Year","Frequency", "Name"],
                         axis=0,
                         ascending=[True, False, True],
                         inplace=True)

    rankedPeople_df = people_df.assign(Rank=ranks)

    rankedWomen_df = women_df.assign(Rank=ranksWomen)

    rankedMen_df = men_df.assign(Rank=ranksMen)

    rankedPeople_df.to_csv("outputFiles/saskatchewanBoth.csv",
                           sep=',',
                           index=False,
                           encoding='utf-8')

    rankedWomen_df.to_csv("outputFiles/saskatchewanFemale.csv",
                          sep=',',
                          index=False,
                          encoding='utf-8')

    rankedMen_df.to_csv("outputFiles/saskatchewanMale.csv",
                        sep=',',
                        index=False,
                        encoding='utf-8')

    #print(rankedWomen_df.head(10).to_string(index=False))

    #print(rankedMen_df.head(10).to_string(index=False))
