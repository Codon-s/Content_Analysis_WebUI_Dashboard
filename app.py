''' Importing Necessary Dependencies '''
import pandas as pd
import plotly.graph_objects as go
from dash import html, Dash, dcc, Input, Output, callback, dash_table, ctx
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template as load_template
from data_cleaning import df
from director_analysis import fig1, fig2, fig3, fig4
from genre_analysis import genre_fig1, genre_fig2, genre_fig3
# from certificate_analysis import cert_fig1

## Loading Bootstrap Template "SLATE"
TEMPLATES = 'slate'
load_template(TEMPLATES)

### Dash APP

## Initialilzing Dash APP here
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE], title='Content Analysis Dashboard')

## Code for Tab 1: Director
tab1 = dbc.Card(
        dbc.CardBody([
            html.P('Analysis Based on Directorship.', className='card-text'),
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Row(
                            [
                            dbc.Col(
                                dcc.Graph(
                                    id = 'Director_Figure1',
                                    figure= fig1
                                ), width=6
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id = 'Director_Figure2',
                                    figure= fig2
                                ), width=6
                            )
                        ],justify='evenly', align='center', style={'padding-bottom':'25px'}
                        ),
                        dbc.Row(
                            [
                            dbc.Col(
                                dcc.Graph(
                                    id = 'Director_Figure3',
                                    figure= fig3
                                ), width=6
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id = 'Director_Figure4',
                                    figure= fig4
                                ), width=6
                            )
                        ],justify='evenly', align='center'
                        )
                    ]),
                    dbc.Col([
                        dbc.Container([
                            html.P(id='table_des'),
                            dash_table.DataTable(
                                id='output',
                                style_cell_conditional=[
                                    {'if': {'column_id': 'Title'}, 'width': '60%'},
                                    {'if': {'column_id': 'Release_Year'}, 'width': '40%'}
                                    ],
                                page_size=20, style_table={
                                    'overflowX': 'auto', 
                                    'backgroundColor': 'rgb(36, 41, 46)'}, # Slate theme primary color, # pylint: disable=line-too-long
                                style_cell={
                                    'textAlign': 'left',
                                    #'backgroundColor': 'rgb(48, 54, 60)',  # Darker background for cells, # pylint: disable=line-too-long
                                    #'color': 'white',  # Text color in cells
                                    'whiteSpace': 'normal'
                                },
                                style_header={
                                    'backgroundColor': 'rgb(48, 54, 60)', # Darker background for headers, # pylint: disable=line-too-long
                                    'color': '#aaaaaa', # Text color in headers
                                    'fontWeight': 'bold',
                                    'textAlign': 'center'
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(43, 49, 55)'# Slightly darker background for odd rows, # pylint: disable=line-too-long
                                    },
                                    {
                                        'if': {'row_index': 'even'},
                                        'backgroundColor': 'rgb(48, 54, 60)'# Darker background for even rows, # pylint: disable=line-too-long
                                    },
                                    {
                                        'if': {
                                            'filter_query': '{Column2} > 2',
                                            'column_id': 'Column2'
                                        },
                                        'backgroundColor': 'rgba(255, 0, 0, 0.1)'
                                    }
                                ]
                                ),
                        ], fluid=True)
                    ],width=4)
                ], justify="evenly", align='center')
            ],fluid=True),
        ]),
        className='tab1',
)

## Code for Tab 2: Certificate Tab
# tab2 = dbc.Card(
#     dbc.CardBody([
#         html.P('This is Content here for Certificate.', className='card-text'),
#         dbc.Container([
#             dbc.Row([
#                 dcc.Graph(
#                     id = 'cert_fig1',
#                     figure=cert_fig1
#                 )
#             ], justify='evenly', align='center', style={'padding-bottom': '25px'}),
#             dbc.Row([
#                 dcc.Dropdown(
#                     ['Item1', 'Item2', 'Item3'],
#                     'Item1',
#                     id='dropdown'
#                 ),
#                 dbc.Col(
#                     dcc.Graph(
#                         id='cert_fig2'
#                     )
#                 )
#             ])
#         ], fluid=True)
#     ]),
#     className='tab2'
# )

## Code for Tab 3: Genre
tab3 = dbc.Card(
    dbc.CardBody([
        html.P('This is Content here Genre.', className='card-text'),
        dbc.Container([
            dbc.Row([
                dcc.Graph(
                    id='genre_fig1',
                    figure=genre_fig1
                )
            ],justify='evenly', align='center', style={'padding-bottom':'25px'}),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(
                        id='genre_fig2',
                        figure=genre_fig2
                    ),width=4
                ),
                dbc.Col(
                    dcc.Graph(
                        id='genre_figUpdate'
                    ), width=4
                ),
                dbc.Col(
                    dcc.Graph(
                        id='genre_fig3',
                        figure=genre_fig3
                    ), width=4
                )
            ], justify= 'evenly')
        ],fluid=True)
    ]),
    className='tab3'
)

