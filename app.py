import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import os
from PlayerDataTracker import PlayerDataTracker
from TeamDataTracker import TeamDataTracker
from flask import Flask, send_from_directory


server = Flask(__name__, static_folder='static')
app = dash.Dash(server=server)
app.title = 'DMBB Compare'
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


@server.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(server.root_path, 'static'),
                               'favicon.ico', mimetype='image/favicon.ico')
@server.route('/dmbb-logo.jpg')
def dmbb_logo():
    return send_from_directory(os.path.join(server.root_path, 'static'),
                               'dmbb-logo.jpg', mimetype='image/dmbb-logo.jpg')

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
    html.Div(
        id='header',
        style={
            'display': 'inline-block',
            'width': '100%',

        },
        children = [
            html.Img(id='image', src='./dmbb-logo.jpg', style={'width':'150px', 'float': 'left'}),
            html.Div(
                style={'float': 'left', 'padding-top': '30px'},
                children = [
                    html.H2(children=['Compare Duke Ballers!']),
                    html.P(style={'padding-left': '5px'}, children=["By Jonathan Michala, Miles Todzo, and Justin Wei"])
                ]

            )

        ]

    ),


    html.Hr(),

    html.Div(
        className='graph-container',
        style={
    		'width':'100%',
        	'margin':'auto',
        	'overflow':'hidden',
            'display': 'inline-block',
        },

        children = [
            # PLAYER GRAPH
            html.Div(
                id='players-div',
                children = [
                    # PLAYER SELECTION
                    html.H4(style={'text-align': 'center'}, children= ['Player Comparator']),
                    html.P('Select multiple players below to compare their average efficiency over a season!'),
                    generatePlayerDropdown('player-selector'),
                    dcc.Graph(
                        id='player-graph'
                    )
                ],
                style = {
                    'width': '48%',
                    'float': 'left',
                    'padding': '3px'
                }
            ),
            # TEAM GRAPH
            html.Div(
                id='teams-div',
                children = [
                    # PLAYER SELECTION
                    html.H4(style={'text-align': 'center'}, children= ['Team Comparator']),
                    html.P('Select multiple teams (by year) below to compare their average rating over a season!'),
                    generatePlayerDropdown('team-selector'),
                    dcc.Graph(
                        id='team-graph'
                    )
                ],
                style = {
                    'width': '48%',
                    'float': 'right',
                    'padding': '3px'

                }
            )
        ]
    ),
    html.Div([
        html.Hr(),
		html.A('View Project Github', href='https://github.com/jwei98/dmbb-compare')
        ], style = {'text-align': 'center'})
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
            title='Player Efficiency Over Season',
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
            title='Team Offensive Rating Over Season',
            xaxis={'title': 'Games Into Season', 'range': [0, 40]},
            yaxis={'title': 'Offensive Rating', 'range': [50, 150]},
            showlegend=True,
        ),
    }

if __name__ == '__main__':
    app.run_server(debug=True)
