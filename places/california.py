import csv
import pandas as pd
import os

def california(filename, gender):
  names = []
  years = []
  count = []
  ranks = []
  total = 0
  if (gender != 'Both'):
    if(os.path.isfile("outputFiles/california"+gender+".csv")):
      return

    with open(filename) as csvDataFile:
      csvReader = csv.reader(csvDataFile, delimiter=',')
      for row in csvReader:
        if (row[1] == gender):
          years.append(row[0])
          ranks.append(-1)
          names.append(row[3].title())
          count.append(int(row[4]))
          total = total + 1
    people = {'Year': years, 'Name': names, 'Frequency': count, 'Rank': ranks}
    people_df = pd.DataFrame(people)
    sorted_people = people_df.sort_values(by=['Year','Frequency'], ascending=[True,False])
    sorted_people.reset_index(drop=True, inplace=True)
    sorted_people['Rank'] = sorted_people.groupby('Year')['Frequency'].rank(ascending = False, method = 'dense').astype(int) 
    #print(sorted_people)
    if gender == 'Female':
      outputFilename = 'outputFiles/californiaFemale.csv'
    else:
      outputFilename = 'outputFiles/californiaMale.csv'
    sorted_people.to_csv(outputFilename,
                         sep=',',
                         index=False,
                         encoding='utf-8')
  else:
    print("There are no common names between both genders for California")
    # single = []
    # singleFreq = []
    # double = []
    # doubleFreq = []
    # with open(filename) as csvDataFile:
    #     csvReader = csv.reader(csvDataFile,delimiter=',')
    #     next(csvReader)
    #     for row in csvReader:
    #         yearName = str(row[0])+row[3].title()
    #         if single.count(yearName) == 0:
    #             single.append(yearName)
    #             singleFreq.append(int(row[4]))
    #         else:
    #             ind = single.index(yearName)
    #             double.append(yearName)
    #             doubleFreq.append(int(row[4])+singleFreq[ind])
    # print(double)
    # print(doubleFreq)
