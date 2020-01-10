# Impacts of a variety of independent variables on HIV rates and HIV treatment rates per country

## Introduction

When studying HIV on the individual level, one must discuss HIV in terms of their T-cell counts (at various times), the time between noticing the disease and treating it, the treatment used, and so on. However, this data isn't public--it involves fairly serious medical data, which could be abused.

Instead, we'll be dealing with aggragated data, which involves its own disadvantages: a lack of particularity and little information on available treatments and individuals' medical statistics, and little that can be done with sampling, given that the sample size easily exceeds half of the countries in the world.
Advantages, however, include the ability to perform more predictive measures on a global scale, and perhaps more importantly, a way to see which measures might result in both lower rates of HIV per country, and higher rates of HIV treatment.

Among these possible variables include: 
- Gross Domestic Product per Capita--The richer a country's people, perhaps the more likely they would be to afford medical treatment and living conditions that don't spread the disease
- Literacy--If people can read, they can take note of any signs or pamphlets that warn against HIV-spreading behavior.
- Hospital Bed Density--If there are more beds, then more people can be treated without waiting lines. Doesn't speak for understaffing.
- Urbanization--With more tightly packed people, the disease can spread more often, but at the same time, hospitals are closer.
- Secondary School Education--Similar to Literacy, but an ability to better understand more preventative methods and access more lucrative jobs to raise living standards.
- Hospital Density--The more available hospitals, especially Specialist hospitals, the more likely someone looking for HIV treatment would be able to find it.
 - HIV treatment availability in specialist hospitals--this combines with the density of specialist hospitals to give us a better understanding of the ease of access someone with HIV has to HIV treatment.


## Data

5 Total Datasets, and 1 Spare, unused.


WorldBank Data:

| Indecies | Column | Description                       |
|----------|:------:|----------------------------------:|
| Country  | GDP    | Gross Domestic Product (Total)    |
| Date (1960-2018)| GDP per Capita | Gross Domestic Product per Capita |
|          | Literacy Rate | Percentage Literacy in the given Country |
|          | Hospital Beds| Number of Hospital Beds per 1000 people |
|          | Urbanization | Percentage of people in Urban Areas |
|          | Secondary School Education | Percentage of Population that has Secondary School Education |
|          | Population | Total Population              |


CIA Factbook Data:

| Column | Description |
|--------|------------:|
| Country| Country name|
|Country Code| AlphaThree 3-letter Country Code|


WHO HIV rates and treatment Data:

| Column | Description |
|--------|------------:|
|Country | Country name (different from CIA and WorldBank country name) |
| TherapyPercentage | Estimated antiretroviral Therapy coverage among people living with HIV (%) 2018|
| TherapyNumber | Reported number of people receiving antiretroviral Therapy |
| HIV2018 | Estimated Number of people (all ages) living with HIV 2018 |
| HIV2010 | Estimated Number of people (all ages) living with HIV 2010 |
| HIV2005 | Estimated Number of people (all ages) living with HIV 2005 |
| HIV2000 | Estimated Number of people (all ages) living with HIV 2000 |


WHO Hospital Data:

| Column | Description |
|--------|------------:|
| Country | Country name (different from CIA and WorldBank country name)|
| Year | 2010 and 2013 only|
| Total Density per 100,000 Population:Health Posts | - |
|Total Density per 100,000 Population:Health Centers| - |
|Total Density per 100,000 Population:District/Rural Hospitals| - |
|Total Density per 100,000 Population:Provincial Hospitals| - |
|Total Density per 100,000 Population:Specialized Hospitals| - |
|Total Density per 100,000 Population:Hospitals| Total Hospitals per 100,000 People|


PEPfAR Expenses Data:

| Column | Description |
|--------|------------:|
| Country | Country name (different from CIA and WorldBank country name)|
| PEPFar Expenditures | Total Expenditures per Country from the President's Emergency Plan for AIDS Relief (PEPfAR) |


WHO Councelling/Treatment/Testing Data:

