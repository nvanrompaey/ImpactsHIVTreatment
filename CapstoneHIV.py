import numpy as np
import pandas as pd
import wbdata
#import plotly.graph_objects as go
#The usual suspects

indicators = {"NY.GDP.PCAP.CD":"Gross Domestic Product perCap",
              "NY.GDP.MKTP.CD":"Gross Domestic Product",
              "SE.ADT.LITR.ZS":"Literacy Rate",
              "SH.MED.BEDS.ZS":"Hospital Beds",
              "SP.URB.TOTL.IN.ZS":"Urbanization",
              "SE.SEC.ENRR":"Secondary School Education",
             }
countries = [i['id'] for i in wbdata.get_country(display=False)]
df = wbdata.get_dataframe(indicators,country='all')
#Wb data lets me get pandas dataframes directly from a source. Hopefully I'll be able to front-end the country tags.

#Unfortunately, there was no clear dictionary with these values. I've decided to create them manually for only the countries that
# don't have No Data values in both my dependent variables, TherapyPercentage2018 and TherapyNumber2018
alpha3codedict = {'Afghanistan':'AFG', 'Albania':'ALB', 'Algeria':'DZA', 'Angola':'AGO', 'Argentina':'ARG', 'Armenia':'ARM', 
                  'Australia':'AUS', 'Azerbaijan':'AZE', 'Bahamas':'BHS', 'Bangladesh':'BGD', 'Barbados':'BRB', 'Belarus':'BLR',
                  'Belize':'BLZ', 'Benin':'BEN', 'Bhutan':'BTN', 'Bolivia (Plurinational State of)':'BOL', 
                  'Bosnia and Herzegovina':'BIH', 'Botswana':'BWA', 'Brazil':'BRA', 'Brunei Darussalam':'BRN', 
                  'Bulgaria':'BGR', 'Burkina Faso':'BFA', 'Burundi':'BDI', 'Cabo Verde':'CPV', 'Cambodia':'KHM', 
                  'Cameroon':'CMR', 'Central African Republic':'CAF', 'Chad':'TCD', 'Chile':'CHL', 'China':'CHN', 
                  'Colombia':'COL', 'Comoros':'COM', 'Congo':'COG', 'Costa Rica':'CRI', "Côte d'Ivoire":'CIV', 'Croatia':'HRV', 
                  'Cuba':'CUB', 'Czechia':'CZE', 'Democratic Republic of the Congo':'COD', 'Denmark':'DNK', 'Djibouti':'DJI', 
                  'Dominican Republic':'DOM', 'Ecuador':'ECU', 'Egypt':'EGY', 'El Salvador':'SLV', 'Equatorial Guinea':'GNQ', 
                  'Eritrea':'ERI', 'Estonia':'EST', 'Eswatini':'SWZ', 'Ethiopia':'ETH', 'Finland':'FIN', 'France':'FRA',                             'Gabon':'GAB', 
                  'Gambia':'GMB', 'Georgia':'GEO', 'Germany':'DEU', 'Ghana':'GHA', 'Guatemala':'GTM', 'Guinea':'GIN',                                 'Guinea-Bissau':'GNB', 
                  'Guyana':'GUY', 'Haiti':'HTI', 'Honduras':'HND', 'Hungary':'HUN', 'Iceland':'ISL', 'Indonesia':'IDN', 
                  'Iran (Islamic Republic of)':'IRN', 'Ireland':'IRL', 'Italy':'ITA', 'Jamaica':'JAM', 'Japan':'JPN',                                 'Jordan':'JOR',
                  'Kazakhstan':'KAZ', 'Kenya':'KEN', 'Kuwait':'KWT', 'Kyrgyzstan':'KGZ', "Lao People's Democratic Republic":'LAO', 
                  'Latvia':'LVA', 'Lebanon':'LBN', 'Lesotho':'LSO', 'Liberia':'LBR', 'Libya':'LBY', 'Luxembourg':'LUX',                               'Madagascar':'MDG', 
                  'Malawi':'MWI', 'Malaysia':'MYS', 'Mali':'MLI', 'Mauritania':'MRT', 'Mauritius':'MUS', 'Mexico':'MEX',                             'Mongolia':'MNG', 
                  'Montenegro':'MNE', 'Morocco':'MAR', 'Mozambique':'MOZ', 'Myanmar':'MMR', 'Namibia':'NAM', 'Nepal':'NPL',                           'New Zealand':'NZL',
                  'Nicaragua':'NIC', 'Niger':'NER', 'Nigeria':'NGA', 'Norway':'NOR', 'Oman':'OMN', 'Pakistan':'PAK',                                 'Panama':'PAN', 
                  'Papua New Guinea':'PNG', 'Paraguay':'PRY', 'Peru':'PER', 'Philippines':'PHL', 'Portugal':'PRT', 'Qatar':'QAT', 
                  'Republic of Moldova':'MDA', 'Romania':'ROU', 'Rwanda':'RWA', 'Saudi Arabia':'SAU', 'Senegal':'SEN',                               'Serbia':'SRB', 
                  'Sierra Leone':'SLE', 'Singapore':'SGP', 'Slovakia':'SVK', 'Somalia':'SOM', 'South Africa':'ZAF',                                   'South Sudan':'SSD', 
                  'Spain':'ESP', 'Sri Lanka':'LKA', 'Sudan':'SDN', 'Suriname':'SUR', 'Switzerland':'CHE',                                             'Syrian Arab Republic':'SYR', 
                  'Tajikistan':'TJK', 'Thailand':'THA', 'Republic of North Macedonia':'MKD', 'Togo':'TGO', 'Tunisia':'TUN', 
                  'Uganda':'UGA', 'Ukraine':'UKR', 'United Republic of Tanzania':'TZA', 'Uruguay':'URY', 'Uzbekistan':'UZB', 
                  'Viet Nam':'VNM', 'Yemen':'YEM', 'Zambia':'ZMB', 'Zimbabwe':'ZWE'}


df.info()
df.head()
df.describe()
#The even more usual suspects
df.loc(axis=0)[:,'2018'].loc(axis=1)['Literacy Rate']
#Testing whether or not I can locate data by both multi-index and column. Definitely can.

df1 = pd.read_csv("data/data.csv")
df3 = pd.read_csv("data/data-2.csv")
df4 = pd.read_csv("data/data-3.csv")
# To be renamed appropriately later
df1.info()
df0 = df1
df0.columns = ['Country','TherapyPercentage2018','TherapyNumber2018','HIV2018','HIV2010','HIV2005','HIV2000']
df2 = df0.loc[(df0['TherapyPercentage2018']!='No data')| (df0['TherapyNumber2018']!='No data')]
df2.drop(0,inplace=True)
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

df2.astype({'TherapyPercentage2018avg':float,'TherapyNumber2018':float,'HIV2018avg':float,'HIV2010avg':float,'HIV2005avg':float,'HIV2000avg':float})

#All Data Cleaning! Just making sure all of the columns are floats and have NaN instead of No Data and have no weird 
#symbols in there.

df2.drop(['TherapyPercentage2018','HIV2018','HIV2010','HIV2005','HIV2000'],axis=1,inplace=True)
df2.head() #Just to make sure it looks nice

df33 = df3[df3['Year']==2013]
#Moving on to data set 2, and making sure it shows only hospitals in a year.

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
