import numpy as np
import pandas as pd
import wbdata
import matplotlib.pyplot as plt
import HIVstats
import plotly.graph_objects as go
import scipy.stats as stats
#The usual suspects
np.set_printoptions(suppress=True)



#Note that wbdata requires 'pip install wbdata' before running. It's a separate plugin for WorldBank's data, which allows
# a smooth pass from their servers into a Pandas dataframe. Also installing plotly if it's not there.


countries = list(HIVstats.alpha3codedict.values())
df = wbdata.get_dataframe(indicators,country=countries)
#Wb data lets me get pandas dataframes directly from a source. Hopefully I'll be able to front-end the country tags.

#Unfortunately, there was no clear dictionary with these values. I've decided to create them manually for only the countries that
# don't have No Data values in both my dependent variables, TherapyPercentage2018 and TherapyNumber2018



df.info()
df.head()
df.describe()
#The even more usual suspects
df.loc(axis=0)[:,'2018'].loc(axis=1)['Literacy Rate']
#Testing whether or not I can locate data by both multi-index and column. Definitely can.

df1 = pd.read_csv("data/data.csv") # http://apps.who.int/gho/data/view.main.23300?lang=en
df3 = pd.read_csv("data/data-2.csv")
df4 = pd.read_csv("data/data-3.csv") # http://apps.who.int/gho/data/view.main.RSUD620v
df5 = pd.DataFrame(list(HIVstats.PepfarOps.items()))
# To be renamed appropriately later

df1.info()
df1.columns = ['Country','TherapyPercentage2018','TherapyNumber2018','HIV2018','HIV2010','HIV2005','HIV2000']
df2 = df1.loc[(df1['TherapyPercentage2018']!='No data')| (df1['TherapyNumber2018']!='No data')]
df2.drop(0,inplace=True) #Normally I'd reset the index here, 
# but in this case, I'm going to be completely changing the structure later
df2.replace('No data',np.nan,inplace=True)
splitcol = df2.TherapyPercentage2018.str.split(' \[',expand=True)
splitcol.columns=['TherapyPercentage2018avg','TherapyPercentageRange']
df2=df2.join(splitcol)

splitcol2 = df2.HIV2018.str.split(' \[',expand=True)
splitcol3 = df2.HIV2010.str.split(' \[',expand=True)
splitcol4 = df2.HIV2005.str.split(' \[',expand=True)
splitcol5 = df2.HIV2000.str.split(' \[',expand=True)
splitcol2.columns=['HIV2018avg','HIV2018range']
splitcol3.columns=['HIV2010avg','HIV2010range']
splitcol4.columns=['HIV2005avg','HIV2005range']
splitcol5.columns=['HIV2000avg','HIV2000range']
df2=df2.join(splitcol2).join(splitcol3).join(splitcol4).join(splitcol5)

df2['TherapyPercentage2018avg'] = df2.TherapyPercentage2018avg.str.replace(" ","")
df2['HIV2018avg']=df2.HIV2018avg.str.replace(" ","")
df2['HIV2018avg']=df2.HIV2018avg.str.replace("<","")
df2['HIV2010avg']=df2.HIV2010avg.str.replace(" ","")
df2['HIV2010avg']=df2.HIV2010avg.str.replace("<","")
df2['HIV2005avg']=df2.HIV2005avg.str.replace(" ","")
df2['HIV2005avg']=df2.HIV2005avg.str.replace("<","")
df2['HIV2000avg']=df2.HIV2000avg.str.replace(" ","")
df2['HIV2000avg']=df2.HIV2000avg.str.replace("<","")
df2['TherapyNumber2018']=df2.TherapyNumber2018.str.replace(" ","")
#This is all just splitting columns, replacing non-number symbols, and renaming columns.

df2 = df2.astype({'TherapyPercentage2018avg':float,
                  'TherapyNumber2018':float,
                  'HIV2018avg':float,
                  'HIV2010avg':float,
                  'HIV2005avg':float,
                  'HIV2000avg':float})
df2.set_index('Country',inplace=True) #Because the countries are the index of the Worldbank dataframe

#All Data Cleaning above! Just making sure all of the columns are floats and have NaN instead of No Data and have no weird 
#symbols in there.

df2.drop(['TherapyPercentage2018','HIV2018','HIV2010','HIV2005','HIV2000'],axis=1,inplace=True)
df2.head() #Just to make sure it looks nice

