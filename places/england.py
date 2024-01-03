import os
import sys
import getopt
import csv
import pandas as pd


def england(gender):
  if(os.path.isfile("outputFiles/england"+gender+".csv")):
    return
  if (gender == 'Female'):
    singleGender('inputFiles/englandGirls.csv', gender)
  elif (gender == 'Male'):
    singleGender('inputFiles/englandBoys.csv', gender)
  elif (gender == 'Both'):
    bothGenders('inputFiles/englandGirls.csv', 'inputFiles/englandBoys.csv')


def singleGender(filename, gender):
  #print("Single Gender")
  years = []
  names = []
  freq = []
  with open(filename) as csvDataFile: #open csv file
    csvReader = csv.reader(csvDataFile, delimiter=',')
    next(csvDataFile)
    for row in csvReader:
      year = 2021
      for col in range(2, 52, 2): #goes through each column of each row
        if (row[col] != '[x]'): #takes into account 0 values
          years.append(int(year))
          freq.append(int(row[col].replace(',', '')))
          names.append(row[0])
        else:
          years.append(int(year))
          freq.append(0)
          names.append(row[0])
        year = year - 1
  people = {'Year': years, 'Name': names, 'Frequency': freq}
  people_df = pd.DataFrame(people) #create a date frame
  sorted_people = people_df.sort_values(by=['Year', 'Frequency', 'Name'],
                                        ascending=[True, False, True]) #sort valeus
  sorted_people.reset_index(drop=True, inplace=True) #fix index
  sorted_people['Rank'] = sorted_people.groupby('Year')['Frequency'].rank(
    ascending=False).astype(int)
  if gender == 'Female':
    outputFilename = 'outputFiles/englandFemale.csv'
  else:
    outputFilename = 'outputFiles/englandMale.csv'

  sorted_people.to_csv(outputFilename, sep=',', index=False, encoding='utf-8')


def bothGenders(fileF, fileM):
  #print("Both Genders")

  limit = input(
    "Due to the large size of the England file, please choose a specific letter (If input is longer than 1, will take the first character): "
  )
  limit = limit[:1]
  check = limit.isalpha() #error checking
  while (check == False):
    limit = input("Invalid Input. Please enter a character: ")
    if (limit.isalpha() == False):
      continue
    else:
      check = True
  limit = limit.upper()

  single = []
  singleFreq = []
  double = []
  doubleFreq = []
  total = 0
  with open(fileF) as femaleFile:  #open female file
    csvReader = csv.reader(femaleFile, delimiter=',')
    next(femaleFile)
    for row in csvReader:
      year = 2021
      for col in range(2, 52, 2):
        if (row[col] != '[x]'):
          if (row[0][0] == limit):
            yearName = str(year) + row[0]
            single.append(yearName)
            singleFreq.append(int(row[col].replace(',', '')))
        else:
          if (row[0][0] == limit):
            yearName = str(year) + row[0]
            single.append(yearName)
            singleFreq.append(0)

        year -= 1
        total += 1
  with open(fileM) as maleFile: #open male file
    csvReader = csv.reader(maleFile, delimiter=',')
    next(maleFile)
    years = []
    names = []
    for row in csvReader:
      year = 2021
      for col in range(2, 52, 2):
        if (row[col] != '[x]'):
          if (row[0][0] == limit):
            yearName = str(year) + row[0]
            if yearName in single:
              years.append(int(year))
              names.append(row[0])
              ind = single.index(yearName)
              doubleFreq.append(
                int(singleFreq[ind]) + int(row[col].replace(',', '')))
          else:
            StopIteration #stops when it reaches next starting letter
        else:
          if (row[0][0] == limit):
            yearName = str(year) + row[0]
            if yearName in single:
              years.append(int(year))
              names.append(row[0])
              ind = single.index(yearName)
              doubleFreq.append(int(singleFreq[ind]))

          else:
            StopIteration

        year -= 1

        #print(year)

  people = {'Year': years, 'Name': names, 'Frequency': doubleFreq}
  people_df = pd.DataFrame(people)
  sorted_people = people_df.sort_values(by=['Year', 'Frequency'],
                                        ascending=[True, False])
  sorted_people.reset_index(drop=True, inplace=True)
  sorted_people['Rank'] = sorted_people.index + 1
  outputFilename = 'outputFiles/englandBoth.csv'
  sorted_people['Rank'] = sorted_people.groupby('Year')['Frequency'].rank(
    ascending=False).astype(int)
  sorted_people.to_csv(outputFilename, sep=',', index=False, encoding='utf-8')
  return outputFilename
