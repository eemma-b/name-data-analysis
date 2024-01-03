#!/usr/bin/env python3
import csv
import pandas as pd
import os
# Year Name Frequency Rank

def whichGenderBC(gender): # whichGender function calls the sorting script using the correct file based on user gender input
  if(os.path.isfile("outputFiles/britishColumbia"+gender+".csv")):
    return

  if (gender == 'Female'):
    bcSingleGender('inputFiles/bc-popular-girls-names.csv', gender) # if gender is female call with female csv file
  elif (gender == 'Male'):
    bcSingleGender('inputFiles/bc-popular-boys-names.csv', gender) # else if gender is male call with male csv file
  elif (gender == 'Both'):
    bcBothGenders('inputFiles/bc-popular-girls-names.csv', 'inputFiles/bc-popular-boys-names.csv') # else call with both genders

def bcSingleGender(filename, gender): # funciton def

  names =     [] 
  years =     [] # intialize empty lists
  frequency = []
  ranks =     []

  with open (filename,  encoding = "ISO-8859-1") as csvDataFile: # open csv file 
    csvReader = csv.reader(csvDataFile, delimiter=',') 
    next(csvReader) 

    for row in csvReader: # iterate over rows
      year = 1921
        
      for col in range (1,101): # iterate over columns - 101 columns

        year += 1 # increase year each iteration
        
        years.append(year) # append year, name, and frequency number
        names.append(row[0].title())
        frequency.append(int(row[col].replace(',',''))) # .replace to get rid of commas in large freq numbers
            
  maleFemale = {'Year':years, 'Name':names, 'Frequency':frequency} # sort the list
  genderList_df = pd.DataFrame(maleFemale) # create a dataframe called genderList
  
  genderList_df.sort_values (["Year", "Frequency", "Name"], axis = 0, ascending = [True, False, True], inplace = True) 
  # sort values by ascending year, descending frequency, and alphabetical names

  genderList_df.reset_index (drop=True, inplace=True) # drop index to reset index
  genderList_df['Rank'] = genderList_df.groupby('Year')['Frequency'].rank(ascending = False, method = 'dense').astype(int) 
  # groupby function creates a column 'Rank' which assigns descending rank based on descending frequency and converts to type int -  dense is part of groupby function
  # 'dense' orders the ranks in descending order and does not skip ranks 
  
  #print((f"{genderList_df}")) 
  
  outputFilename = 'outputFiles/britishColumbia'+gender+'.csv' # output the sorted file and include gender in name
  genderList_df.to_csv(outputFilename, sep = ',', index = False, encoding = 'ISO-8859-1')

def bcBothGenders(fileFemale, fileMale):

  names =     [] 
  years =     [] # intialize empty lists
  frequency = []
  ranks =     []

  with open (fileFemale,  encoding = "ISO-8859-1") as csvDataFile: # open csv file 
    csvReader = csv.reader(csvDataFile, delimiter=',') 
    next(csvReader) 

    for row in csvReader: # iterate over rows
      year = 1921
        
      for col in range (1,101): # iterate over columns - 101 columns

        year += 1 # increase year each iteration
        
        years.append(year) # append year, name, and frequency number
        names.append(row[0].title())
        frequency.append(int(row[col].replace(',',''))) # .replace to get rid of commas in large freq numbers

  with open (fileMale,  encoding = "ISO-8859-1") as csvDataFile: # open csv file 
    csvReader = csv.reader(csvDataFile, delimiter=',') 
    next(csvReader) 

    for row in csvReader: # iterate over rows
      year = 1921
        
      for col in range (1,101): # iterate over columns - 101 columns

        year += 1 # increase year each iteration
        
        years.append(year) # append year, name, and frequency number
        names.append(row[0].title())
        frequency.append(int(row[col].replace(',',''))) # .replace to get rid of commas in large freq numbers        
  
  bothGendersList = {'Year':years, 'Name':names, 'Frequency':frequency} # sort the list
  bothGenders_df = pd.DataFrame(bothGendersList) # create a dataframe called genderList
  
  bothGenders_df.sort_values (["Year", "Frequency", "Name"], axis = 0, ascending = [True, False, True], inplace = True) 
  # sort values by ascending year, descending frequency, and alphabetical names
  
  bothGenders_df.reset_index (drop=True, inplace=True) # drop index to reset index
  bothGenders_df['Rank'] = bothGenders_df.groupby('Year')['Frequency'].rank(ascending = False, method = 'dense').astype(int) 
  # groupby function creates a column 'Rank' which assigns descending rank based on descending frequency and converts to type int -  dense is part of groupby function
  # 'dense' orders the ranks in descending order and does not skip ranks 
  
  outputFilename = 'outputFiles/britishColumbiaBoth.csv' # output the sorted file and include gender in name
  bothGenders_df.to_csv(outputFilename, sep = ',', index = False, encoding = 'ISO-8859-1')