## Dash Layout
app.layout = html.Div([
    html.H1(
        id='title',
        children = 'Content Analysis Dashboard',
        style={'textAlign': 'center', 'margin_top': '25px'}
    ),
    dbc.Tabs([
        dbc.Tab(tab1, label='Director'),
        # dbc.Tab(tab2, label='Certificate'),  # Tab 2: Certificate
        dbc.Tab(tab3, label='Genre')
    ])
],  style={"backgroundColor": "rgb(44, 48, 54)"}  # Set dark gray background color
)

## Callback for Tab 1: Director
@callback(
    [Output('table_des', 'children'), Output('output', 'data'), Output('output', 'columns')],
    Input('Director_Figure1', 'hoverData'),
    Input('Director_Figure2', 'hoverData'),
    Input('Director_Figure3', 'hoverData'),
    Input('Director_Figure4', 'hoverData')
)
def update_output_director(value, value2, value3, value4):
    '''Callback Update for Director'''
    if ctx.triggered:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == 'Director_Figure1':
            if value is not None:
                inlist = value['points'][0]['pointNumbers']
                dt = df.loc[inlist]
                dt = dt[['Title', 'Director']]
                for i in dt.index:
                    if dt.Director.loc[i] == 'Not Available':
                        continue
                    a = dt.Director.loc[i]
                    dt.at[i, 'Director'] = ','.join(a)

                description = 'Saturation of Directors in different Ratings'
                return description, dt.to_dict('records'), [{'id':c, 'name': c} for c in dt.columns]
            dt = df.head(20)
            dt = dt[['Title', 'Director']]
            for i in dt.index:
                if dt.Director.loc[i] == 'Not Available':
                    continue
                a = dt.Director.loc[i]
                dt.at[i, 'Director'] = ','.join(a)

            description = "Hover on any Field to update Table."
            return description, dt.to_dict('records'), [{'id':c, 'name': c} for c in dt.columns]
        if trigger == 'Director_Figure2':
            if value2 is not None:
                platform = value2['points'][0]['label']
                dt = df.loc[df.Platform == platform]
                dt = dt[['Title', 'Director']]
                for i in dt.index:
                    if dt.Director.loc[i] == 'Not Available':
                        continue
                    a = dt.Director.loc[i]
                    dt.at[i, 'Director'] = ','.join(a)
                description = 'Distribution of Directions in different Platforms'
                return description, dt.to_dict('records'), [{'id':c, 'name': c} for c in dt.columns]
            dt = df.head(20)
            dt = dt[['Title', 'Director']]
            for i in dt.index:
                if dt.Director.loc[i] == 'Not Available':
                    continue
                a = dt.Director.loc[i]
                dt.at[i, 'Director'] = ','.join(a)

            description = "Hover on any Field to update Table."
            return description, dt.to_dict('records'), [{'id':c, 'name': c} for c in dt.columns]
        if trigger == 'Director_Figure3':
            if value3 is not None:
                director = value3['points'][0]['x']
                dt = df.loc[df.Director.apply(lambda x: director in x)]
                dt = dt[['Title', 'Director']]
                for i in dt.index:
                    if dt.Director.loc[i] == 'Not Available':
                        continue
                    a = dt.Director.loc[i]
                    dt.at[i, 'Director'] = ','.join(a)

                description = "Top 10 Most Active Directors."
                return description, dt.to_dict('records'), [{'id':c, 'name': c} for c in dt.columns]
            dt = df.head(20)
            dt = dt[['Title', 'Director']]
            for i in dt.index:
                if dt.Director.loc[i] == 'Not Available':
                    continue
                a = dt.Director.loc[i]
                dt.at[i, 'Director'] = ','.join(a)

            description = "Hover on any Field to update Table."
            return description, dt.to_dict('records'), [{'id':c, 'name': c} for c in dt.columns]
        if trigger == 'Director_Figure4':
            if value4 is not None:
                director = value4['points'][0]['x']
                dt = df.loc[df.Director.apply(lambda x: director in x)]
                dt = dt[['Title', 'Director']]
                for i in dt.index:
                    if dt.Director.loc[i] == 'Not Available':
                        continue
                    a = dt.Director.loc[i]
                    dt.at[i, 'Director'] = ','.join(a)

                description = "Movie Ratings by Genre and Director."
                return description, dt.to_dict('records'), [{'id':c, 'name': c} for c in dt.columns]
            dt = df.head(20)
            dt = dt[['Title', 'Director']]
            for i in dt.index:
                if dt.Director.loc[i] == 'Not Available':
                    continue
                a = dt.Director.loc[i]
                dt.at[i, 'Director'] = ','.join(a)

            description = "Hover on any Field to update Table."
            return description, dt.to_dict('records'), [{'id':c, 'name': c} for c in dt.columns]
    else:
        dt = df.head(20)
        dt = dt[['Title', 'Director']]
        for i in dt.index:
            if dt.Director.loc[i] == 'Not Available':
                continue
            a = dt.Director.loc[i]
            dt.at[i, 'Director'] = ','.join(a)

        description = "Hover on any Field to update Table."
        return description, dt.to_dict('records'), [{'id':c, 'name': c} for c in dt.columns]