| Column | Description |
|--------|------------:|
| Country | Country name (different from all other country names)|
| HIV(ARV) Treatment 2014 | HIV (ARV) Treatment availability in Specialized Facilities and Services |
| HEPATITIS Treatment 2014| HEPATITIS Treatment availability in Specialized Facilities and Services |
| HIV Testing and Councelling 2014| HIV Testing and Councelling availability in Specialized Facilities and Services|
| Hepatitis Testing and Councelling 2014| Hepatitis Testing and Councelling availability in Specialized Facilities and Services|
| Hepatitis Vaccination 2014| Hepatitis Vaccination availability in Specialized Facilities and Services|


## Methods

**Data Cleaning Methods**

First among data cleaning methods was getting all of my desired data into clean columns. The WHO HIV rates and treatment Data table in particular included a great deal of messy data. Every column was a string, because every column included brackets with ranges, eg. 22 000\[12 000 - 24 000\]. Additionally, each number had a space separating the thousandths. Some countries had < signs in their HIV20XX columns. Lastly, each number column needed to be set .astype to Float. Similar proccesses were performed for the rest of the data, except for the WorldBank data, which was fairly clean, and needed nothing more than picking out specific columns and backfilling. The backfilling will be addressed after the Conclusion.

Next was correcting country names to match those of WorldBank's data. Unfortunately, this required creating a dictionary specifically for these country name -> correct country name pairs. Next, again, was creating a dictionary of Country codes to match up the countries listed in the WHO HIV rates and treatments, and take only the countries from WorldBank that matched. This reduced wait times for loading significantly.

The most important part of the dataset was matching up all the appropriate columns. In the case of the WHO HIV rates and treatment Data, the table had to be split, given a new index, and one of those split tables had to be Transposed.
For four different tables, this was done using the following code:

```python
def forcemulindex(df,date,columns,y):
    index000 = [(x,date) for x in df.index]
    index000 = pd.MultiIndex.from_tuples(index000,names=y)
    return pd.DataFrame({columns[a]:df[columns[a]].to_list() for a in range(len(columns))},index000)
```

Afterwards, all tables were easily joinable.

The WHO Councelling/Treatment/Testing Data went unused, because it included too many missing values along dependent variables that already included missing values in many larger countries, and because its data was qualitative.


**Hypotheses**

With the data cleaned, there were still a few variables that were not ready. One was HIV rates, which required dividing the reported HIV numbers by the population. Another was splitting the PEPfAR funding by the number of reported HIV cases, in order to determine whether spending more on a given patient would influence treatment rates, and likewise, whether HIV rates would influence PEPfAR funding per HIV-infected capita.

My Hypotheses were as follows:
- Null: PEPfAR funding does not have a significant impact on HIV treatment (a=0.05) 
- Alternate:PEPfAR funding would have significant impact on HIV treatment

And:
- Null: PEPfAR funding is not the most significant variable with respect to HIV treatment rates.
- Alternate:PEPfAR funding is the most significant variable with respect to HIV treatment rates.


**Statistical Methods**

