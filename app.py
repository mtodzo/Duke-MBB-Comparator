import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
from PlayerDataTracker import PlayerDataTracker


app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

pdt = PlayerDataTracker()
playerList = pdt.getPlayers()

playerGraphs = []
for player in playerList:
    p = go.Scatter(
        x = player.getGameNos(),
        y = player.getAverageEffs(),
        mode = 'lines',
        name = player.getName()
    )
    playerGraphs.append(p)

app.layout = html.Div([
    html.H2('Hello, Team!'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['Justin Wei', 'Jonathan Michala', 'Miles Todzo']],
        value='Justin Wei'
    ),
    html.Div(id='display-value'),
    dcc.Graph(
        figure=go.Figure(
            data= playerGraphs,
            layout=go.Layout(
                title='Player Efficacies per Game',
                showlegend=True,
                legend=go.Legend(
                    x=0,
                    y=1.0
                ),
                margin=go.Margin(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
    )
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])

def display_value(value):
    if value == 'Justin Wei':
        return 'Justin Wei is dope!'
    elif value == 'Jonathan Michala':
        return 'Hello, Jonathan! Welcome :-)'
    else:
        return 'Error: Who is Miles Todzo? Serra sucks at basketball'



if __name__ == '__main__':
    app.run_server(debug=True)
