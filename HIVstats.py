#This will be the statistical models I use with the data. Most of the data is aggragated
import numpy as np
import pandas as pd
np.set_printoptions(suppress=True)

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

def masscorrelation(df,x,ind):
    x1 = list(set(x.copy()))
    ind1 = list(set(ind.copy()))
    corrtable = df[x1].corr()
    for a in ind1:
        x1.remove(a)
    return corrtable.loc(axis=0)[x1].loc(axis=1)[ind1]
    