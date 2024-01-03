#!/usr/bin/env python3

# Libraries - importing libraries
import os
import sys
import getopt
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def graphMenu(x, y, xlabel, ylabel, title):

  #Ask user for type of graph
  choiceGraph = input(
      "\nPlease choose what kind of graph you want to print\n1) Line Graph\n2) Bar Graph\n3) Pie Graph\n4) Back to Location Menu\n\nEnter your choice (1-4): "
    )
  print("\n")
  if choiceGraph == '1':

    print("Displaying Line Graph...\n\n")

    lineGraph(x, y, xlabel, ylabel, title)
    print("\n")

    return
  elif choiceGraph == '2':

    print("Displaying Bar Graph...\n\n")
    barGraph(x, y, xlabel, ylabel, title)
    print("\n")

    return
  elif choiceGraph == '3':

    print("Displaying Pie Graph...\n")
    pieGraph(x, y, title)
    print("\n")

    return
  elif choiceGraph == '4':
    return
  else:
    print("Not a Valid Choice!")
    graphMenu(x, y, xlabel, ylabel, title)
    print("\n")
    
def lineGraph(x, y, xlabel, ylabel, title):

  plt.plot(x, y)

  # naming the x axis
  plt.xlabel(xlabel)
  # naming the y axis
  plt.ylabel(ylabel)

  # giving a title to graph
  plt.title(title)

  # function to show the plot
  plt.show()


def pieGraph(x, y, title):

  plt.pie(y, labels=x)
  plt.title(title)

  plt.show()

def barGraph(x, y, xlabel, ylabel, title):

  plt.bar(x, y, color='blue', width=0.4)
  plt.xticks(range(len(x)), x, rotation='vertical')

  plt.xlabel(xlabel)
  plt.xticks()
  plt.ylabel(ylabel)
  plt.title(title)
  plt.show()

def originGraph(c1,p1,c2,p2,c3,p3,c4,p4,c5,p5,name):
  labels = [c1,c2,c3,c4,c5,"Other"]
  sizes =  [p1,p2,p3,p4,p5,100-p1-p2-p3-p4-p5]
  fig, ax = plt.subplots()
  ax.pie(sizes, labels=labels, autopct='%1.1f%%')
  plt.title("Most Common Origin for " + name)
  plt.show()