I then performed a correlation between dependent and independent variables, a correlation between independent variables, a covariance between independent variables, a series of linear regressions (Although an inverse or logarithmic regression might've fit some of the data better), and drew p-values to determine which variables were statistically significant with respect to the two major dependent variables: Rate of HIV testing, and 


## Results

A correlation matrix was set up in order to determine which independent variables influenced each other most. A covariance table was made, but went unused because the units involved and scales were so different from one another. For the purposes of this project, only 2018 was used.

**Independent Variable Correlation**

See the following correlation table:

![HIV Independent Variable Correlation Table](https://github.com/nvanrompaey/ImpactsHIVTreatmentCap1/img/CorrelationTable.png)

- Literacy Rate is fairly strongly correlated with Secondary School Education, as expected, somewhat strongly connected to GDP per Capita, Urbanization, and Hospital Beds.
- Secondary School Education is somewhat strongly connected to GDP per Capita, Urbanization, and Hospital Beds, and a small negative correlation with PEPfAR funding per HIV-infected Capita.
- GDP per Capita is somewhat strongly connected to Urbanization, but not that heavily correlated with Hospital Beds.
- Urbanization only has a little correlation with Hospital Bed density, and a small negative correlation with PEPfar funding per HIV-infected Capita.

This means that Literacy Rate is a fairly strong bet instead of Secondary School Education, but for the most part, none are significant predictors of the others. We can then remove Secondary School Education, slightly thinning things out


**Dependent Variable Correlation**

See the following correlation table:

![HIV Dependent Correlation Table](https://github.com/nvanrompaey/ImpactsHIVTreatmentCap1/img/DependentCorrelationTable.png)

Woah! This one's a little different. These correlation values aren't that strong at all between are most interesting Dependent variables.

HIV rates are only correlated heavily with PEPfAR aid, and slightly with PEPfAR per HIV Capita. This doesn't say much for PEPfAR helping out with HIV rates, but rather, the higher the HIV issue, likely, the more PEPfAR aid is needed! That just makes sense. One would expect a huge problem would warrant a larger response. But on a smaller scale, the amount of PEPfAR per person doesn't really have an impact on HIV rates, nor HIV rates on PEPfAR per person.

However, Treatment Rates are only moderately correlated with Gross Domestic Product per Capita, and somewhat correlated with everything except for Specialist Hospital Density. It seems that Gross Domestic Product really determines whether a country has a good chance of treating HIV, and everything else is just a bit of a help.

But let's take some regressions.


**Linear Regressions**

![Urbanization vs Treatment Rate Linear Regression](https://github.com/nvanrompaey/ImpactsHIVTreatmentCap1/img/LinregURBTreat.png)
![GDP vs Treatment Rate Linear Regression](https://github.com/nvanrompaey/ImpactsHIVTreatmentCap1/img/LinregGDPCTreat.png)
![Secondary School Education vs Treatment Rate Linear Regression](https://github.com/nvanrompaey/ImpactsHIVTreatmentCap1/img/LinregSecSchoolTreat.png)
![Literacy rate vs HIV rate Linear Regression](https://github.com/nvanrompaey/ImpactsHIVTreatmentCap1/img/LinregLitHIVrate.png)


It looks like we actually see some predictive lines here. Urbanization seems to have an upward trend with respect to Treatment Rate between countries. GDP definitely has a strong correlation, but this correlation might even be stronger if it's logarithmic!

What's surprising to see, though, is our lost 'Secondary School Education' variable returns fairly strongly in the regression. However, Literacy rate seems to have no impact on HIV rate at all--it's nearly a flat line.

Let's look at the P-values, then, see which are most statistically significant.

|P-Values| Hospital Density<br>per 100k|Hospital Beds|Urbanization|Literacy Rate|PEPfAR aid per HIV-infected Capita|GDP per Capita|Secondary School Education|
|---|---|---|---|---|---|---|---|
|HIV Rate|0.8490680968076938|0.1423298878606633|0.019183689311732557|0.8114069990259042|2.2796476790831106e-07|0.10256953652729779|0.047023565496384874| 
|Treatment Rate|0.2471899373777917|0.007917216110037185|0.017992359238618406|0.001479948587061623|0.009631853816514345|6.378889713470144e-07|0.00014549911275807775|


The P-values these regressions describe seem to imply that for HIV rates, the best predictors are Urbanization and PEPfAR aid per Capita.
Likewise, for Therapy rates, the best predictors appear to be Secondary School Education, and Literacy rate.

Further visualizations were used for a more map-based stance, as were 3-dimensional and 4-dimensional graphs.


# Limitations
As said at the very start of this document, the data I'm using is aggragated, and therefore a fairly small dataset, with a frankly wide variety of results. Many of the results were from different years, and worse, some major HIV rates were missing entirely--such as from the US, Canada, Russia, China, and India, which make up a more than significant portion of the world's population alone. the CDC might have more information, but I didn't use their data this time.

Furthermore, I had to backfill my WorldBank data--this was necessary because there wasn't any current data. This, however, is dangerous, because in some cases, it was necessary to push forward even 1993 data up to 2018.

In a similar vein, this data included values from 2000 to 2018, and I only used the 2018 data, assuming the 2013 and 2014 data was similar enough. In another study, I would likely take a snapshot of the data for 2000,2010,2005,2000, and show off the data

