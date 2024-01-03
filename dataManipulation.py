import os
import sys
import getopt
import csv
import pandas as pd
import requests
import re
from printGraph import graphMenu
from printGraph import originGraph
from places.england import england
from places.california import california
from places.alberta import Alberta
from places.newbrunswick import NewBrunswick
from places.saskatchewan import saskatchewan
from places.novascotia import novascotia
from places.britishcolumbia import whichGenderBC
from places.quebec import whichGenderQU
from places.newfoundland import newfoundland
from places.southAus import southAustralia


def topXinY(filename, n, year):  #returns top x names in year in given file
  names = []
  freq = []
  years = []
  topXfreq = []
  topXname = []
  allYears = []

  with open(filename, 'r', encoding='utf-8',
            errors='ignore') as File:  #open file for year
    csvreader = csv.reader(File, delimiter=',')
    next(File)
    count = int(0)

    for row in csvreader:
      allYears.append(int(row[0]))
    #get the max and min for error checking
    minY = min(allYears)
    maxY = max(allYears)
    while ((int(year) < minY) or (int(year) > maxY)):
      year = input("Invalid Input. Please enter a new value for year [" +
                   str(minY) + "-" + str(maxY) + "]: ")
      while (year.isdigit() is False):
        year = input("Invalid Input. Please enter a new value for year [" +
                     str(minY) + "-" + str(maxY) + "]: ")
    print("\n")

  File.close()

  with open(filename, 'r', encoding='utf-8', errors='ignore') as File: 
    #opens the file to append
    csvreader = csv.reader(File, delimiter=',')
    next(File)
    count = 0

    for row in csvreader:
      if (int(row[0]) == int(year)):

        years.append(row[0])
        names.append(row[1])
        if (row[2].isdigit()):
          freq.append(row[2])
        length = max(names, key=len)
        maxlength = len(length)
        count += 1

    if (int(count) < int(n)):
      print("There were not enough names for that year to give a top " +
            str(n) + " names but here is a list of the top " + str(count) +
            " names.")
      print("Most popular names in " + str(year))
      for i in range(0, int(count)):
        print(f'{i+1:<4} {names[i]:<{maxlength}}{freq[i]}')
        topXfreq.insert(0, freq[i])
        topXname.insert(0, names[i])
    else:
      print("Most popular names in " + str(year))
      for i in range(0, int(n)):
        print(f'{i+1:<4} {years[i]:<7} {names[i]:<{maxlength}}{freq[i]}')
        topXfreq.insert(0, freq[i])
        topXname.insert(0, names[i])

    # for graphing function

    xlabel = 'Names'
    ylabel = 'Frequency'
    title = 'Top ' + str(len(topXfreq)) + ' Names in ' + str(year)

    graphMenu(topXname, topXfreq, xlabel, ylabel, title)  #call graph

  File.close()


