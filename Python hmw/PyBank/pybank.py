# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 14:04:09 2019

@author: Jeffrey Wang
"""
#import packages
import os
import csv

monthlist=[]
profitlist=[]

csvpath = os.path.join( 'Resources', 'budget_data.csv')

#reading
with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        #print(row) for testing
        '''store data into separate lists that will be used for obtaining values later'''
        monthlist.append(row[0])
        profitlist.append(row[1])
monthlist.pop(0)
profitlist.remove('Profit/Losses')

for i in  range(0, len(profitlist)):
    profitlist[i]=int(profitlist[i])
print("Total profit/loss " + str(sum(profitlist)))  



#---------------------------------------------------------------------
monthlen=len(monthlist)
print("Total Months " + str(monthlen))



#profit/losses
proflosslist=[]
for i in range(1, len(profitlist)):
    proflosslist.append(int(profitlist[i])-int(profitlist[i-1]))
print("Max profit increase is " + str(max(proflosslist)))
print("Largest loss decrease is " + str(min(proflosslist)))


#Average
print("Average Month profit/loss change" + str(sum(proflosslist)/len(proflosslist)))

#-----------------------------------------------------------
#finding the month of max profit and lowest loss

greatest=0
greatestmonth="a"
for i in range(0, len(proflosslist)):
    if greatest <= proflosslist[i]:
        greatest=proflosslist[i]
        greatestmonth=monthlist[i+1]
print("The month of Largest Profit is " +greatestmonth)

least=0
leastmonth="a"
for i in range(0, len(proflosslist)):
    if least >= proflosslist[i]:
        least=proflosslist[i]
        leastmonth=monthlist[i+1]
        
print("The month of Largest Profit is " + leastmonth)
