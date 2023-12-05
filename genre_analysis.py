'''Importing Necessary Dependencies'''
from collections import Counter
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash_bootstrap_templates import load_figure_template as load_template
from data_cleaning import df

## Loading Bootstrap Template "SLATE"
TEMPLATES = 'slate'
load_template(TEMPLATES)

# Fetching Count of Genre
genre_counts = {}
for i in df.Genre:
    if i == 'Not Available':
        continue
    else:
        for j in i:
            genre_counts[j] = genre_counts.get(j, 0) + 1

genre_counts_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count'])

## Figure 1: Genre Counts
bar_trace = go.Bar(
    x=genre_counts_df['Genre'],
    y=genre_counts_df['Count'],
    name='Bar Chart',
    text=genre_counts_df['Count'],  # Text values to display on each bar
    textposition='outside',  # Automatically position the text
    marker_color='rgb(72, 84, 99)'
)

line_trace = go.Scatter(
    x = genre_counts_df['Genre'],
    y = genre_counts_df['Count'],
    mode = 'lines',
    name = 'Line Overlay',
    yaxis = 'y2', #Use a secondary y-axis for the line trace
    line=dict(color='rgb(0, 128, 255)')  # Set line color to a shade of blue
)

layout = go.Layout(
    title = 'Genre Counts',
    yaxis = dict(title = "Count"),
    yaxis2 = dict(title = "Count", overlaying = 'y', side='right')
)

genre_fig1 = go.Figure(
    data = [
        bar_trace,
        line_trace
    ],
    layout=layout
)

#genre_fig1.show()

## Figure 2: Top 5 Genres by Movie Count

top_genres = genre_counts_df.sort_values(by='Count', ascending=False).head(10)
genre_fig2 = px.bar(
    top_genres,
    x='Genre',
    y='Count',
    title='Top 5 Genres by Movie Count',
    labels={'Genre': 'Genre', 'Count': 'Number of Movies'},
    color_discrete_sequence=['rgb(72, 84, 99)']
)

# Customizing the appearance of the chart
genre_fig2.update_layout(
    xaxis_title='Genre',
    yaxis_title='Number of Movies',
)

# Adding hover text for more information
genre_fig2.update_traces(text=top_genres['Count'], textposition='outside')

# Adjusting the size and appearance of the figure
genre_fig2.update_layout(
    margin=dict(l=50, r=50, t=80, b=80),
)

## Figure 3: Top 5 Common Genre Pairs

genre_lists = []
for genres in df['Genre']:
    if len(genres) > 1:
        genre_lists.append(genres)
genre_counts = []
for genres in genre_lists:
    a =tuple(genres)
    genre_counts.append(a)
a = Counter(genre_counts)

b = a.most_common(5)

top_5 = []
for genres, count in b:
    #print(list(genres), count)
    top_5.append((list(genres), count))

# Create a DataFrame for the top 5 common genre lists
top_genre_lists_df = pd.DataFrame({'Genre List': [", ".join(genres) for genres, _ in top_5],
                                  'Count': [count for _, count in top_5]})


# Create a bar chart using Plotly
genre_fig3 = px.bar(
    top_genre_lists_df,
    x='Genre List',
    y='Count',
    title='Top 5 Common Genre Lists',
    labels={'Genre List': 'Genre List', 'Count': 'Frequency'},
    color_discrete_sequence=['rgb(72, 84, 99)']
)

# Customizing the appearance of the chart
genre_fig3.update_layout(
    xaxis_title='Genre List',
    yaxis_title='Frequency',
)

# Adding hover text for more information
genre_fig3.update_traces(text=top_genre_lists_df['Count'], textposition='outside')

# Adjusting the size and appearance of the figure
genre_fig3.update_layout(
    margin=dict(l=50, r=50, t=80, b=80),
)