def numNamesMaleFemaleYear(filename, year,x):  #returns How many names are in both the female and male names lists in a given year in a given province or country and what are they?

  if (os.path.isfile(filename)):
    if filename.endswith("Both.csv"):
      pass
    else:
      print(
        '\033[91;1m' +
        "\nBoth Gender file must be used! Here are places with data for both genders: "
        + '\033[0m')
      filename = choosePlaceBoth(year)
      return

  allYearsScan = []
  years = []
  names = []
  numbers = []
  ranks = []
  total = 0

  with open(filename, 'r', encoding= 'ISO-8859-1', errors='ignore') as File:  #open file for year
    csvreader = csv.reader(File, delimiter=',')
    next(File)

    for row in csvreader:
      allYearsScan.append(int(row[0]))
    minY = min(allYearsScan)
    maxY = max(allYearsScan)
    if(x == 2):
      year = input("Please enter a year ["+ str(minY) + "-" + str(maxY) + "]: ")
    while (year.isdigit() is False):
        year = input("Invalid Input. Please enter a new value for year [" +str(minY) + "-" + str(maxY) + "]: ")
    while ((int(year) < minY) or (int(year) > maxY)):
      year = input("Invalid Input. Please enter a new value for year [" + str(minY) + "-" + str(maxY) + "]: ")
      

  File.close()

  with open(filename, 'r', encoding='utf-8', errors='ignore') as csvDataFile:
    csvReader = csv.reader(csvDataFile, delimiter=',')
    for row in csvReader:

      if (not row[0].isdigit()):
        continue
      else:
        if int(row[0]) == int(year):
          years.append(int(row[0]))
          names.append(row[1])
          numbers.append(int(row[2]))
          ranks.append(row[3])
          total = total + 1
    print("\nThere are ", total, " names in ", year)
    print("\n")
    if total > 0:
      people = {
        'Year': years,
        'Name': names,
        'Frequency': numbers,
        'Rank': ranks
      }
      people_df = pd.DataFrame(people)

      people_df.sort_values(["Frequency", "Name"],
                            axis=0,
                            ascending=[False, True],
                            inplace=True)
      peopleList = people_df.values.tolist()

      x = []
      y = []

      print("\nYear\tName\t\t     Frequency")
      # ind = 0
      for i in range(len(
          peopleList)):  # print out the name and frequency for the given year
        if (peopleList[i][2] > 19):
          x.append(peopleList[i][1])  #names
          y.append(peopleList[i][2])  #frequency
          print(
            f"{peopleList[i][0]:<4}\t{peopleList[i][1]:<16}\t{peopleList[i][2]:<5}"
          )

      # for graphing function

      xlabel = 'Names'
      ylabel = 'Frequency'
      title = 'Most Popular Names in ' + str(year)
      graphMenu(x[:100], y[:100], xlabel, ylabel, title)


def mostPopularName(filename):
  nameFreq = {}
  with open(filename, 'r', encoding='utf-8', errors='ignore') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for row in csvreader:
      name = row[1]
      freq = row[2]
      if not name or not freq:
        continue
      try:
        freq = int(freq)
      except ValueError:
        continue
      if name in nameFreq:
        nameFreq[name] += freq
      else:
        nameFreq[name] = freq

  if not nameFreq:
    return 'Unknown due to missing frequencies'
  else:
    popularName = max(nameFreq, key=nameFreq.get)
    print("\nThe most popular name is:", '\033[95;1m'+ popularName+ '\033[;0m')
    print("The Frequency of", popularName, "is", nameFreq[popularName], "\n")

def observeName(filename):

  personName = input("\nEnter a name: ").strip().title(
  )  # get user input for the name and use .title() to match case to the csv files

  while not personName.isalpha(
  ):  # check if the user input is the correct datatype
    print(
      "\nInput must be a name."
    )  # if not re-ask the user to input data until its correctly inputted
    personName = input("Enter a name: ").strip().upper()  # ask again

  names = []
  years = []  # intialize empty lists
  frequency = []
  ranks = []
  nameFound = 0

  with open(filename, encoding="ISO-8859-1") as csvDataFile:  # open csv file
    csvReader = csv.reader(csvDataFile, delimiter=',')
    next(csvReader)

    for row in csvReader:  # iterate over rows

      if row[
          1] == personName:  # if the name matches the name in the command line arguement
        nameFound = 1
        years.append(int(row[0]))  # then append all rows
        names.append(row[1])
        frequency.append(int(row[2]))
        ranks.append(row[3])

        people = {
          'Year': years,
          'Name': names,
          'Frequency': frequency,
          'Rank': ranks
        }  # set the dataframe variables
        people_df = pd.DataFrame(people)  # create a dataframe

        people_df.sort_values(
          ["Year", "Frequency", "Name", "Rank"],
          axis=0,
          ascending=[True, False, False, False],
          inplace=True)  # define how these values should be sorted
        peopleList = people_df.values.tolist()

    if (nameFound == False):  # check if the name was found in the csv file
      print(str(personName) + " does not exist")

    else:
      for i in range(len(
          peopleList)):  # print out the year and frequency for the given name
        print(
          (f"{peopleList[i][0]}, {peopleList[i][1]}, {peopleList[i][3]:<0}"))
  print("\n")
  xlabel = 'Names'
  ylabel = 'Frequency'
  title = 'Popularity of '+ personName
  graphMenu(years, frequency, xlabel, ylabel, title) 


