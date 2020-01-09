#This will be the statistical models I use with the data. Most of the data is aggragated
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
np.set_printoptions(suppress=True)

#Indicators for wbdata below
indicators = {"NY.GDP.PCAP.CD":"Gross Domestic Product perCap",
              "NY.GDP.MKTP.CD":"Gross Domestic Product",
              "SE.ADT.LITR.ZS":"Literacy Rate",
              "SH.MED.BEDS.ZS":"Hospital Beds",
              "SP.URB.TOTL.IN.ZS":"Urbanization",
              "SE.SEC.ENRR":"Secondary School Education",
              "SP.POP.TOTL":"Population"
             }

#A dictionary with the values for PEPFar aid by country. Not all countries are included.
PepfarOps = {'Afghanistan':0, 'Albania':0, 'Algeria':0, 'Angola':63970147, 'Argentina':0, 'Armenia':0, 
                  'Australia':0, 'Azerbaijan':0, 'Bahamas':0, 'Bangladesh':0, 'Barbados':0, 'Belarus':0,
                  'Belize':0, 'Benin':0, 'Bhutan':0, 'Bolivia (Plurinational State of)':0, 
                  'Bosnia and Herzegovina':0, 'Botswana':243505105, 'Brazil':0, 'Brunei Darussalam':0,
                  'Bulgaria':0, 'Burkina Faso':0, 'Burundi':69377086, 'Cabo Verde':0, 'Cambodia':38004551,
                  'Cameroon':165990182, 'Central African Republic':0, 'Chad':0, 'Chile':0, 'China':0,
                  'Colombia':0, 'Comoros':0, 'Congo':0, 'Costa Rica':0, "Côte d'Ivoire":538265985, 'Croatia':0, 
                  'Cuba':0, 'Czechia':0, 'Democratic Republic of the Congo':260932763, 'Denmark':0, 'Djibouti':0,
                  'Dominican Republic':49846158, 'Ecuador':0, 'Egypt':0, 'El Salvador':0, 'Equatorial Guinea':0, 
                  'Eritrea':0, 'Estonia':0, 'Eswatini':261382646, 'Ethiopia':710615477, 'Finland':0, 'France':0, 'Gabon':0,
                  'Gambia':0, 'Georgia':0, 'Germany':0, 'Ghana':44912122, 'Guatemala':0, 'Guinea':0, 'Guinea-Bissau':0, 
                  'Guyana':0, 'Haiti':478953418, 'Honduras':0, 'Hungary':0, 'Iceland':0, 'Indonesia':48783075, 
                  'Iran (Islamic Republic of)':0, 'Ireland':0, 'Italy':0, 'Jamaica':0, 'Japan':0, 'Jordan':0,
                  'Kazakhstan':0, 'Kenya':2234874886, 'Kuwait':0, 'Kyrgyzstan':0, "Lao People's Democratic Republic":0, 
                  'Latvia':0, 'Lebanon':0, 'Lesotho':261623701, 'Liberia':0, 'Libya':0, 'Luxembourg':0, 'Madagascar':0, 
                  'Malawi':531750870, 'Malaysia':0, 'Mali':0, 'Mauritania':0, 'Mauritius':0, 'Mexico':0, 'Mongolia':0, 
                  'Montenegro':0, 'Morocco':0, 'Mozambique':1570866968, 'Myanmar':0, 'Namibia':251711607, 'Nepal':0, 'New Zealand':0,
                  'Nicaragua':0, 'Niger':0, 'Nigeria':1689405947, 'Norway':0, 'Oman':0, 'Pakistan':0, 'Panama':0, 
                  'Papua New Guinea':20338253, 'Paraguay':0, 'Peru':0, 'Philippines':0, 'Portugal':0, 'Qatar':0, 
                  'Republic of Moldova':0, 'Romania':0, 'Rwanda':358937578, 'Saudi Arabia':0, 'Senegal':0, 'Serbia':0, 
                  'Sierra Leone':0, 'Singapore':0, 'Slovakia':0, 'Somalia':0, 'South Africa':2310288231, 'South Sudan':74394283, 
                  'Spain':0, 'Sri Lanka':0, 'Sudan':0, 'Suriname':0, 'Switzerland':0, 'Syrian Arab Republic':0, 
                  'Tajikistan':0, 'Thailand':0, 'Republic of North Macedonia':0, 'Togo':0, 'Tunisia':0, 
                  'Uganda':1616267026, 'Ukraine':119226605, 'United Republic of Tanzania':1884979709, 'Uruguay':0, 'Uzbekistan':0, 
                  'Viet Nam':0, 'Yemen':0, 'Zambia':1515352860, 'Zimbabwe':646172054}

