import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

world_cup_data = [
    {"Year": 1930, "Winner": "Uruguay", "Runner_Up": "Argentina", "Venue": "Estadio Centenario", "Location_City": "Montevideo", "Location_Country": "Uruguay", "Attendance": 68346},
    {"Year": 1934, "Winner": "Italy", "Runner_Up": "Czechoslovakia", "Venue": "Stadio Nazionale PNF", "Location_City": "Rome", "Location_Country": "Italy", "Attendance": 55000},
    {"Year": 1938, "Winner": "Italy", "Runner_Up": "Hungary", "Venue": "Stade Olympique de Colombes", "Location_City": "Paris", "Location_Country": "France", "Attendance": 45000},
    {"Year": 1950, "Winner": "Uruguay", "Runner_Up": "Brazil", "Venue": "Maracanã Stadium", "Location_City": "Rio de Janeiro", "Location_Country": "Brazil", "Attendance": 173850},
    {"Year": 1954, "Winner": "Germany", "Runner_Up": "Hungary", "Venue": "Wankdorf Stadium", "Location_City": "Bern", "Location_Country": "Switzerland", "Attendance": 62500},
    {"Year": 1958, "Winner": "Brazil", "Runner_Up": "Sweden", "Venue": "Råsunda Stadium", "Location_City": "Solna", "Location_Country": "Sweden", "Attendance": 49737},
    {"Year": 1962, "Winner": "Brazil", "Runner_Up": "Czechoslovakia", "Venue": "Estadio Nacional", "Location_City": "Santiago", "Location_Country": "Chile", "Attendance": 68679},
    {"Year": 1966, "Winner": "England", "Runner_Up": "Germany", "Venue": "Wembley Stadium", "Location_City": "London", "Location_Country": "England", "Attendance": 96924},
    {"Year": 1970, "Winner": "Brazil", "Runner_Up": "Italy", "Venue": "Estadio Azteca", "Location_City": "Mexico City", "Location_Country": "Mexico", "Attendance": 107412},
    {"Year": 1974, "Winner": "Germany", "Runner_Up": "Netherlands", "Venue": "Olympiastadion", "Location_City": "Munich", "Location_Country": "Germany", "Attendance": 78000},
    {"Year": 1978, "Winner": "Argentina", "Runner_Up": "Netherlands", "Venue": "Estadio Monumental", "Location_City": "Buenos Aires", "Location_Country": "Argentina", "Attendance": 71483},
    {"Year": 1982, "Winner": "Italy", "Runner_Up": "Germany", "Venue": "Santiago Bernabéu", "Location_City": "Madrid", "Location_Country": "Spain", "Attendance": 90000},
    {"Year": 1986, "Winner": "Argentina", "Runner_Up": "Germany", "Venue": "Estadio Azteca", "Location_City": "Mexico City", "Location_Country": "Mexico", "Attendance": 114600},
    {"Year": 1990, "Winner": "Germany", "Runner_Up": "Argentina", "Venue": "Stadio Olimpico", "Location_City": "Rome", "Location_Country": "Italy", "Attendance": 73603},
    {"Year": 1994, "Winner": "Brazil", "Runner_Up": "Italy", "Venue": "Rose Bowl", "Location_City": "Pasadena", "Location_Country": "United States", "Attendance": 94194},
    {"Year": 1998, "Winner": "France", "Runner_Up": "Brazil", "Venue": "Stade de France", "Location_City": "Saint-Denis", "Location_Country": "France", "Attendance": 80000},
    {"Year": 2002, "Winner": "Brazil", "Runner_Up": "Germany", "Venue": "International Stadium", "Location_City": "Yokohama", "Location_Country": "Japan", "Attendance": 69029},
    {"Year": 2006, "Winner": "Italy", "Runner_Up": "France", "Venue": "Olympiastadion", "Location_City": "Berlin", "Location_Country": "Germany", "Attendance": 69000},
    {"Year": 2010, "Winner": "Spain", "Runner_Up": "Netherlands", "Venue": "Soccer City", "Location_City": "Johannesburg", "Location_Country": "South Africa", "Attendance": 84490},
    {"Year": 2014, "Winner": "Germany", "Runner_Up": "Argentina", "Venue": "Maracanã Stadium", "Location_City": "Rio de Janeiro", "Location_Country": "Brazil", "Attendance": 74738},
    {"Year": 2018, "Winner": "France", "Runner_Up": "Croatia", "Venue": "Luzhniki Stadium", "Location_City": "Moscow", "Location_Country": "Russia", "Attendance": 78011},
    {"Year": 2022, "Winner": "Argentina", "Runner_Up": "France", "Venue": "Lusail Stadium", "Location_City": "Lusail", "Location_Country": "Qatar", "Attendance": 88966},
    {"Year": 2026, "Winner": None, "Runner_Up": None, "Venue": "MetLife Stadium", "Location_City": "East Rutherford", "Location_Country": "United States", "Attendance": None}
]