def observeLetter(filename):

  personLetter = input(
    "\nEnter a letter: ").strip().upper()  # get user input for a letter

  while not personLetter.isalpha() or len(
      personLetter
  ) != 1:  # check if the user input is the correct datatype and that it is only one char
    print("\nInput must be a single letter."
          )  # ask for user input until it satisfies the conditions
    personLetter = input("Enter a letter: ").strip().upper()

  names = []
  namesTotal = []
  years = []  # intialize empty lists
  frequency = []
  ranks = []
  letterFound = 0
  empId = 0
  nameLen = 15

  with open(filename, encoding="ISO-8859-1") as csvDataFile:  # open csv file
    csvReader = csv.reader(csvDataFile, delimiter=',')
    next(csvReader)

    for row in csvReader:  # iterate over rows

      if row[1][0].upper(
      ) == personLetter:  # if the name matches the name in the command line arguement
        if row[1] not in names:
          letterFound = 1  # keep track there are names starting with the letter

          namesTotal.append(int(
            row[2]))  # create a list that counts total frequency per person

          years.append(int(row[0]))  # then append all rows
          names.append(row[1])
          frequency.append(int(row[2]))
          ranks.append(row[3])

        elif row[1] in names:
          empId = names.index(
            row[1]
          )  # if the name is already in the list and starts with the correct letter - store its frequency in namesTotal
          namesTotal[empId] += int(row[2])
  csvDataFile.close()

  people = {
    'Year': years,
    'Name': names,
    'Total Frequency': namesTotal,
    'Rank': ranks
  }  # set the dataframe variables
  people_df = pd.DataFrame(people)  # convert to dataframe
  people_df.sort_values(
    ["Total Frequency", "Name", "Rank"],
    axis=0,
    ascending=[True, True, False],
    inplace=True)  # define how these values should be sorted
  peopleList = people_df.values.tolist()  # convert values to list
  peopleList.sort(key=lambda x: x[2])
  temp = []
  if (letterFound == 0):  # if letter was not found then let the user know
    print(f"\nNo one has a name starting with the letter {personLetter}")
  else:
    try:
      temp = peopleList[-20:]
      print('\n\033[95;1m'+ "Name\t\t Frequency" +'\033[;0m')
      for n in range(0, 20):
        formatNames = f"{temp[n][1]:<{nameLen}}"
        print(f"{formatNames} {temp[n][2]:<0}") # print out correct values
    except:
      peopleList = peopleList[-len(peopleList):]
      print('\n\033[95;1m'+ "Name\t\t Frequency" +'\033[;0m')
      for l in range(len(peopleList)):
        formatNames = f"{peopleList[l][1]:<{nameLen}}"
        print(f"{formatNames} {peopleList[l][2]:<0}")  # print out correct values

  xlabel = 'Names'  # graphing variables
  ylabel = 'Frequency'
  title = 'Popularity of Names Starting With ' + personLetter  # create accurate title for the graph
  name = list(map(lambda x: x[1], peopleList))
  counts = list(map(lambda y: int(y[2]), peopleList))
  graphMenu(name, counts, xlabel, ylabel, title)


