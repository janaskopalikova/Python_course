import dash
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os


app = dash.Dash()
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

#layout
all_options = {
    'Histogram': ['Ethanol by beertax', 'Ethanol by cigtax', 'Skin colour + employ', 'Age by family size', 'Living area by age', 'Education by living area'],
    'Boxplot': ['Work status vs. unemployment rate', 'Work status vs. age', 'Work status vs. education', 'Health vs. education', 'Health vs. age']
}
markdown_text = 'Interactive application displays these [data](https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/wooldridge/alcohol.csv) about alcohol users in USA (no year or advanced information about investigation found)'

app.layout = html.Div(style={'padding-top': '30px', 'padding-bottom': '50px', 'padding-left': '80px', 'padding-right': '80px', 'backgroundColor': '#b4d8ee', 'font-family': 'sans-serif'},
children=[
    html.H1(children='Alcohol fairy tale: What we know about alcohol users from USA?', style={'color': '#000455', 'textAlign': 'center', 'fontSize': "36", 'font-weight': 'bold'}),
    html.H3(dcc.Markdown(children=markdown_text), style={'color': '#000455', 'fontSize': "16", 'textAlign': 'center'}),
    html.H3(children='Options:', style={'color': '#000455', 'fontSize': "20", 'font-weight': 'bold'}),

    dcc.RadioItems(
        id='radio-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Histogram'
    ),

    html.Br(),

    dcc.Dropdown(id='plot-dropdown'),

    html.Br(),
    dcc.Graph(id='example-graph')
])

#radioitems + dropdown
@app.callback(
    dash.dependencies.Output('plot-dropdown', 'options'),
    [dash.dependencies.Input('radio-dropdown', 'value')])
def set_plot_options(selected_plot):
    return [{'label': i, 'value': i} for i in all_options[selected_plot]]


@app.callback(
    dash.dependencies.Output('plot-dropdown', 'value'),
    [dash.dependencies.Input('plot-dropdown', 'options')])
def set_plot_value(available_options):
    return available_options[0]['value']

#graphs
@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('plot-dropdown', 'value'),
     dash.dependencies.Input('radio-dropdown', 'value')])

def update_figure(graph_type,plot_type):
    if graph_type == 'Work status vs. unemployment rate':
        trace1 = go.Box(y = alcohol.loc[(alcohol.status == 1)].unemrate, name = 'out of workforce')
        trace2 = go.Box(y = alcohol.loc[(alcohol.status == 2)].unemrate, name = 'unemployed')
        trace3 = go.Box(y = alcohol.loc[(alcohol.status == 3)].unemrate, name = 'employed')
        layout = go.Layout(showlegend = True, title = 'Work status vs. unemployment rate', xaxis=dict(title="Work status"), yaxis=dict(title="Unemployment rate (%)"))
        data = [trace1, trace2, trace3]

    elif graph_type == 'Work status vs. age':
        trace1 = go.Box(y = alcohol.loc[(alcohol.status == 1)].age, name = 'out of workforce')
        trace2 = go.Box(y = alcohol.loc[(alcohol.status == 2)].age,name = 'unemployed')
        trace3 = go.Box(y = alcohol.loc[(alcohol.status == 3)].age,name = 'employed')
        layout = go.Layout(showlegend = True, title = 'Work status vs. age', xaxis=dict(title="Work status"), yaxis=dict(title="Age (years)"))
        data = [trace1, trace2, trace3]

    elif graph_type == 'Work status vs. education':
        trace1 = go.Box(y = alcohol.loc[(alcohol.status == 1)].educ, name = 'out of workforce')
        trace2 = go.Box(y = alcohol.loc[(alcohol.status == 2)].educ, name = 'unemployed')
        trace3 = go.Box(y = alcohol.loc[(alcohol.status == 3)].educ, name = 'employed')
        layout = go.Layout(showlegend = True, title = 'Work status vs. education',xaxis=dict(title="Work status"),yaxis=dict(title="Education (years of schooling)"))
        data = [trace1, trace2, trace3]

    elif graph_type == 'Health vs. education':
        trace1 = go.Box(y = alcohol.loc[(alcohol.exhealth == 1)].educ, name = 'excellent health')
        trace2 = go.Box(y = alcohol.loc[(alcohol.vghealth == 1)].educ, name = 'very good health')
        trace3 = go.Box(y = alcohol.loc[(alcohol.goodhealth == 1)].educ, name = 'good health')
        trace4 = go.Box(y = alcohol.loc[(alcohol.fairhealth == 1)].educ, name = 'fair health')
        layout = go.Layout(showlegend = True, title = 'Health vs. education', xaxis=dict(title="Health"), yaxis=dict(title="Education (years of schooling)"))
        data = [trace1, trace2, trace3, trace4]

    elif graph_type == 'Health vs. age':
        trace1 = go.Box(y = alcohol.loc[(alcohol.exhealth == 1)].age, name = 'excellent health')
        trace2 = go.Box(y = alcohol.loc[(alcohol.vghealth == 1)].age, name = 'very good health')
        trace3 = go.Box(y = alcohol.loc[(alcohol.goodhealth == 1)].age, name = 'good health')
        trace4 = go.Box(y = alcohol.loc[(alcohol.fairhealth == 1)].age, name = 'fair health')
        layout = go.Layout(showlegend = True, title = 'Health vs. age', xaxis=dict(title="Health"), yaxis=dict(title="Age (years)"))
        data = [trace1, trace2, trace3, trace4]

    elif graph_type == 'Ethanol by beertax':
        trace1 = go.Histogram(x=alcohol[alcohol.beertax < 0.5].ethanol, opacity=0.75, name = 'tax < 0.5 $ per gallon')
        trace2 = go.Histogram(x=alcohol[alcohol.beertax.between(0.5, 1.5, inclusive=False)].ethanol, opacity=0.75, name = 'tax = 0.5-1.5 $ per gallon')
        trace3 = go.Histogram(x=alcohol[alcohol.beertax > 1.5].ethanol, opacity=0.75, name = 'tax > 1.5 $ per gallon')
        data = [trace1, trace2, trace3]
        layout = go.Layout(barmode = 'overlay', title = 'Ethanol by beertax', showlegend=True, xaxis=dict(title="State per-capita ethanol consumption (gallons ?)"))

    elif graph_type == 'Ethanol by cigtax':
        trace1 = go.Histogram(x=alcohol[alcohol.cigtax < 15].ethanol, opacity=0.75, name = 'tax < 15 cents per pack')
        trace2 = go.Histogram(x=alcohol[alcohol.cigtax.between(15, 25, inclusive=False)].ethanol, opacity=0.75, name = 'tax = 15-25 cents per pack')
        trace3 = go.Histogram(x=alcohol[alcohol.cigtax > 25].ethanol, opacity=0.75, name = 'tax > 25 cents per pack')
        data = [trace1, trace2, trace3]
        layout = go.Layout(barmode = 'overlay', title = 'Ethanol by cigtax', showlegend=True, xaxis=dict(title="State per-capita ethanol consumption (gallons ?)"))

    elif graph_type == 'Skin colour + employ':
        trace1=go.Histogram(x=alcohol[alcohol.white==1].employ, opacity=0.75, name='employed')
        trace3=go.Histogram(x=alcohol[alcohol.white==0].employ, opacity=0.75, name='unemployed')
        data=[trace1,trace3]
        layout=go.Layout(barmode='overlay', title='Skin colour + employ', showlegend=True, xaxis=dict(title="white"))

    elif graph_type == 'Age by family size':
        trace1=go.Histogram(x=alcohol[alcohol.famsize<3].age, opacity=0.75, name='1-2familysize')
        trace3=go.Histogram(x=alcohol[alcohol.famsize>2].age, opacity=0.75, name='>=3familysize')
        data=[trace1,trace3]
        layout=go.Layout(barmode='overlay', title='Age by familysize', showlegend=True, xaxis=dict(title="years"))

    elif graph_type == 'Living area by age':
        trace1=go.Histogram(x=alcohol[(alcohol.northeast==1)].age, name='northeast')
        trace2=go.Histogram(x=alcohol[(alcohol.midwest==1)].age, name='midwest')
        trace3=go.Histogram(x=alcohol[(alcohol.south==1)].age, name='south')
        trace4=go.Histogram(x=alcohol.loc[(alcohol.centcity==1)].age, name='centra lcity')
        trace5=go.Histogram(x=alcohol.loc[(alcohol.outercity==1)].age, name='outer city')
        layout=go.Layout(showlegend=True, title='Living area by age', xaxis=dict(title="years"))
        data = [trace1, trace2, trace3, trace4, trace5]

    elif graph_type == 'Education by living area':
        trace1=go.Histogram(x=alcohol[(alcohol.northeast==1)].educ, name='northeast')
        trace2=go.Histogram(x=alcohol[(alcohol.midwest==1)].educ, name='midwest')
        trace3=go.Histogram(x=alcohol[(alcohol.south==1)].educ, name='south')
        trace4=go.Histogram(x=alcohol.loc[(alcohol.centcity==1)].educ, name='central city')
        trace5=go.Histogram(x=alcohol.loc[(alcohol.outercity==1)].educ, name='outer city')
        layout=go.Layout(showlegend=True, title='Education by living area', xaxis=dict(title="years of schooling"))
        data=[trace1,trace2,trace3,trace4,trace5]

    else:
        trace1 = go.Histogram(x=alcohol[alcohol.beertax < 0.5].ethanol, opacity=0.75, name = 'tax < 0.5')
        trace2 = go.Histogram(x=alcohol[alcohol.beertax.between(0.5, 1.5, inclusive=False)].ethanol, opacity=0.75, name = 'tax = 0.5-1.5')
        trace3 = go.Histogram(x=alcohol[alcohol.beertax > 1.5].ethanol, opacity=0.75, name = 'tax > 1.5')
        data = [trace1, trace2, trace3]
        layout = go.Layout(barmode = 'overlay', title = 'Ethanol by beertax')

    figure = {'data': data, 'layout': layout}
    return figure

#loading dataset
alcohol = pd.read_csv('https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/master/csv/wooldridge/alcohol.csv')

if __name__ == '__main__':
    app.run_server()
