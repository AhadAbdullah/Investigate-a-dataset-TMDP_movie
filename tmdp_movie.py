# -*- coding: utf-8 -*-
"""TMdp-Movie.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cm0G2-EJ_An2k2MHFaDZRJt0RNzJgWzL

# Project TMDb movie Analysis
#### By Ahad Alotaibi

## Table of content 

 <li><a href='#intro'>Introducation </a></li>
 <li><a href='#wrangling'>Date Wrangling</a></li>
 <li><a href='#eda'>Exploratory Data Analysis </a></li>
 <li><a href='#conclusions'>conclusions </a></li> </ul>

#Introducation



In this project we will be analysing data assocaiated with the TMDb movie data (cleaned from original data on Kaggle) This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.In particular, we will be intrested in finding:
- The original title for the movie have the highest runtime in 1990.
- Which genre (romance / horror) has the highest popularity (with the release bettwen years (1960 - 1990))
-Is there a relationship between budget and revenue
-Number of movie releases per year
"""

# Commented out IPython magic to ensure Python compatibility.
# Import Python necessary  package essential for our analysis 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
from IPython.display import display

"""# Date Wrangling 
### General properties
"""

# Load your data and print out a few lines. Perform operations to inspect data
df = pd.read_csv('tmdb-movies.csv')
df.head(100000)

df.columns

# Shape of our dataset.
df.shape

# describe the dataset 
df.describe()

df.info()

# to defind how much null value in each culome 
df.isnull().sum()

"""We know the culome 
(popularity ,budget ,revenue ,original_title ,runtime,release_date,revenue,vote_count ,vote_average ,release_year,budget_adj,revenue_adj ) not have null value.
"""

# Check for duplicated rows:
df.duplicated().sum()

#drop these duplicated rows 
df.drop_duplicates(inplace=True)
# To confirme is drop Duplicate
df.duplicated().sum()

# Drop the coulme we will not used in data anlaysis 
df.drop(
    ['homepage','tagline','production_companies','keywords','overview'
     ,'cast','director','release_date','vote_count','vote_average'], inplace = True, axis = 1)

"""# Exploratory Data Analysis

Research Question 1 ( The original title for the 
movie have the highest runtime in 1990 ? )
"""

#Step 1
#show all row when release_year = 1990
#df.query('release_year == 1990')
#get runtime 
release_copy=df.query('release_year == 1990').get(["original_title","runtime"])
#release_copy=df.query('release_year == 1990')
release_copy.head(10866)
#get the original title for the movie have the highest runtime in 1990 
print(release_copy['runtime'].max())
print("Movie have highest runtime in 1990")
print(release_copy.query('runtime==192').get(["original_title"]))

"""**Observations** : The original_title of Movie have highest runtime in 1990 is Stephen King's It

Research Question 2 (Which genre (romance / horror) has the highest popularity (with the release bettwen years (1960 - 1990)
"""

# Step 1
from pandas.core.window.expanding import Axis
from os import access
# to split the genres 
genres = df.genres.str.get_dummies()
# concat the dummies with the data set  
genres1=pd.concat([df,genres],axis=1)
# To make sure of the merge print the name of columns 
genres1.columns

from matplotlib import colors
from numpy.lib.shape_base import tile
#step 2 
# query about release_year with the release bettwen years (1960 - 1990) have 1 in Romance or Horror
Quetion2=genres1.query('release_year >= 1960 & release_year <= 1990').get(["release_year","popularity","Romance","Horror"])

# find the MAX popularity in Romance 
romance=Quetion2.query('Romance == 1').get(["release_year","popularity"]).groupby('release_year')[['popularity']].max()

# find the MAX popularity in Horror 
Horror=Quetion2.query('Horror == 1').get(["release_year","popularity"]).groupby('release_year')[['popularity']].max()