def compareTopTen(inputFileName, inputFileNameTwo, year, loc1, loc2):
  years = []
  names = []

  ranks = []
  total = 0

  years2 = []
  names2 = []

  ranks2 = []
  total2 = 0

  freq   = []
  freq2  = []

  allYears1 = []
  allYears2 = []
  with open(inputFileName, encoding='utf-8', errors='ignore') as csvDataFile: #open file
    csvReader = csv.reader(csvDataFile, delimiter=',')
    next(csvReader)

    for row in csvReader:
      if(int(row[0]) not in allYears1):
        allYears1.append(int(row[0]))
      
      if int(row[0]) == int(year):
        years.append(int(row[0]))
        names.append(row[1])
        freq.append(int(row[2]))

        ranks.append(row[3])
        total = total + 1
  csvDataFile.close()
  
  with open(inputFileNameTwo, encoding='utf-8',
            errors='ignore') as csvDataFile2:
    csvReader2 = csv.reader(csvDataFile2, delimiter=',')
    next(csvReader2)
    for row in csvReader2:
      if(int(row[0])not in allYears2):
        allYears2.append(int(row[0]))
      if int(row[0]) == int(year):        
        years2.append(int(row[0]))
        names2.append(row[1])
        freq2.append(int(row[2]))
        ranks2.append(row[3])
        total2 = total2 + 1
  csvDataFile2.close()
  if ((int(year) not in years) or (int(year) not in years2)):
    minYear = max(min(allYears1), min(allYears2))
    maxYear = min(max(allYears1), max(allYears2))
    year2 = 0
    while ((int(year) > maxYear) or (int(year) < minYear)):
      year2 = input("Invalid year. Please enter a new year [" + str(minYear) +
                    "-" + str(maxYear) + "]:  ")
      print(year2)
      compareTopTen(inputFileName, inputFileNameTwo, year2, loc1, loc2)
      return
      print("\n\n")
      

  #print(f'{i+1:<4} {years[i]:<7} {names[i]:<{maxlength}}{freq[i]}')
  names.insert(0, loc1.title()+" Names")
  names2.insert(0, loc2.title()+" Names")
  maxlength1 = max(names, key=len)
  maxlength1 = len(maxlength1)
  maxlength2 = max(names2, key=len)
  maxlength2 = len(maxlength2)
  if (len(names) > 1):
    for i in range(0, 11):
      if (i == 0):
        print("\n\n" + '\033[95;1m' +
              f'{"    "} {names[0]:<{maxlength1}}   {"  Frequency   "} {names2[0]:<{maxlength2}} {"     Frequency     "}' +'\033[;0m')
      else:
        print(f'{i:<4} {names[i]:<{maxlength1}} {freq[i]:^15} {"  "} {names2[i]:<{maxlength2}} {freq2[i]:^15}')
  else:
    print("Invalid input")
    print("\n")

def origin(name):
  print("\n")
  linkname = 'https://api.nationalize.io/?name=' + name
  res = requests.get(linkname)  #get link
  places = res.json()
  #tries to get a first country for the name if fails then asks for reinput
  try:
    first = places["country"][0]['country_id']
    firstp = round(places["country"][0]['probability'] * 100, 1)
  except:
    print("Sorry name is not in database")
    choice = input(
      "Would you like to try another name? input yes or y for Yes: ")
    if (choice.upper() == 'Y' or choice.upper() == "YES"):
      name = input("Please enter a name: ")
      origin(name)
    return
  try:
    second = places["country"][1]['country_id']
    secondp = round(places["country"][1]['probability'] * 100, 1)
  except:
    print("Sorry name does not have enough data.")
    if (choice.upper() == 'Y' or choice.upper() == "YES"):
      name = input("Please enter a name: ")
      origin(name)
    return
  try:
    third = places["country"][2]['country_id']
    thirdp = round(places["country"][2]['probability'] * 100, 1)
  except:
    print("Sorry name does not have enough data.")
    if (choice.upper() == 'Y' or choice.upper() == "YES"):
      name = input("Please enter a name: ")
      origin(name)
    return
  try:
    fourth = places["country"][3]['country_id']
    fourthp = round(places["country"][3]['probability'] * 100, 1)
  except:
    print("Sorry name does not have enough data.")
    if (choice.upper() == 'Y' or choice.upper() == "YES"):
      name = input("Please enter a name: ")
      origin(name)
    return
  try:
    fifth = places["country"][4]['country_id']
    fifthp = round(places["country"][4]['probability'] * 100, 1)
  except:
    print("Sorry name does not have enough data.")
    if (choice.upper() == 'Y' or choice.upper() == "YES"):
      name = input("Please enter a name: ")
      origin(name)
    return


#finds corresponding countries to the country codes
  with open("outputFiles/countrycodes.csv") as file:
    csvReader = csv.reader(file, delimiter=',')
    for row in csvReader:
      if row[1] == (first):
        full1 = row[0]
      elif row[1] == (second):
        full2 = row[0]
      elif row[1] == (third):
        full3 = row[0]
      elif row[1] == (fourth):
        full4 = row[0]
      elif row[1] == (fifth):
        full5 = row[0]

  try:
    print("The most probable origin is " + full1 + " with a " + str(firstp) +
          "% probability.\nThe second most probable origin is " + full2 +
          " with a " + str(secondp) +
          "% probability.\nThe third most probable origin is " + full3 +
          " with a " + str(thirdp) +
          "% probability.\nThe fourth most probable origin is " + full4 +
          " with a " + str(fourthp) +
          "% probability.\nThe fifth most probable origin is " + full3 +
          " with a " + str(fifthp) + "% probability.")
    print("\n")
  except:
    print("Invalid name")
    return
  y = False
  while y == False:
    x = input("Would you like to view a graph y/n: ")
    if (x.upper() == 'Y' or x.upper() == "YES"):  #graph
      originGraph(full1, firstp, full2, secondp, full3, thirdp, full4, fourthp,
                  full5, fifthp, name)
      y = True
    elif (x.upper() == 'N' or x.upper() == "NO"):
      y = True
    else:
      continue
  print("\n")


