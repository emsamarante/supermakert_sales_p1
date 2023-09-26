import dash
from dash.dependencies import Output, Input, State
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

from layouts import layout, df
import numpy as np
import plotly.express as px


load_figure_template("minty")
app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
app.title = "Dashboard de Vendas"
app._favicon = "logo.ico"


app.layout = layout


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [Output('city_fig', 'figure'),
     Output('pay_fig', 'figure'),
     Output('gender_fig', 'figure'),
     Output('income_per_date', 'figure'),
     Output('income_per_product', 'figure')
     ],

    [Input("switches-input", 'value'),
     Input("radio-selected-style", 'value')]
)
def update_graph(cities_selected, variable_selected):
    operation = np.sum if variable_selected == "Gross Income" else np.mean

    if (variable_selected == "Gross Income"):
        texto = "Sum"
    else:
        texto = "Average"

    df_filtered = df[df['City'].isin(cities_selected)]
    df_city = df_filtered.groupby("City")[variable_selected].apply(
        operation).to_frame().reset_index()

    df_gender = df_filtered.groupby(["Gender", "City"])[variable_selected].apply(
        operation).to_frame().reset_index()

    df_payment = df_filtered.groupby("Payment")[variable_selected].apply(
        operation).to_frame().reset_index()

    df_income_time = df_filtered.groupby("Date")[variable_selected].apply(
        operation).to_frame().reset_index()

    df_product_income = df_filtered.groupby(["Product line", "City"])[variable_selected].apply(
        operation).to_frame().reset_index()

    fig_city = px.bar(df_city, x='City', y=variable_selected,
                      title=f"<b>{texto} of {variable_selected} by City<b>")

    fig_gender = px.bar(df_gender, x='Gender',
                        y=variable_selected, barmode="group", color='City',
                        title=f"<b>{texto} of {variable_selected} by Gender<b>")

    fig_payment = px.bar(df_payment, y='Payment', x=variable_selected,
                         title=f"<b>{texto} of {variable_selected} by Type of Payment<b>")

    fig_income = px.bar(df_product_income, x='Product line',
                        y=variable_selected, color='City', barmode='group',
                        title=f"<b>{texto} of {variable_selected} by Product line<b>")

    fig_income_date = px.bar(df_income_time, x='Date',
                             y=variable_selected,
                             title=f"<b>{texto} of {variable_selected} by Date<b>")

    for fig in [fig_city, fig_gender, fig_payment, fig_income, fig_income_date]:
        fig.update_layout(
            margin={'l': 60, 'b': 40, 't': 70}, template='minty',
            title=dict(font=dict(size=18),
                       automargin=False, yref='paper'), title_x=0,
        )
    fig_payment.update_layout(
        margin={'l': 60, 'b': 40, 't': 70}, template='minty',
        title=dict(font=dict(size=18),
                   automargin=False, yref='paper'), title_x=0,
        yaxis_title=None,
    )

    return fig_city, fig_gender, fig_payment, fig_income_date, fig_income


app.run_server(debug=False, port=8050, host='0.0.0.0')