#This was unavailable, so I had to manually get the alpha codes for the countries I wanted, given the data in my Data1 dataset.
alpha3codedict = {'Afghanistan':'AFG', 'Albania':'ALB', 'Algeria':'DZA', 'Angola':'AGO', 'Argentina':'ARG', 'Armenia':'ARM', 
                  'Australia':'AUS', 'Azerbaijan':'AZE', 'Bahamas':'BHS', 'Bangladesh':'BGD', 'Barbados':'BRB', 'Belarus':'BLR',
                  'Belize':'BLZ', 'Benin':'BEN', 'Bhutan':'BTN', 'Bolivia (Plurinational State of)':'BOL', 
                  'Bosnia and Herzegovina':'BIH', 'Botswana':'BWA', 'Brazil':'BRA', 'Brunei Darussalam':'BRN', 
                  'Bulgaria':'BGR', 'Burkina Faso':'BFA', 'Burundi':'BDI', 'Cabo Verde':'CPV', 'Cambodia':'KHM', 
                  'Cameroon':'CMR', 'Central African Republic':'CAF', 'Chad':'TCD', 'Chile':'CHL', 'China':'CHN', 
                  'Colombia':'COL', 'Comoros':'COM', 'Congo':'COG', 'Costa Rica':'CRI', "Côte d'Ivoire":'CIV', 'Croatia':'HRV', 
                  'Cuba':'CUB', 'Czechia':'CZE', 'Democratic Republic of the Congo':'COD', 'Denmark':'DNK', 'Djibouti':'DJI', 
                  'Dominican Republic':'DOM', 'Ecuador':'ECU', 'Egypt':'EGY', 'El Salvador':'SLV', 'Equatorial Guinea':'GNQ', 
                  'Eritrea':'ERI', 'Estonia':'EST', 'Eswatini':'SWZ', 'Ethiopia':'ETH', 'Finland':'FIN', 'France':'FRA', 'Gabon':'GAB', 
                  'Gambia':'GMB', 'Georgia':'GEO', 'Germany':'DEU', 'Ghana':'GHA', 'Guatemala':'GTM', 'Guinea':'GIN', 'Guinea-Bissau':'GNB', 
                  'Guyana':'GUY', 'Haiti':'HTI', 'Honduras':'HND', 'Hungary':'HUN', 'Iceland':'ISL', 'Indonesia':'IDN', 
                  'Iran (Islamic Republic of)':'IRN', 'Ireland':'IRL', 'Italy':'ITA', 'Jamaica':'JAM', 'Japan':'JPN', 'Jordan':'JOR',
                  'Kazakhstan':'KAZ', 'Kenya':'KEN', 'Kuwait':'KWT', 'Kyrgyzstan':'KGZ', "Lao People's Democratic Republic":'LAO', 
                  'Latvia':'LVA', 'Lebanon':'LBN', 'Lesotho':'LSO', 'Liberia':'LBR', 'Libya':'LBY', 'Luxembourg':'LUX', 'Madagascar':'MDG', 
                  'Malawi':'MWI', 'Malaysia':'MYS', 'Mali':'MLI', 'Mauritania':'MRT', 'Mauritius':'MUS', 'Mexico':'MEX', 'Mongolia':'MNG', 
                  'Montenegro':'MNE', 'Morocco':'MAR', 'Mozambique':'MOZ', 'Myanmar':'MMR', 'Namibia':'NAM', 'Nepal':'NPL', 'New Zealand':'NZL',
                  'Nicaragua':'NIC', 'Niger':'NER', 'Nigeria':'NGA', 'Norway':'NOR', 'Oman':'OMN', 'Pakistan':'PAK', 'Panama':'PAN', 
                  'Papua New Guinea':'PNG', 'Paraguay':'PRY', 'Peru':'PER', 'Philippines':'PHL', 'Portugal':'PRT', 'Qatar':'QAT', 
                  'Republic of Moldova':'MDA', 'Romania':'ROU', 'Rwanda':'RWA', 'Saudi Arabia':'SAU', 'Senegal':'SEN', 'Serbia':'SRB', 
                  'Sierra Leone':'SLE', 'Singapore':'SGP', 'Slovakia':'SVK', 'Somalia':'SOM', 'South Africa':'ZAF', 'South Sudan':'SSD', 
                  'Spain':'ESP', 'Sri Lanka':'LKA', 'Sudan':'SDN', 'Suriname':'SUR', 'Switzerland':'CHE', 'Syrian Arab Republic':'SYR', 
                  'Tajikistan':'TJK', 'Thailand':'THA', 'Republic of North Macedonia':'MKD', 'Togo':'TGO', 'Tunisia':'TUN', 
                  'Uganda':'UGA', 'Ukraine':'UKR', 'United Republic of Tanzania':'TZA', 'Uruguay':'URY', 'Uzbekistan':'UZB', 
                  'Viet Nam':'VNM', 'Yemen':'YEM', 'Zambia':'ZMB', 'Zimbabwe':'ZWE'}

def masscorrelation(df,x,ind):
    #This function takes a dataframe, a list of total labels, and a list of independent variables.
    #It then spits out a correlation table where the independent variables are compared against the dependent variables.
    x1 = list(set(x.copy()))
    ind1 = list(set(ind.copy()))
    corrtable = df[x1].corr()
    for a in ind1:
        x1.remove(a)
    return corrtable.loc(axis=0)[x1].loc(axis=1)[ind1]

def forcemulindex(df,date,columns,y):
    #Takes a dataframe, a single date string, a list of strings, and a lists of two column names to be used.
    # Spits out a new table with a multiindex.
    index000 = [(x,date) for x in df.index]
    index000 = pd.MultiIndex.from_tuples(index000,names=y)
    return pd.DataFrame({columns[a]:df[columns[a]].to_list() for a in range(len(columns))},index000)

def easycouple(dep,indep):
    couple = []
    for a in indep:
        for b in dep:
            couple.append([a,b])
    return couple

def linregtograph(df,columns,ax):
    # Takes a dataframe, desired columns, and axes, returns None with a linear regression graph.
    statty = df.dropna(subset=columns)
    x = statty.loc(axis=1)[columns[0]]
    m,b,r,p,ste = stats.linregress(statty.loc(axis=1)[columns])
    ax.scatter(x,statty.loc(axis=1)[columns[1]])
    ax.plot(x,m*x+b,color=(0.5,0,0.8))
    ax.set(xlabel=columns[0],ylabel=columns[1])
    return None


def multilinreggraph(df,mulcol):
    figs, axs = plt.subplots(len(mulcol),figsize=(16,50))
    if len(mulcol)==1:
        linregtograph(df,mulcol[0],axs)
    else:
        for a in range(len(mulcol)):
            linregtograph(df,mulcol[a],axs[a])
    figs.show()
    figs.tight_layout()
    return None    
    