def printMenu(filename):
  if ("Female.csv" in filename):
    loc = filename.replace('Female.csv', '')
    gen = "Female"
  elif ("Male.csv" in filename):
    loc = filename.replace('Male.csv', '')
    gen = "Male"
  elif ("Both.csv" in filename):
    loc = filename.replace('Both.csv', '')
    gen = "Both Genders"
  loc = loc.replace('outputFiles/', '')
  loc = re.sub(r"(?<=\w)([A-Z])", r" \1", loc)

  print('\033[95;1m' + "\n\nCurrent File: " + loc.title() +
        "    Current Gender: " + gen + '\033[0m')
  choiceManipulate = input(
    "\n\nPlease choose another option:\n\n1) Find how many names are in both the female and male names lists in a given year in a given province or country\n2) Find top x names for the gender in the province in a given year\n3) Compare two provinces in a given year to find what names they have in common in their top 10s\n4) Find a name to see its rank in various years for the province\n5) Find the all-time most popular male/female name in the province\n6) View the origin of a name\n7) Search a letter to see names starting with this letter and their rank in various years\n8) Back to location menu\n\nEnter your choice: (1-8): "
  )

  if choiceManipulate == '1':
    df = pd.read_csv(filename, encoding='ISO-8859-1')

    #Finding min and max years
    highestYear = df['Year'].max()
    lowestYear = df['Year'].min()

    year = input("Enter a year between: " + str(lowestYear) + " - " +
                 str(highestYear) + ": ")

    if (year.isdigit() is True):
      if (int(year) > highestYear or int(year) < lowestYear):
        print("\nNot in the range of availible years\n")
        while (int(year) > highestYear or int(year) < lowestYear):
          year = input("Enter a year between: " + str(lowestYear) + " - " +
                       str(highestYear) + ": ")
        file = numNamesMaleFemaleYear(filename, int(year),1)
        if (file == 'invalid'):
          return file
        return
      else:
        file = numNamesMaleFemaleYear(filename, int(year),1)
        if (file == 'invalid'):
          return file
        return
    else:
      print("Invalid Input!")
      while(year.isdigit() is False):
        year = input("Enter a year between: " + str(lowestYear) + " - " + str(highestYear) + ": ")
      while (int(year) > highestYear or int(year) < lowestYear):
        year = input("Enter a year between: " + str(lowestYear) + " - " +
                      str(highestYear) + ": ")
      file = numNamesMaleFemaleYear(filename, int(year),1)
      if (file == 'invalid'):
        return file
      return

  elif choiceManipulate == '2':
    df = pd.read_csv(filename, encoding='ISO-8859-1')
    print("\n")
    x = input("Enter x for Top X in Year: ")
    while (x.isdigit() == False):
      x = input("Invalid input. Enter x for Top X in Year: ")
    print("\n")
    #Finding min and max years
    highestYear = df['Year'].max()
    lowestYear = df['Year'].min()
    year = input("Enter a year between: " + str(lowestYear) + " - " +
                 str(highestYear) + ": ")

    if (year.isdigit() is True):
      while((int(year) > highestYear) or (int(year) < lowestYear)):
        print("\nNot in the range of availible years\n")
        year = input("Enter a year between: " + str(lowestYear) + " - " + str(highestYear) + ": ")
    else:
      while(year.isdigit() is False):
            year = input("Enter a year between: " + str(lowestYear) + " - " +
                        str(highestYear) + ": ")
      while((int(year) > highestYear) or (int(year) < lowestYear)):
        print("\nNot in the range of availible years\n")
        year = input("Enter a year between: " + str(lowestYear) + " - " + str(highestYear) + ": ")
    topXinY(filename, x, int(year))
    return
  elif choiceManipulate == '3':
    if ("Female.csv" in filename):
      loc1 = filename.replace('Female.csv', '')
    elif ("Male.csv" in filename):
      loc1 = filename.replace('Male.csv', '')
    elif ("Both.csv" in filename):
      loc1 = filename.replace('Both.csv', '')

    loc1 = loc1.replace('outputFiles/', '')
    loc1 = re.sub(r"(?<=\w)([A-Z])", r" \1", loc1)

    filename2 = 'done'
    while (filename2 == 'done' or filename2 == 'invalid'):
      print('\033[95;1m'+"\n-----Enter a location to compare to " + loc1.title() + "-----"+'\033[;0m')
      print(
        "**Note inputting 11 or an Invalid character will result in the function being called again**\n\n"
      )
      filename2 = choosePlace()

    if ("Female.csv" in filename2):
      loc2 = filename2.replace('Female.csv', '')
    elif ("Male.csv" in filename2):
      loc2 = filename2.replace('Male.csv', '')
    elif ("Both.csv" in filename2):
      loc2 = filename2.replace('Both.csv', '')
    else:
      return
    loc2 = loc2.replace('outputFiles/', '')
    loc2 = re.sub(r"(?<=\w)([A-Z])", r" \1", loc2)
    y = input("\nEnter the year you would like to view: ")
    print("Comparing " + loc1.title() + " to " + loc2.title() +
          " in the year " + y)

    compareTopTen(filename, filename2, y, loc1, loc2)

    return
  elif choiceManipulate == '4':
    observeName(filename)
    return
  elif choiceManipulate == '5':
    mostPopularName(filename)
    return
  elif choiceManipulate == '6':
    name = input("Enter a name to find its origin: ")
    origin(name)
    return
  elif choiceManipulate == '7':
    observeLetter(filename)
    return

  elif choiceManipulate == '8':

    return
  else:
    print("Invalid choice!")
    printMenu(filename)


