#!/usr/bin/env python3

# Libraries - importing libraries
import os 
import sys
import getopt 
import csv 
import pandas as pd
import numpy as np
import re

#importing from files
from dataManipulation import choosePlace
from dataManipulation import printMenu
from dataManipulation import compareTopTen


# menu of files that will allow the user to pick which files to read
# menu that will ask for the specific gender, both or exit
# menu of different functions - different options for both 

def main(argv):
  print('\033[95;7m'+"----------Welcome to Dragonfly Name Analysis----------\n"+'\033[0m')
  filename = ''
  while(filename !=  'done'):
    filename = choosePlace()
    while((filename == 'invalid')  or (filename == 'back')):
      filename = choosePlace()
    if (filename != 'done'):
      if "newfoundland" in filename:
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
          print('\033[95m'+"\n-----Enter a location to compare to " + loc1.title() + "-----" + '\033[0m')
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
      else:
        printMenu(filename)
  print('\033[95;1m'+"Thank you for using Dragonfly Data Analysis"+'\033[0m')
  

if __name__ == "__main__":
  main(sys.argv[1:])