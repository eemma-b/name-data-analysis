#!/usr/bin/env python3
import csv
import numpy as np
import os

def Alberta(filename, outputFilename,gender):
  years = []
  names = []
  frequency = []
  rank = []
  header = []
  if(os.path.isfile("outputFiles/Alberta"+gender+".csv")):
    return

  try:
    with open(filename) as csvDataFile:
      csvReader = csv.reader(csvDataFile, delimiter=',')
      header = next(csvReader)
      for row in csvReader:
        years.append(int(row[0]))
        names.append(row[1].strip())
        frequency.append(int(row[2]))
        rank.append(row[3])
  except Exception as e:
    print(f"An error occurred: {e}")
  
  data = np.column_stack((years, names, frequency, rank))
  np.savetxt(outputFilename, data, delimiter=',', fmt='%s', header=','.join(header), comments='')