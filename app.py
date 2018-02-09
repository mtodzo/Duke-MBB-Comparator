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

playerGraphs = {}

def createPlayerGraphs():
    for player in playerList:
        p = go.Scatter(
            x = player.getGameNos(),
            y = player.getAverageEffs(),
            mode = 'lines',
            name = player.getName()
        )
        playerGraphs[player.getName()] = p

createPlayerGraphs()

# generates player dropdown
def generatePlayerDropdown(selectorID):
    complete_data = []
    values = []
    for player in playerList:
        data = {}
        data['label'] = player.name
        data['value'] = player.name
        values.append(player)
        complete_data.append(data)
    return dcc.Dropdown(
        id=selectorID,
        options= complete_data,
        multi=True,
        )

app.layout = html.Div([
    html.H2('Compare Dukie Ballers!'),

    # PLAYER SELECTION
    html.H3('Pick Players to Compare:'),
    generatePlayerDropdown('player1-selector'),

    html.Div(id='display-value'),
    dcc.Graph(id='player-graph'),
])

@app.callback(dash.dependencies.Output('player-graph', 'figure'),
              [dash.dependencies.Input('player1-selector', 'value')])

def player_1_selector_callback(playerNames):
    playersToGraph = []
    for pn in playerNames:
        playersToGraph.append(playerGraphs[pn])
    return {
        'data': playersToGraph,
        'layout': go.Layout(
            title='Average Player Efficiency Over Season',
            showlegend=True,
            margin=go.Margin(l=40, r=0, t=40, b=30)
        ),
        'style': {'height': 300},
    }


if __name__ == '__main__':
    app.run_server(debug=True)