def choosePlace():

  print("\nWhich province would you like to look at?\n")

  print(
    "1. British Columbia \n2. Alberta\n3. Saskatchewan\n4. Quebec\n5. New Brunswick \n6. Nova Scotia\n7. Newfoundland\n\nExtras:\n\n8. California\n9. England\n10. South Australia\n11. Exit\n"
  )  # print out a menu that consists of all places

  print("Inputting anything else will ask for input again\n"
        )  # ask for user input for which place they would like to look at
  choice = input("What Place Would You Like to Look At: ")

  if choice == '1':

    print("\n")
    print(
      '\033[95;1m' + "----British Columbia----" + '\033[0m'
    )  # print out province name and the gender options and allow user to quit
    choice = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) View Both Gender Names\n4) Back to Location Menu\n\nEnter your choice: (1-4): "
    )  # take user input
    #choice.isdigit()
    if choice == '1':
      whichGenderBC(
        "Female"
      )  # call whichGender function which calls the file script  the correct
      return 'outputFiles/britishColumbiaFemale.csv'
    elif choice == '2':
      whichGenderBC("Male")
      return 'outputFiles/britishColumbiaMale.csv'

    elif choice == '3':
      whichGenderBC("Both")
      return 'outputFiles/britishColumbiaBoth.csv'

    elif choice == '4':

      return choosePlace()

    else:
      print("Not a valid choice!")
      return choosePlace()

  elif choice == '2':

    print("\n")
    print('\033[95;1m' + "----Alberta----" + '\033[0m')
    choice = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) View Both Gender Names\n4) Back to Location Menu\n\nEnter your choice: (1-4): "
    )
    if choice == '1':
      Alberta("inputFiles/AlbertaFemale.csv", "outputFiles/albertaFemale.csv",
              "Female")
      return ("outputFiles/albertaFemale.csv")

    elif choice == '2':
      Alberta("inputFiles/AlbertaMale.csv", "outputFiles/albertaMale.csv",
              "Male")
      return ("outputFiles/albertaMale.csv")

    elif choice == '3':
      Alberta("inputFiles/AlbertaBothGenders.csv", "outputFiles/albertaBoth.csv",
              "Both")
      return ("outputFiles/albertaBoth.csv")

    elif choice == '4':
      return choosePlace()
    else:
      print("Not a valid choice!")
      return choosePlace()

  elif choice == '3':

    print("\n")
    print('\033[95;1m' + "----Saskatchewan----" + '\033[0m')
    choice = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) View Both Gender Names\n4) Back to Location Menu\n\nEnter your choice: (1-4):"
    )
    if (choice.isdigit()):

      if choice == '1':
        saskatchewan("Female")
        return ('outputFiles/saskatchewanFemale.csv')

      elif choice == '2':
        saskatchewan("Male")
        return ('outputFiles/saskatchewanMale.csv')

      elif choice == '3':
        saskatchewan("Both")
        return ('outputFiles/saskatchewanBoth.csv')

      elif choice == '4':
        return choosePlace()
      else:
        print("Not a valid choice!\n")
        choosePlace()

    else:
      print("Not a valid choice!\n")
      return choosePlace()

  elif choice == '4':

    print("\n")
    print('\033[95;1m' + "----Quebec----" + '\033[0m')
    choice = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) View Both Gender Names\n4) Back to Location Menu\n\nEnter your choice: (1-4): "
    )
    if choice == '1':
      whichGenderQU("Female")
      return ('outputFiles/quebecFemale.csv')

    elif choice == '2':
      whichGenderQU("Male")
      return ('outputFiles/quebecMale.csv')

    elif choice == '3':
      whichGenderQU("Both")
      return ('outputFiles/quebecBoth.csv')

    elif choice == '4':
      return choosePlace()
    else:
      print("Not a valid choice!")
      return choosePlace()

  elif choice == '5':

    print("\n")
    print('\033[95;1m' + "----New Brunswick----" + '\033[0m')
    choice = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) View Both Gender Names\n4) Back to Location Menu\n\nEnter your choice: (1-4): "
    )
    if choice == '1':
      NewBrunswick('inputFiles/NewBrunswickFemale.csv',
                   'outputFiles/newBrunswickFemale.csv')
      return ('outputFiles/newBrunswickFemale.csv')

    elif choice == '2':
      NewBrunswick('inputFiles/NewBrunswickMale.csv',
                   'outputFiles/newBrunswickMale.csv')
      return ('outputFiles/newBrunswickMale.csv')

    elif choice == '3':
      NewBrunswick('inputFiles/NewBrunswickBoth.csv',
                   'outputFiles/newBrunswickBoth.csv')
      return ('outputFiles/newBrunswickBoth.csv')

    elif choice == '4':
      return choosePlace()
    else:
      print("Not a valid choice!\n")
      return choosePlace()

  elif choice == '6':

    print("\n")
    print('\033[95;1m' + "----Nova Scotia----" + '\033[0m')
    choice = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) View Both Gender Names\n4) Back to Location Menu\n\nEnter your choice: (1-4): "
    )

    if choice == '1':
      novascotia("Female")
      return ('outputFiles/novaScotiaFemale.csv')

    elif choice == '2':
      novascotia("Male")
      return ('outputFiles/novaScotiaMale.csv')

    elif choice == '3':
      novascotia("Both")
      return ('outputFiles/novaScotiaBoth.csv')

    elif choice == '4':
      return choosePlace()
    else:
      print("Not a valid choice!\n")
      return choosePlace()

  elif choice == '7':

    print("\n")
    print('\033[95;1m' + "----Newfoundland----" + '\033[0m')
    print(
      '\033[95m' +
      " Warning the Newfoundland File did not have frequencies and can only be used for the compare top ten function. Selecting a gender will result in the compare top ten function being called."
      + '\033[0m')
    selection = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) View Both Gender Names\n4) Back to Location Menu\n\nEnter your choice: (1-4): "
    )
    if selection == '1':
      newfoundland("Female")
      return ('outputFiles/newfoundlandFemale.csv')

    elif selection == '2':
      newfoundland("Male")
      return ('outputFiles/newfoundlandMale.csv')

    elif selection == '3':
      newfoundland("Both")
      return ('outputFiles/newfoundlandBoth.csv')

    elif selection == '4':
      return choosePlace()
    else:
      print("Not a valid choice!\n")
      return choosePlace()

  elif choice == '8':

    print("\n")
    print('\033[95;1m' + "----California----" + '\033[0m')
    choice = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) Back to Location Menu\n\nEnter your choice: (1-3): "
    )
    if choice == '1':
      california("inputFiles/california.csv", "Female")
      return ("outputFiles/californiaFemale.csv")

    elif choice == '2':
      california("inputFiles/california.csv", "Male")
      return ("outputFiles/californiaMale.csv")

    elif choice == '3':
      return choosePlace()
    else:
      print("Not a valid choice!\n")
      return choosePlace()

  elif choice == '9':

    print("\n")
    print('\033[95;1m' + "----England----" + '\033[0m')
    choice = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) View Both Gender Names\n4) Back to Location Menu\n\nEnter your choice: (1-4): "
    )
    if choice == '1':
      england("Female")
      return ("outputFiles/englandFemale.csv")

    elif choice == '2':
      england("Male")
      return ("outputFiles/englandMale.csv")

    elif choice == '3':
      england("Both")
      return ("outputFiles/englandBoth.csv")

    elif choice == '4':
      return choosePlace()
    else:
      print("Not a valid choice!\n")
      return choosePlace()

  elif choice == '10':

    print("\n")
    print('\033[95;1m' + "----South Australia----" + '\033[0m')
    selection = input(
      "\nPlease choose an option:\n\n1) View Female Names\n2) View Male Names\n3) View Both Gender Names\n4) Back to Location Menu\n\nEnter your choice: (1-4): "
    )
    if selection == '1':
      southAustralia("Female")
      return ("outputFiles/australiaFemale.csv")

    elif selection == '2':
      southAustralia("Male")
      return ("outputFiles/australiaMale.csv")

    elif selection == '3':
      southAustralia("Both")
      return ("outputFiles/australiaBoth.csv")
    
    elif selection == '4':
      return choosePlace()
    else:
      print("Not a valid choice!\n")
      return choosePlace()

  elif choice == '11':
    return 'done'

  else:
    print("\nNot a Valid Choice!")
    return 'invalid'