#Further cleaning, because I want all this to match the Worldbank data!
df220 = df2[['HIV2018avg','HIV2010avg','HIV2005avg','HIV2000avg']] #This is breaking it up into two tables so one can be stacked.

index221 = [(x,'2018') for x in df2.index]
index221 = pd.MultiIndex.from_tuples(index221,names=['country','date'])
df221 = pd.DataFrame({'TherapyNumber2018':df2['TherapyNumber2018'].to_list(),
                      'TherapyPercentage2018avg':df2['TherapyPercentage2018avg'].to_list()},
                     mulindex221) #This dataframe was very particular about being reconstructed.

df221.index = [df221.index.get_level_values(0),df221.index.get_level_values(1).astype(str)] 
#The multiindices are very stubborn about being int instead of object. They have to be forcibly changed.
df220.columns=['2018','2010','2005','2000']
df220 = df220.stack().to_frame()
df220.index = [df220.index.get_level_values(0).rename('country'),df220.index.get_level_values(1).rename('date')]
#Likewise, they hate being renamed, except by force.
df220.columns=['Average HIV patients'] #Two separate column settings are required just because we needed to rename earlier.


df220 = df220.join(df221,on=['country','date'])
#And then join them back together, with NaN values for all dates that aren't 2018.



df33 = df3[df3['Year']==2013]
#Moving on to data set 2, and making sure it shows only hospitals in a year.

df33.set_index('Country',inplace=True)
index331 = [(x,'2018') for x in df33.index]
index331 = pd.MultiIndex.from_tuples(index331,names=['country','date'])
df33.columns=['Year',
              'Total Density/100k: Health Posts',
              'Total Density/100k: Health Centers',
              'Total Density/100k: Rural Hospitals',
              'Total Density/100k: Provincial Hospitals',
              'Total Density/100k: Specialized Hospitals',
              'Total Density/100k: Total Hospitals']
df331 = pd.DataFrame({'Total Density/100k: Health Posts 2013':df33['Total Density/100k: Health Posts'].to_list(),
                      'Total Density/100k: Health Centers 2013':df33['Total Density/100k: Health Centers'].to_list(),
                      'Total Density/100k: Rural Hospitals 2013':df33['Total Density/100k: Rural Hospitals'].to_list(),
                      'Total Density/100k: Provincial Hospitals 2013':df33['Total Density/100k: Provincial Hospitals'].to_list(),
                      'Total Density/100k: Specialized Hospitals 2013':df33['Total Density/100k: Specialized Hospitals'].to_list(),
                      'Total Density/100k: Total Hospitals 2013':df33['Total Density/100k: Total Hospitals'].to_list()},index331)
df331.index = [df331.index.get_level_values(0),df331.index.get_level_values(1).astype(str)]
#Preparing this in the same way df220 and 221 were prepared

df4.columns = ['Country','HIV (ARV) treatment 2014 in specialized facilities and services',
               'HEPATITIS treatment 2014 in specialized facilities and services',
               'HIV testing and councelling 2014 in specialized facilities and services',
               'Hepatitis testing and councelling 2014 in specialized facilities and services',
               'Hepatitis Vaccination 2014 in specialized facilities and services']
df44 = df4.drop([0,1])

df44.set_index('Country',inplace=True)
index440 = [(x,'2018') for x in df44.index]
index440 = pd.MultiIndex.from_tuples(index440,names=['country','date'])
df44.columns=['ARVtreatment',
              'HEPtreatment',
              'HIVtest',
              'HEPtest',
              'HEPvaccine']
df440 = pd.DataFrame({'HIV (ARV) treatment 2014 in specialized facilities and services':df44['ARVtreatment'].to_list(),
                      'HEPATITIS treatment 2014 in specialized facilities and services':df44['HEPtreatment'].to_list(),
                      'HIV testing and councelling 2014 in specialized facilities and services':df44['HIVtest'].to_list(),
                      'Hepatitis testing and councelling 2014 in specialized facilities and services':df44['HEPtest'].to_list(),
                      'Hepatitis Vaccination 2014 in specialized facilities and services':df44['HEPvaccine'].to_list()}
                      ,index440)
df440.index = [df440.index.get_level_values(0),df440.index.get_level_values(1).astype(str)]

#Effectively equivalent of what was done with df33 above.

df5.set_index(0,inplace=True)
index550 = [(x,'2018') for x in df5.index]
index550 = pd.MultiIndex.from_tuples(index550,names=['country','date'])

