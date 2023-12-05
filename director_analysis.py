'''Importing Necessary Dependencies'''
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template as load_template
from data_cleaning import df

## Loading Bootstrap Template "SLATE"
TEMPLATES = 'slate'
load_template(TEMPLATES)

### Director Analysis
directors = []
for i in df.index:
    if df.Director.loc[i] == 'Not Available':
        continue
    for j in df.Director.loc[i]:
        if j in directors:
            continue
        directors.append(j)

dt = pd.DataFrame(columns=['Director', 'Count', 'Avg_Ratings', 'Platform'])

for i in directors:
    filtered_df = df[df['Director'].apply(lambda x, temp=i: temp in x)]
    count = filtered_df.shape[0]
    ratings = filtered_df.Ratings.mean()
    platform = filtered_df.Platform.unique().tolist()
    dt.loc[len(dt.index)] = [i, count, ratings, platform]

## Figure 1: Saturation of Directors in Different Ratings
fig1 = px.histogram(dt, x = 'Avg_Ratings', color_discrete_sequence=['rgb(72, 84, 99)'])
fig1.update_layout(title = 'Saturation of Directors in different Ratings',
                   xaxis_title = 'Ratings',
                   yaxis_title = 'Count of Directors',
                   )
#fig1.show()

## Figure 2: Distribution of Directions in Platforms
# Calculating Platform Frequencies
count = dt.explode('Platform')['Platform'].value_counts().reset_index()
count.columns = ['Platform', 'Frequency']

## Plotting Pie Chart
colors = ['rgb(72, 84, 99)', 'rgb(92, 104, 119)', 'rgb(112, 124, 139)',
          'rgb(132, 144, 159)', 'rgb(152, 164, 179)', 'rgb(172, 184, 199)']

fig2 = go.Figure(data=[
            go.Pie(labels=count.Platform, values=count.Frequency, marker=dict(colors=colors))
        ])

fig2.update_layout(
    title='Distribution of Directions in different Platforms'
)

fig2.update_traces(hoverinfo='label+value+percent',
                  textinfo='label+percent',
                  title_font = dict(size=20))

#fig2.show()

## Figure 3: Top 10 Most Active Directors
active_directors = dt.sort_values(by="Count", ascending=False).head(10)

fig3 = go.Figure(data=[
    go.Bar(x = active_directors.Director,
          y = active_directors.Count,
          name='Count of Movies',
          marker_color='rgb(72, 84, 99)'),
    go.Bar(x = active_directors.Director,
          y = active_directors.Avg_Ratings,
          name = 'Average Rating of Director',
          marker_color='rgb(92, 104, 119)')
])

fig3.update_layout(title='Top 10 Most Active Directors',
                  xaxis = dict(title='Director'),
                  yaxis = dict(title='Count of Directions & Average Ratings'),
                  barmode = 'group',
                  )

#fig3.show()

## Figure 4: Top 10 Highest Rated Directors
top_dir1 = dt.sort_values(by='Avg_Ratings',ascending = False).head(10)
top_dir_list = top_dir1.Director.to_list()

top_dir = pd.DataFrame(columns=['Director', 'Genre', 'Ratings'])

for i in top_dir_list:
    filtered_df = df[df['Director'].apply(lambda x, temp=i: temp in x)]
    genre = filtered_df.Genre.explode().to_list()
    rate = top_dir1[top_dir1.Director == i].Avg_Ratings
    top_dir.loc[len(top_dir.index)] = [i, genre, rate.values[0]]
# Create an empty list to store expanded data
expanded_data = []

# Iterate over rows and expand the data
for idx, row in top_dir.iterrows():
    for genre in row['Genre']:
        expanded_data.append(
            {'Director': row['Director'], 'Ratings': row['Ratings'], 'Genre': genre}
            )

# Create a DataFrame from the expanded data
expanded_df = pd.DataFrame(expanded_data)

# Create a grouped bar chart using Plotly Express
fig4 = px.bar(expanded_df, x='Director', y='Ratings', color='Genre', barmode='overlay',
             title='Movie Ratings by Genre and Director',
             labels={'Ratings': 'Movie Ratings', 'Director': 'Director Name', 'Genre': 'Genre'},
             color_discrete_sequence=['rgb(72, 84, 99)', 'rgb(92, 104, 119)', 'rgb(112, 124, 139)',
                             'rgb(132, 144, 159)', 'rgb(152, 164, 179)', 'rgb(172, 184, 199)']
            )

## Show the chart
#fig4.show()
