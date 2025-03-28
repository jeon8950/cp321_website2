import numpy as np 
import pandas as pd 
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.graph_objs as go

#step 1
data = [
    {"Year": 1930, "Winner": "Uruguay", "Runner-up": "Argentina"},
    {"Year": 1934, "Winner": "Italy", "Runner-up": "Czechoslovakia"},
    {"Year": 1938, "Winner": "Italy", "Runner-up": "Hungary"},
    {"Year": 1950, "Winner": "Uruguay", "Runner-up": "Brazil"},
    {"Year": 1954, "Winner": "Germany", "Runner-up": "Hungary"},
    {"Year": 1958, "Winner": "Brazil", "Runner-up": "Sweden"},
    {"Year": 1962, "Winner": "Brazil", "Runner-up": "Czechoslovakia"},
    {"Year": 1966, "Winner": "England", "Runner-up": "Germany"},
    {"Year": 1970, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1974, "Winner": "Germany", "Runner-up": "Netherlands"},
    {"Year": 1978, "Winner": "Argentina", "Runner-up": "Netherlands"},
    {"Year": 1982, "Winner": "Italy", "Runner-up": "Germany"},
    {"Year": 1986, "Winner": "Argentina", "Runner-up": "Germany"},
    {"Year": 1990, "Winner": "Germany", "Runner-up": "Argentina"},
    {"Year": 1994, "Winner": "Brazil", "Runner-up": "Italy"},
    {"Year": 1998, "Winner": "France", "Runner-up": "Brazil"},
    {"Year": 2002, "Winner": "Brazil", "Runner-up": "Germany"},
    {"Year": 2006, "Winner": "Italy", "Runner-up": "France"},
    {"Year": 2010, "Winner": "Spain", "Runner-up": "Netherlands"},
    {"Year": 2014, "Winner": "Germany", "Runner-up": "Argentina"},
    {"Year": 2018, "Winner": "France", "Runner-up": "Croatia"},
    {"Year": 2022, "Winner": "Argentina", "Runner-up": "France"}
]

df = pd.DataFrame(data)

df.to_csv("Fifa_WorldCup_Finals.csv", index = False)

print(df)




app = Dash()
server = app.server
winners = sorted(df["Winner"].unique())
years = sorted(df["Year"].unique())
app.layout=[
    html.Div(children='FIFA World Cup Winners and Runner ups'), 
    html.Button("Show winning countries", id = 'winner-button', n_clicks=0 ),
    html.Div(id="winners-output"),
    html.Hr(),
    html.Label("Select a Country"),
    dcc.Dropdown(
        id = "country-dropdown",
        options = [{"label": country, "value": country} for country in winners],
        placeholder = "choose a country"
    ),
    html.Div(id = "win-count"),
    html.Hr(),
    html.Label("Select a year"),
    dcc.Dropdown(
        id = "year-dropdown",
        options = [{"label" : year, "value" : year} for year in years],
        placeholder = "choose a year"
    ),
    html.Div(id = 'year-output'),
    html.Hr(),
    dash_table.DataTable(data=df.to_dict('records'))
]
@app.callback(
    Output("winners-output", "children"),
    Input("winner-button", "n_clicks")
)

def show_winners(n_clicks):
    if n_clicks>0:
        return html.Ul([html.Li(country) for country in winners])
    return ""

@app.callback(
    Output("win-count", "children"),
    Input("country-dropdown", "value")
)

def show_win_count(selected_country):
    if selected_country:
        win_count = df[df["Winner"] == selected_country].shape[0]
        return html.H3(f"{selected_country} has won the World Cup {win_count} times")
    return ""

@app.callback(
    Output("year-output", "children"),
    Input("year-dropdown", "value")
)

def show_year_result(selected_year):
    if selected_year:
        match = df[df["Year"] == selected_year]
        if not match.empty:
            winner =match["Winner"].values[0]
            runnerup = match["Runner-up"].values[0]
            return html.H3(f"In {selected_year}, {winner} won the World Cup and {runnerup} was the runner-up.")
    return ""
            
if __name__== '__main__':
    app.run(debug=True)