#Step 3 
#and storing all this in variable
Horror_polt= Horror.groupby('release_year')[['popularity']].sum()
romance_polt=romance.groupby('release_year')[['popularity']].sum()
#giving the figure size(width, height)
plt.figure(figsize=(12,6), dpi = 130)
#labeling x-axis
plt.xlabel('Release Year of Movies', fontsize = 12)
#labeling y-axis
plt.ylabel('Max popularity for romance and horror Movies', fontsize = 12)
#title of a the plot
plt.title('Highest popularity for genre romance and horror bettwen years (1960 - 1990)')
#plotting what needs to be plotted
plt.plot(Horror_polt, color='red')
plt.plot(romance_polt, color= 'blue')
#showing the plot
plt.show()

"""**Observations**:
The popularity of Romance Movies began from 1982 to 1990 and achieved the highest prevalence in 1990, while horror Movies began to decline in popularity after 1986, and the highest value of spread was in 1979.

Research Question 3 (Is there a relationship between budget and revenue?)
"""

from matplotlib import colors
from numpy.lib.shape_base import tile
#Research Question 2 (Is there a relationship between budget and revenue?)
#Step 1
#giving the figure size(width, height)
plt.figure(figsize=(12,8), dpi = 130)
# Plotting the relation between revenue & vote counts
Quetion3= plt.scatter(df['budget_adj'],
            df['revenue_adj'], 
            alpha = 0.6) #transparency level of points on the plot. Used to avoid overplotting
# add and format additional elements, such as titles and axis labels
#title of a the plot
plt.title('A Relationship between budget and revenue',fontsize = 14, 
          weight = "bold")
#labeling x-axis
plt.xlabel("budget_adj", weight = "bold")
#labeling y-axis
plt.ylabel("revenue_adj", weight = "bold")
#showing the plot
plt.show()

"""**Observations**:


1.   The graph shows that the most Movies that had a budget between 0 to 1 million dollars (in dollar value in 2010) got a Revenue equal to the budget  or less than 0.5 of the budget .
2.   The highest Revenue value was 2.9 million dollars(in dollar value in 2010) for a movie with a budget of 2.4
3.   The value of the budget spent on the movies is not the main factor in increasing the Revenue

Research Question 4 (Number of movie releases per year ?)
"""

#Research Question 4 (Number of movie releases per year ?)
Release_Movie=df.query('release_year >=1960').get(["release_year"])
Release_Movie.release_year.hist()
# title and labels
plt.xlabel('Release year')
plt.ylabel('Count of movie')
plt.title('Number of movie releases per year')

"""**Observations**:

1.   From 1960 to 1984, the number of Movies produced each year did not exceed 100 Movies.
2.   The graph shows The Movie production sector began to grow in 1979's.
3.   700 Movie were produced in 2015, which is the highest value so far.

#Conclusions

####Data Limitations:

Although our dataset contains more than 10,000 rows it's pretty insufficient to draw precise conclusions :

1. Most of the data columns are irrelevant for the analysis

2. many NAN values are missing from our dataset for an uncertain reason (We should try a better web scrapping for a better data quality or prepare data from a different source).

3. The formula for writing budget, Revenue, etc. is inaccurate

####Conclusions :


*   The original_title of Movie 
have highest runtime in 1990 is Stephen King's It
*   The popularity of Romance Movies began from 1982 to 1990 and achieved the highest prevalence in 1990, while horror Movies began to decline in popularity after 1986, and the highest value of spread was in 1979.   
*   The graph shows that the most Movies that had a budget between 0 to 1 million dollars (in dollar value in 2010) got a Revenue equal to the budget  or less than 0.5 of the budget .
*   The highest Revenue value was 2.9 million dollars(in dollar value in 2010) for a movie with a budget of 2.4
*   The value of the budget spent on the movies is not the main factor in increasing the Revenue .
*   From 1960 to 1984, the number of Movies produced each year did not exceed 100 Movies.
*   The graph shows The Movie production sector began to grow in 1979's.
*   700 Movie were produced in 2015, which is the highest value so far.
"""