def choosePlaceBoth(year):

  print("\nWhich province would you like to look at?")

  print(
    "1. British Columbia \n2. Alberta\n3. Saskatchewan\n4. Quebec\n5. New Brunswick \n6. Nova Scotia\n\nExtras:\n\n7. England\n8. South Australia\n"
  )  # print out a menu that consists of all places

  print("Inputting anything else will ask for input again\n"
        )  # ask for user input for which place they would like to look at
  choice = input("What Place Would You Like to Look At: ")

  if choice == '1':

    whichGenderBC("Both")
    numNamesMaleFemaleYear('outputFiles/britishColumbiaBoth.csv', year,2)
    
  elif choice == '2':

    Alberta("inputFiles/AlbertaBothGenders.csv", "outputFiles/albertaBoth.csv",
            "Both")
    numNamesMaleFemaleYear("outputFiles/albertaBoth.csv", year,2)

  elif choice == '3':

    saskatchewan("Both")
    numNamesMaleFemaleYear('outputFiles/saskatchewanBoth.csv', year,2)

  elif choice == '4':

    whichGenderQU("Both")
    numNamesMaleFemaleYear('outputFiles/quebecBoth.csv', year,2)

  elif choice == '5':

    NewBrunswick('inputFiles/NewBrunswickBothGenders.csv',
                 'outputFiles/newBrunswickBoth.csv')
    numNamesMaleFemaleYear('outputFiles/newBrunswickBoth.csv', year,2)

  elif choice == '6':

    novascotia("Both")
    numNamesMaleFemaleYear("outputFiles/novaScotiaBoth.csv", year,2)

  elif choice == '7':

    england("Both")
    numNamesMaleFemaleYear("outputFiles/englandBoth.csv", year,2);

  elif choice == '8':

    southAustralia("Both")
    numNamesMaleFemaleYear("outputFiles/australiaBoth.csv", year,2)

  else:
    print('\033[91;1m' + "\nNot a Valid Choice!" + '\033[0m\n')
    choosePlaceBoth(year)
    return


#https://stackoverflow.com/questions/8924173/how-can-i-print-bold-text-in-python
