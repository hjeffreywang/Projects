#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np
# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)


# ## Player Count
pcnt= len(purchase_data["SN"].value_counts())
unique_playersdf=purchase_data["SN"].drop_duplicates()

#from google: aggragate all purchase costs based on SN
purchase_data_agg=purchase_data.groupby(purchase_data.SN).agg({'Price':sum,'Age':'first','Gender':'first','Item ID':'first', 'Item Name':'first'})
# * Display the total number of players
# 
print("total number of players is " + str(pcnt))

# In[2]:





# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, total purchase, total revenue.
#

unqitm_array=purchase_data['Item Name'].unique()
prices_array=purchase_data['Price']
purchaseID_count=purchase_data['Purchase ID'].count()
#Other information is put into their own list for calculations later


'''calculation of total, avg price, etc'''
unqitmcnt=unqitm_array.size
avgprice=prices_array.mean()
totalrevenue=prices_array.sum()



# 
# * Create a summary data frame to hold the results
# 
Summaryone=pd.DataFrame({"Number of Unique Items":[unqitmcnt],
                         "Average Price":[avgprice], 
                         "Number of Purchases": [purchaseID_count], 
                         "Total Revenue": [totalrevenue]})

# # 
print(Summaryone)
# In[3]:





# ## Gender Demographics
gender=purchase_data.loc[:,['Gender','Price','SN']]

'''separate the unique SNs only'''
uniqueplayerstotal=gender.nunique()['SN']
uniqueplayergender=gender.drop_duplicates(['SN'])

count_of_genders=uniqueplayergender.groupby('Gender').count()


genderstats=purchase_data.groupby("Gender")



# * Percentage and Count of Male Players
#Originally was running a forward loop of the entire dataframe and counting each gender
 
'''google taught me a more succinct way to count'''
gendercount=uniqueplayergender.pivot_table(index=['Gender'], aggfunc='size')
#convert series to dataframe
gendercountdf=gendercount.to_frame()
#find percentage and put into list
percentgender=gendercountdf[0]/uniqueplayerstotal*100

'''adding, renaming and reforming dataframe'''
gendercountdf['Percentage']=percentgender[:]
'turn column name into string for renaming'
gendercountdf.columns = gendercountdf.columns.astype(str)
gendercountdf=gendercountdf.rename(columns={"0": "Total"})
print(gendercountdf)
# 


# In[4]:





# 
# ## Purchasing Analysis (Gender)

#male/female purchases
malepurchases=gendercountdf.loc['Male'][0]
femalepurchases=gendercountdf.loc['Female'][0]
otherpurchases=gendercountdf.loc['Other / Non-Disclosed'][0]
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# Total purchase money [key== value]
malepurchasetotalseries=purchase_data[purchase_data['Gender']== 'Male']['Price']
femalepurchasetotalseries=purchase_data[purchase_data['Gender']== 'Female']['Price']
otherpurchasetotalseries=purchase_data[purchase_data['Gender']== 'Other / Non-Disclosed']['Price']


malepurchasetotal=malepurchasetotalseries.sum()
femalepurchasetotal=femalepurchasetotalseries.sum()
otherpurchasetotal=otherpurchasetotalseries.sum()
# Averages
malepurchaseaverage=malepurchasetotal/malepurchases
femalepurchaseaverage=femalepurchasetotal/femalepurchases
otherpurchaseaverage=otherpurchasetotal/otherpurchases


# * Create a summary data frame to hold the results
Summarygenderpurchase=pd.DataFrame({"Gender":['Male','Female','Other / Non-Disclosed'],
                                    "Total Purchases":[malepurchases,femalepurchases,otherpurchases], 
                                    "Total Purchase Value ($)": [malepurchasetotal,femalepurchasetotal,otherpurchasetotal], 
                                    "Average Purchase Price": [malepurchaseaverage,femalepurchaseaverage,otherpurchaseaverage]})
