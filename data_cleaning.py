'''Importing Necessary Dependencies'''
import re
import pandas as pd

## Reading Dataset
df = pd.read_csv('./ottdata2.csv')

## Droping Unnecessary Columns and Rows
df.drop(columns=['Unnamed: 0'], inplace= True)

df.drop_duplicates(subset='Title', keep='first', inplace=True)

droplist = df[(df.Type.isnull()) & (df.Release_Year.isnull()) & (df.Certificate.isnull()) & (df.Duration.isnull()) & (df.Genre.isnull()) & (df.Ratings.isnull()) & (df.Director.isnull()) & (df.Cast.isnull()) & (df.Platform.isnull())] # pylint: disable=line-too-long

droplist = droplist.index.to_list()

df.drop(droplist, inplace=True)

## After Drop, Resetting Index
df.reset_index(drop = True, inplace=True)

## Working on Release_Year Column
for i in df.index:
    try:
        a = df.Release_Year.loc[i]
        a = a.split(' ')[1]
        a = a[1:5]
        df.at[i, 'Release_Year'] = a
    finally:
        continue

df.Release_Year = pd.to_numeric(df.Release_Year, errors='coerce')

df.Release_Year.fillna(0, inplace=True)

df.Release_Year = df.Release_Year.astype('int64')
# Release Year contains Value: 0 instead of NaN

## Working on Certificate Column
df.Certificate.replace({'Not Rated':'Unrated', 'Passed':'Approved', '16':'16+', '13':'13+', '18':'18+', 'All':'UA', '15':'15+', '12':'12+', 'U/A':'UA'}, inplace=True) # pylint: disable=line-too-long

## Working on Duration Column
df.Duration = df.Duration.str.replace(' min','')

df.Duration = df.Duration.str.replace(',','')

df.Duration.fillna(0, inplace=True)

df.Duration = df.Duration.astype('int64')
# Duration is in Minutes, NaN values is filled with integer 0

## Working on Genre Column
df.Genre = df.Genre.str.split(',')

df.Genre.fillna('Not Available', inplace=True)

## Working on Director Column
df.Director = df.Director.str.split(',')

df.Director.fillna('Not Available', inplace=True)

for i in df.index:
    if df.Director.loc[i] == 'Not Available':
        continue
    else:
        a = df.Director.loc[i]
        row = []
    for j, value in enumerate(a):
        if j == 0:
            row.append(value)
        else:
            b = value[1:]
            row.append(b)
    df.at[i, 'Director'] = row

## Working on Cast Column
df.Cast = df.Cast.str.split(',')

df.Cast.fillna('Not Available', inplace=True)

for i in df.index:
    if df.Cast.loc[i] == 'Not Available':
        continue
    a = df.Cast.loc[i]
    row = []
    for j, value in enumerate(a):
        row.append(' '.join(re.findall('[A-Z][a-z]*', value)))

    df.at[i, 'Cast'] = row
