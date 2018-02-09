import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
from PlayerDataTracker import PlayerDataTracker
from TeamDataTracker import TeamDataTracker

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
dcc._css_dist[0]['relative_package_path'].append('styles.css')

pdt = PlayerDataTracker()
tdt = TeamDataTracker()

playerList = pdt.getPlayers()
teamList = tdt.getTeams()

playerGraphs = {}
teamGraphs = {}

def createPlayerGraphs():
    for player in playerList:
        p = go.Scatter(
            x = player.getGameNos(),
            y = player.getAverageEffs(),
            mode = 'lines',
            name = player.getName()
        )
        playerGraphs[player.getName()] = p

def createTeamGraphs():
    for team in teamList:
        p = go.Scatter(
            x = team.getGameNos(),
            y = team.getAverageEffs(),
            mode = 'lines',
            name = team.getName()
        )
        teamGraphs[team.getName()] = p

createPlayerGraphs()
createTeamGraphs()

# generates player dropdown
def generatePlayerDropdown(selectorID):
    complete_data = []
    values = []
    if selectorID == 'player-selector':
        for player in playerList:
            data = {}
            data['label'] = player.name
            data['value'] = player.name
            values.append(player)
            complete_data.append(data)
    else:
        for team in teamList:
            data = {}
            data['label'] = team.name
            data['value'] = team.name
            values.append(team)
            complete_data.append(data)
    sorted_data = sorted(complete_data, key=lambda k: k['label'])

    return dcc.Dropdown(
        id=selectorID,
        options= sorted_data,
        multi=True,
        )

app.layout = html.Div(children = [
    html.H2(style={'text-align':'center'}, children=['Compare Dukie Ballers!']),
    html.Div(
        className='graph-container',
        style={
    		'width':'100%',
        	'margin':'auto',
        	'overflow':'hidden',
            'display': 'inline-block'
        },

        children = [

            # PLAYER GRAPH
            html.Div(
                id='players-div',
                children = [
                    # PLAYER SELECTION
                    html.H3('Pick Players to Compare:'),
                    generatePlayerDropdown('player-selector'),
                    dcc.Graph(
                        id='player-graph'
                    )
                ],
                style = {
                    'width': '48%',
                    'float': 'left',
                    'padding': '5px'
                }
            ),
            # TEAM GRAPH
            html.Div(
                id='teams-div',
                children = [
                    # PLAYER SELECTION
                    html.H3('Pick Teams to Compare:'),
                    generatePlayerDropdown('team-selector'),
                    dcc.Graph(
                        id='team-graph'
                    )
                ],
                style = {
                    'width': '48%',
                    'float': 'right'
                }
            )
        ]
    )
])

@app.callback(dash.dependencies.Output('player-graph', 'figure'),
              [dash.dependencies.Input('player-selector', 'value')])

def player_selector_callback(playerNames):

    playersToGraph = []
    if playerNames:
        for pn in playerNames:
            playersToGraph.append(playerGraphs[pn])
    return {
        'data': playersToGraph,
        'layout': go.Layout(
            title='Average Player Efficiency Over Season',
            xaxis={'title': 'Games Into Season', 'range': [0, 40]},
            yaxis={'title': 'Player Efficiency', 'range': [0, 40]},
            showlegend=True,
        ),
    }

@app.callback(dash.dependencies.Output('team-graph', 'figure'),
              [dash.dependencies.Input('team-selector', 'value')])

def team_selector_callback(teamNames):

    teamsToGraph = []
    if teamNames:
        for tn in teamNames:
            teamsToGraph.append(teamGraphs[tn])
    return {
        'data': teamsToGraph,
        'layout': go.Layout(
            title='Average Team Offensive Rating Over Season',
            xaxis={'title': 'Games Into Season', 'range': [0, 40]},
            yaxis={'title': 'Offensive Rating', 'range': [50, 150]},
            showlegend=True,
        ),
    }

if __name__ == '__main__':
    app.run_server(debug=True)