Summarygenderpurchase=Summarygenderpurchase.set_index('Gender')

# * Display the summary data frame
print(Summarygenderpurchase)
# In[5]:





# ## Age Demographics

# * Establish bins for ages
# 
agebin=[0,9,  14,  19,  24,  29,  100]
agecateg=['1-10','10-14','15-19','20-24','25-29','>=30']


# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
ageseparateddf=pd.cut(purchase_data_agg['Age'], agebin, labels= agecateg)
age_df=purchase_data_agg
age_df['Age Group'] =ageseparateddf
# 
# * Calculate the numbers and percentages by age group and creating df
# originally forward loop counting each age
agecountseries=age_df.pivot_table(index=['Age Group'], aggfunc='size')
agecountdf=agecountseries.to_frame()
agecountpercent=agecountdf[0]/uniqueplayerstotal*100
agecountdf=agecountdf.rename(columns={"0": "Players in Age Group"})

# * Create a summary data frame to hold the results
# 
agecountdf['Age Group Percentage']=agecountpercent[:]
agecountdf.columns = agecountdf.columns.astype(str)
agecountdf=agecountdf.rename(columns={"0": "Total in Age Group"})
print(agecountdf)
# 

# In[6]:


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
age_total_list=age_df.groupby(["Age Group"]).sum()
age_total_purchase_value=age_total_list.loc[:,'Price']

ageseparateddf2=pd.cut(purchase_data['Age'], agebin, labels= agecateg)
agedf2=purchase_data
agedf2['Age Group'] =ageseparateddf2
agecountseries2=agedf2.pivot_table(index=['Age Group'], aggfunc='size')
agecountdf2=agecountseries2.to_frame()


age_average_purchase=age_total_purchase_value/agecountdf2[0]


age_summary_purchase=pd.DataFrame({"Purchases":agecountdf2[0],
                                  "Total Purchase Value":age_total_purchase_value,
                                  "Average Purchase Value":age_average_purchase})
# 
print(age_summary_purchase)


# In[7]:





# ## Top Spenders
sortedpurchasedata=purchase_data_agg.sort_values("Price", ascending=False)
# 
# * Create a summary data frame to hold the results
sortedpurchasedata=sortedpurchasedata.rename(columns={"Price": "Money Spent"})
#
# 
# * Display a preview of the summary data frame
print(sortedpurchasedata.head(5))

# In[8]:





# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value

#number of purchases
itemgroupby=purchase_data.groupby(["Item ID"]).count()
itemgroupby=itemgroupby.rename(columns={"SN": "Number of Purchases"})
itempurchasecount=itemgroupby.sort_values("Number of Purchases",ascending=False)

#total purchase values
#find total value of purchases by summing price of each ID
itempurchaseagg=purchase_data.groupby(purchase_data['Item ID']).agg({'Item Name':'first',"Item ID":'first','Price':sum,})

#rename to reflect the total
itempurchaseagg=itempurchaseagg.rename(columns={"Price": "Total Purchase Value"})

#set index of dataframe to item ID so it can merge with purchase count
itempurchaseagg=itempurchaseagg.set_index("Item ID")

#add column of original prices
itemprices=purchase_data.groupby(purchase_data['Item ID']).agg({'Price':'first'})
itempurchaseagg["Item Prices"]=itemprices['Price']


#add number of purchases of each item
itempurchaseagg["Number of Purchases"]=itempurchasecount["Number of Purchases"]

# * Sort the purchase count column in descending order
itempurchaseagg=itempurchaseagg.sort_values("Number of Purchases",ascending=False)

# 
# * Display a preview of the summary data frame
print(itempurchaseagg.head(10))
# 

# In[9]:





# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
item_totalvaluesort=itempurchaseagg.sort_values("Total Purchase Value",ascending=False)
print(item_totalvaluesort.head(10))

# 
# 

# In[10]:




