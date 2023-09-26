from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd


df = pd.read_csv("data/supermarket_sales - Sheet1.csv")
df['Date'] = pd.to_datetime(df['Date'])
df.rename(columns={'gross income': 'Gross Income'}, inplace=True)

img = dbc.CardImg(src="static/images/logo.png",
                  style={'position': 'absolute', 'bottom': '10px'})

git = dbc.CardImg(src="static/images/github.png",
                  style={'height': '3.5vh', 'width': '1.8vw',
                         'margin-left': '1vw'})

linkedin = dbc.CardImg(src="static/images/linkedin.png",
                       style={'height': '3.5vh', 'width': '1.8vw',
                              'margin-left': '1vw'})

insta = dbc.CardImg(src="static/images/insta.png",
                    style={'height': '3.5vh', 'width': '1.8vw',
                           'margin-left': '1vw'})

content_descricao = html.Div(
    [
        dbc.Button(
            "Project:",
            id="collapse-button",
            className="mb-1",
            color="secondary",
            n_clicks=0,
            size='sm',
            outline=True,
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody(
                "Supermarket sales data analysis in the USA"),
                inverse=False),
            id="collapse",
            is_open=True,
        ),
    ]
)


switches = html.Div(
    [
        dbc.Label("Cities:"),
        dbc.Checklist(
            options=[{"label": i, "value": i} for i in df['City'].unique()],
            value=df['City'].unique(),
            id="switches-input",
            switch=True,

        ),
    ]
)


radios = html.Div(
    [
        dbc.Label("Analysis by:"),
        dbc.RadioItems(
            id="radio-selected-style",
            options=[{"label": 'Gross Income', "value": 'Gross Income'},
                     {"label": 'Rating', "value": 'Rating'}],
            labelCheckedClassName="text-success",
            inputCheckedClassName="border border-success bg-success",
            value='Gross Income'
        )

    ]
)


content = [html.Div(
    dbc.Container(
        [
            html.H2("Data Clarity", style={
                    "font-family": "uniform black", "font-size": "32px",
                    "text-align": "center", 'font-weight': 'bold'}),
            html.Hr(className="my-2"),
            html.Br(),
            content_descricao,
            html.Hr(className="my-2"),
            switches,
            html.Hr(className="my-2"),
            radios,
            html.Div([
                dbc.NavLink(git, href="https://emsamarante.github.io/",
                            external_link=True),
                dbc.NavLink(linkedin, href="https://www.linkedin.com/in/eduardo-amarante/",
                            external_link=True),
                dbc.NavLink(insta, href="https://www.instagram.com/dataclarityllc/",
                            external_link=True)
            ], style={'bottom': '3vh',
                      'height': '6vh', 'width': '10vw',
                      'display': 'flex',
                      'justify-content': 'space-between',
                      'align-items': 'center',
                      'position': 'fixed'})
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 rounded-3",
)]

aside = dbc.Card(content,
                 style={
                     'height': '95vh', 'margin-left': '20px', 'padding': '1px',
                     "margin-top": "20px"})

left = dbc.Col([aside,
                ], sm=2)


# lado direito do dash
# Graficos
l11 = html.Div(children=[
               dcc.Graph(id='city_fig', style={
                         'height': '35vh'})
               ])

l12 = html.Div(children=[
               dcc.Graph(id='pay_fig', style={'height': '35vh'})
               ])

l13 = html.Div(children=[
               dcc.Graph(id='gender_fig', style={'height': '35vh'})
               ])


l21 = html.Div(children=[
               dcc.Graph(id='income_per_date', style={'height': '30vh'})
               ])


l31 = html.Div(children=[
               dcc.Graph(id='income_per_product', style={'height': '30vh'})
               ])

linha1 = dbc.Row([
    dbc.Col([l11], sm=4),
    dbc.Col([l12], sm=4),
    dbc.Col([l13], sm=4)
], style={'height': '35vh'})

linha2 = dbc.Row([l21], style={'height': '30vh'})

linha3 = dbc.Row([l31], style={'height': '25vh'})

right = dbc.Col(
    dbc.Row([
        linha1,
        linha2,
        linha3
    ]),
    sm=10)


# Definindo o layout
layout = html.Div([
    dbc.Row([
        left,
        right
    ], style={'height': '5vh'})


])