#Further Data Cleaning, this time with the WorldBank data all in one
dfcountrydata = df #to make sure I don't overwrite the dataframe
dfcountrydata.update(df.groupby(level=0).bfill())
'''
        This above one is particularly dangerous, but I decided I really had no choice. This short command updates all of our
        new dataframe's data using the previous data, grouped by the Country-level index.
        Ultimately, the data will all be effectively 3-dimensional. There's Country as one dimension, Year as another, and the
        column values as each 'third' dimension.

        The issue with the above command is that if we only have data for, say, 1993, and then 2015, then all of the data from 2000,
        2005, and 2010 will be the 1993 data. Likewise, if we have only 1960's data, then that data is assumed for all the data upwards.
        Some data is entirely missing before some date after 2000, so we have nonexistent datapoints there.

        I anticipate that my data will just have to be inaccurate in the meantime. It will just have to be so.
'''
dfcountrydata.loc(axis=0)[:,('2018','2010','2005','2000')].head(52)
#This is just viewing the specific data here and there.

df230 = df220.join(df331, on=['country','date'])
#df234 = df230.join(df440, on=['country','date'])
dfHIVfull = dfcountrydata.loc(axis=0)[:,('2018','2010','2005','2000')].join(df230, on=['country','date'])
#Combining all of the current data into one table. Note that I'm combining 2013 and 2014 data with 2018 data, but
# I've chosen to treat those data as the most current.


dfHIVfull.loc(axis=0)[:,'2018']=dfHIVfull.loc(axis=0)[:,'2018'].fillna({'HIV (ARV) treatment 2014 in specialized facilities and services':'No Data',
                                        'HEPATITIS treatment 2014 in specialized facilities and services':'No Data',
                                        'HIV testing and councelling 2014 in specialized facilities and services':'No Data',
                                        'Hepatitis testing and councelling 2014 in specialized facilities and services':'No Data',
                                        'Hepatitis Vaccination 2014 in specialized facilities and services':'No Data'})
#This is all to fix the NaN values so they can all be strings for plotting.


figs, axs = plt.subplots(8,3,figsize=(16,20))
stat = dfHIVfull.loc(axis=0)[:,'2018']
xlab = ['Literacy Rate','Gross Domestic Product perCap','Total Density/100k: Specialized Hospitals 2013',
        'Urbanization', 'Urbanization', 'Hospital Beds','Secondary School Education','PEPFar Aid']
xstats = [stat.sort_values(xlab[0]),
          stat.sort_values(xlab[1]),
          stat[stat['Total Density/100k: Specialized Hospitals 2013']<2].sort_values(xlab[2]),
          stat[stat['Total Density/100k: Specialized Hospitals 2013']<2].sort_values(xlab[3]),
          stat.sort_values(xlab[4]),
          stat.sort_values(xlab[5]),
          stat.sort_values(xlab[6]),
          stat.sort_values(xlab[7])]

ystats = ['Average HIV patients', 'TherapyPercentage2018avg','TherapyNumber2018']

x = [xstats[a][xlab[a]] for a in range(8)]

y = [[xstats[a][ystats[b]] for b in range(3)] for a in range(8)]
for a in range(8):
    for b in range(3):
        if (b == 0) or (b == 2):
            axs[a,b].scatter(x[a],(y[a][b])/xstats[a]['Population'])
        else:
            axs[a,b].scatter(x[a],y[a][b])
        axs[a,b].set(xlabel=xlab[a],ylabel=ystats[b])

figs.tight_layout()

#With those, let's graph em! All of them. Every single possible combination within reason. Excepting the really sorta' dirty Data 3 collection. It's really not worth it.

stat.loc(axis=1)['Literacy Rate','Gross Domestic Product perCap','Total Density/100k: Specialized Hospitals 2013',
        'Urbanization', 'Hospital Beds','Secondary School Education','PEPFar Aid'].cov()

#Take the covariance for a covariance table

totlab = ['Literacy Rate','Gross Domestic Product perCap','Total Density/100k: Specialized Hospitals 2013',
        'Urbanization', 'Hospital Beds','Secondary School Education','PEPFar Aid','Average HIV patients', 
          'TherapyPercentage2018avg','TherapyNumber2018', 'Average HIV Patients div Pop','TherapyNumber2018 div Pop']
stat2 = stat
stat2['Average HIV Patients div Pop'] = stat2['Average HIV patients']/stat2['Population']
stat2['TherapyNumber2018 div Pop'] = stat2['TherapyNumber2018']/stat2['Population']
HIVstats.masscorrelation(stat2,totlab,xlab)

#And create a nice correlation table