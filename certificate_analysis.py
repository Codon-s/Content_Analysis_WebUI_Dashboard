'''Importing Necessary Modules'''
import pandas as pd
import plotly.express as px
from dash_bootstrap_templates import load_figure_template as load_template
from data_cleaning import df

## Loading Bootstrap Template "SLATE"
TEMPLATES = 'slate'
load_template(TEMPLATES)

df.Certificate.fillna('Unrated', inplace=True)

certificate_categories = {
    'UA': 'GA',
    'G': 'GA',
    'TV-G': 'GA',
    'E': 'GA',
    'E10+': 'GA',
    'U': 'GA',
    'TV-Y': 'GA',
    'Approved': 'GA',
    'PG': 'PG',
    'TV-PG': 'PG',
    '12+': 'GA',
    '13+': 'GA',
    'UA 13+': 'GA',
    'TV-13': 'GA',
    'TV-14': 'TM',
    'PG-13': 'PG',
    'T': 'TM',
    '15+': 'TM',
    '16+': 'TM',
    'UA 16+': 'TM',
    'M/PG': 'TM',
    'TV-MA': 'AO',
    'R': 'AO',
    '18+': 'AO',
    'MA-17': 'AO',
    'NC-17': 'AO',
    'TV-18': 'AO',
    'A': 'AO',
    'UA 7+': 'GA',
    '7': 'GA',
    'M': 'TM',
    'GP': 'GA',
    'Unrated': 'Unrated',
    '(Banned)': '(Banned)',
    'TV-Y7-FV': 'PG',
    'TV-Y7': 'GA'
}

df['Category'] = df['Certificate'].map(certificate_categories)

# Figure 1: Frequency of Certificates

certi_counts = df['Certificate'].value_counts().reset_index()
certi_counts.columns = ['Certificate', 'Count']

cert_fig1 = px.bar(
    certi_counts,
    x='Certificate',
    y='Count',
    title='Frequency of Certificates',
    labels={'Ceritifcate': "Certificate Type", 'Count':'Number of Titles'},
    color_discrete_sequence=['rgb(72, 84, 99)']
)

cert_fig1.update_traces(
    text = certi_counts['Count'],
    textposition='outside'
)

# fig.show()

# Figure 2: Frequency of Certificates for Different Categories

def cert_fig2(category):
    '''Function Provides Output of Figure 2, with outlining appropriate
    pie section based on the category'''
    dt = df[df.Category == category]
    dt.Certificate.value_counts()
    result = pd.DataFrame({
        'Certificate' : dt.Certificate.value_counts().keys().to_list(),
        'Values': dt.Certificate.value_counts().values
    })

    fig = px.bar(
        x=result.Certificate,
        y=result.Values,
        labels={'x': 'Certificate', 'y': 'Count'},
        color_discrete_sequence=['rgb(72, 84, 99)']
    )

    fig.update_layout(
        title = 'Frequency of Certificates for Adult Only Category'
    )

    fig.update_traces(
        text = result.Values,
        textposition = 'outside'
    )

    #fig.show()
    return fig