## Callback for Tab 2: Certificate
# @callback(
#     Output('cert_fig2', 'figure'),
#     Input('dropdown', 'value')
# )
# def update_output(value):
#     print(value)

## Callback for Tab 3: Genre
@callback(
    Output('genre_figUpdate', 'figure'),
    Input('genre_fig2', 'hoverData'),
    Input('genre_fig3', 'hoverData')
)
def update_output_genre(value,value2):
    '''Callback Update for Genre'''
    if ctx.triggered:
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger == 'genre_fig2':
            if value is not None:
                listofindex = []
                for i in df.index:
                    if df.Genre.loc[i] == 'Not Available':
                        continue
                    a = df.Genre.loc[i]
                    for j in a:
                        if j == value['points'][0]['x']:
                            listofindex.append(i)

                filtered_df = df.loc[listofindex]

                a = pd.DataFrame({
                    'Platform': filtered_df['Platform'].value_counts().keys().to_list(),
                    'Count': filtered_df['Platform'].value_counts().values
                })
                genre = 'Genre: '+value['points'][0]['x']
                colors = ['rgb(72, 84, 99)', 'rgb(92, 104, 119)', 'rgb(112, 124, 139)',
                        'rgb(132, 144, 159)', 'rgb(152, 164, 179)', 'rgb(172, 184, 199)']

                fig = go.Figure(
                    data = [
                        go.Pie(
                            labels = a['Platform'],
                            values = a['Count'],
                            marker=dict(colors=colors),
                            textposition='auto'
                        )
                    ]
                )

                fig.update_layout(
                    title=f'Distribution of {genre} across Platforms'
                )

                fig.update_traces(hoverinfo='label+value+percent',
                                textinfo='label+percent',
                                title_font = dict(size=20))
                return fig
            fig = go.Figure(
                data = [
                    go.Pie()
                ]
            )
            fig.update_layout(
                title = 'Hover on Adjacent Graphs to Update'
            )
            return fig

        if trigger == 'genre_fig3':
            if value2 is not None:
                filtered_df = pd.DataFrame(columns=['Genre', 'Platform'])
                for i in df.index:
                    if df.Genre.loc[i] == 'Not Available':
                        continue
                    a = df.Genre.loc[i]
                    a = ','.join(a)
                    temp = value2['points'][0]['x']
                    if a == temp.replace(' ',''):
                        filtered_df.loc[len(filtered_df.index)] = [df.Genre.loc[i], df.Platform.loc[i]] # pylint: disable=line-too-long

                a = filtered_df.groupby(['Platform']).size().reset_index(name='count')
                a = a.sort_values(by='count', ascending=False)
                genre = 'Genre: '+"'"+temp+"'"
                colors = ['rgb(72, 84, 99)', 'rgb(92, 104, 119)', 'rgb(112, 124, 139)',
                        'rgb(132, 144, 159)', 'rgb(152, 164, 179)', 'rgb(172, 184, 199)']

                fig = go.Figure(
                    data = [
                        go.Pie(
                            labels = a['Platform'],
                            values = a['count'],
                            marker=dict(colors=colors),
                            textposition = 'auto'
                        )
                    ]
                )

                fig.update_layout(
                    title = f'Distribution of {genre} across Platforms'
                )

                fig.update_traces(hoverinfo='label+value+percent',
                                textinfo='label+percent',
                                title_font = dict(size=20)
                                )
                return fig
            fig = go.Figure(
                data = [
                    go.Pie()
                ]
            )
            fig.update_layout(
                title = 'Hover on Adjacent Graphs to Update'
            )
            return fig
    else:
        fig = go.Figure(
            data = [
                go.Pie()
            ]
        )
        fig.update_layout(
            title = 'Hover on Adjacent Graphs to Update'
        )
        return fig

if __name__ == '__main__':
    app.run(debug=True)