df = pd.DataFrame(world_cup_data)

win_counts = df['Winner'].value_counts().reset_index()
win_counts.columns = ['Country', 'Wins']


app = dash.Dash(__name__)

server=app.server

app.title = "FIFA World Cup Dashboard"


app.layout = html.Div(
    style={"backgroundColor": "#000000", "color": "white", "fontFamily": "Arial, sans-serif", "padding": "20px","overflowX": "hidden","boxSizing": "border-box"},
    children=[
        html.H1("FIFA World Cup Finals Dashboard", style={"textAlign": "center", "color": "white"}),

        html.Div([
            html.Label("Select a Country:", style={"color": "white", "fontWeight": "bold"}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{"label": c, "value": c} for c in sorted(win_counts["Country"].unique())],
                value="Brazil",
                style={"backgroundColor": "#1e1e1e", "color": "black"},
            ),
            html.Div(id='country-output', style={"marginTop": "10px", "color": "white"})
        ], style={"width": "48%", "display": "inline-block", "paddingRight": "2%"}),

        html.Div([
            html.Label("Select a Year:", style={"color": "white", "fontWeight": "bold"}),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{"label": int(y), "value": int(y)} for y in sorted(df["Year"].dropna().unique())],
                value=2022,
                style={"backgroundColor": "#1e1e1e", "color": "black"},
            ),
            html.Div(id='year-output', style={"marginTop": "10px", "color": "white"})
        ], style={"width": "48%", "display": "inline-block"}),

        html.Br(), html.Br(),
        

       html.Div([
            dcc.Graph(
                id="choropleth",
                style={"height": "80vh", "width": "90vw"}
            )
        ], style={
            "paddingLeft": "18vw",  # shift it right by 10% of screen width
            "boxSizing": "border-box"
        })


    ])

@app.callback(
    Output('country-output', 'children'),
    Input("country-dropdown", "value")
)
def update_country_output(country):
    wins = win_counts[win_counts["Country"]==country]['Wins'].values[0]
    return f'{country} has won the FIFA World Cup {wins} time(s).'

@app.callback(
    Output('year-output', "children"),
    Input("year-dropdown", 'value')
)
def update_year_output(year):
    row = df[df["Year"]==year]
    if not row.empty and pd.notna(row.iloc[0]['Winner']):
        winner = row.iloc[0]['Winner']
        runner_up = row.iloc[0]['Runner_Up']
        return f'In {year}, {winner} won against {runner_up}.'
    else:
        return f'No data available for the year {year}. TBD'
    
@app.callback(
    Output('choropleth', 'figure'),
    Input("country-dropdown", 'value')
)
def update_map(_):
    fig = px.choropleth(
        win_counts,
        locations="Country",
        locationmode="country names",
        color="Wins",
        color_continuous_scale="Blues",
        title="World Cup Wins by Country"
    )
    fig.update_layout(
        height=700,  
        width=1100, 
        plot_bgcolor="#000000",
        paper_bgcolor="#000000",
        font_color="white"
    )
    fig.update_geos(showcountries=True,
    showcoastlines=True,
    showland=True)

    return fig

if __name__ == "__main__":
    app.run(debug=True)

