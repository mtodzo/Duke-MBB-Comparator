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
offensiveTeamGraphs = {}
defensiveTeamGraphs = {}
overallTeamGraphs = {}

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
        name = team.getName()
        offensive = go.Scatter(
            x = team.getGameNos(),
            y = team.getAverageEffs('offensive'),
            mode = 'lines',
            name = name
        )
        defensive = go.Scatter(
            x = team.getGameNos(),
            y = team.getAverageEffs('defensive'),
            mode = 'lines',
            name = name
        )
        overall = go.Scatter(
            x = team.getGameNos(),
            y = team.getAverageEffs('overall'),
            mode = 'lines',
            name = name
        )
        offensiveTeamGraphs[name] = offensive
        defensiveTeamGraphs[name] = defensive
        overallTeamGraphs[name] = overall

createPlayerGraphs()
createTeamGraphs()

# generates player dropdown
def generatePlayerDropdown(selectorID):
    complete_data = []
    values = []
    if selectorID == 'player-selector':
        for player in playerList:
            data = {}
            data['label'] = player.name.replace('_', ' ')
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

    # ABOUT SECTION
    html.Div(
        className='about',
        style={
    		'width':'90%',
        	'margin':'auto',
        	'overflow':'hidden',
            'text-align': 'left'
        },
        children = [
            html.H3(style= {'text-align': 'left'}, children=['About']),
            html.P('For our datathon hack, we were interested in comparing Duke basketball players and teams throughout history. \
            Below you will find two comparison tools.'),
            html.P('On the left, you can view and compare individual players\' average efficiency over \
            the course of a season. "Player efficiency" is John Hollinger’s all-in-one player rating statistic, which takes into account \
            multiple factors to give a good idea of a player’s overall performance each game.'),
            html.P('On the right, you can compare the offensive, defensive, and overall performance ratings of Blue Devil teams from each year.'),
            html.P('See the Calculations section below for more details on our specific calculations (including equations)!')
        ]
    ),


    html.Hr(),
    html.Div(
        className='graph-container',
        style={
    		'width':'95%',
        	'margin':'auto',
            'padding': '0px',
        	'overflow':'hidden',
            'text-align': 'left'
        },

        children = [
            # PLAYER GRAPH
            html.Div(
                id='players-div',
                children = [
                    # PLAYER SELECTION
                    html.H4(style={'text-align': 'center'}, children= ['Player Comparator']),
                    html.P('Try comparing Christian Laettner and Marvin Bagley III, or \
                    Grayson Allen\'s peformance over the course of his fours years (\'15, \'16, \'17, \'18)!'),
                    generatePlayerDropdown('player-selector'),
                    html.Br(),
                    html.Br(),
                    dcc.Graph(
                        id='player-graph'
                    )
                ],
                style = {
                    'width': '47%',
                    'float': 'left',
                }
            ),
            # TEAM GRAPH
            html.Div(
                id='teams-div',
                children = [
                    # PLAYER SELECTION
                    html.H4(style={'text-align': 'center'}, children= ['Team Comparator']),
                    html.P('Try comparing our current team to a championship team rating! \
                    (1990-91, 1991-1992, 2000-2001, 2009-10, 2014-15)'),
                    generatePlayerDropdown('team-selector'),
                    dcc.Tabs(
             	    	tabs=[
             	    		{'label': 'Offensive Rating', 'value': 0},
             	    		{'label': 'Defensive Rating', 'value': 1},
             	    		{'label': 'Overall Rating', 'value': 2}
             	    	],
             	    	value=0,
             	    	id='tabs'
             	    ),
                    dcc.Graph(
                        id='team-graph'
                    )
                ],
                style = {
                    'width': '47%',
                    'float': 'right',

                }
            )
        ]
    ),

    html.Hr(),

    # team performance average over history
    html.Div(
        style={
    		'width':'90%',
        	'margin':'auto',
        	'overflow':'hidden',
            'text-align': 'left'
        },
        children = [
            html.H3(children=['Team Historical Trends']),
            html.P(children=['Below, we can observe trends regarding Duke\'s basketball teams over time. Note how \
            our offensive ratings have steadily increased throughout the years, while our defensive rating hasn\'t— reflecting a shift in the way \
            the game is played in the modern age (run and gun style of offense).']),
            dcc.Tabs(
                tabs=[
                    {'label': 'Offensive Rating', 'value': 0},
                    {'label': 'Defensive Rating', 'value': 1},
                    {'label': 'Overall Rating', 'value': 2}
                ],
                value=0,
                id='history-tabs'
            ),
            dcc.Graph(
                id='history-graph'
            )
        ]
    ),

    html.Hr(),
    html.Hr(),
    # CALCULATIONS SECTION
    html.Div(
        className='calculations',
        style={
    		'width':'90%',
        	'margin':'auto',
        	'overflow':'hidden',
            'text-align': 'left'
        },
        children = [
            html.H3(style= {'text-align': 'left'}, children=['Calculations']),
            html.P('To calculate player efficiency, we used the following equation:'),
            html.P(style= {'margin-left' : '10em'}, children=['points + rebounds + assists + steals + blocks − missed FG − missed FT - turnovers) / (games played)']),
            html.P('To calculate team ratings, we used the accepted metrics of:'),
            html.P(style= {'margin-left' : '10em'}, children=['offensive rating = (total points/total possessions) * 100']),
            html.P(style= {'margin-left' : '10em'}, children=['defensive rating = (opponent\'s total points / opponent\'s total possessions) * 100']),
            html.P(style= {'margin-left' : '10em'}, children=['overall rating = (offensive rating + defensive rating) / 2']),
            html.P('To calculate total possessions, we used the following equation:'),
            html.P(style= {'margin-left' : '10em'}, children=['total number of possessions = FG attempted - offensive rebounds + turnovers + (0.4 x FT attempted)']),
            html.P('This equation is always used for calculating possessions since basketball possessions can only end in a \
            field goal attempt, offensive rebound, turnover, or free throw. The factor by which the free throw is multiplied \
            by may vary between .4 and .5 in some versions of this equation, but as long as the value is kept constant for the comparisons, \
            any possible error from this value is insignificant.')
        ]
    ),
    html.Div([
        html.Hr(),
		html.A('View Project Github', href='https://github.com/jwei98/dmbb-compare'),
        html.P('#DukeMBBStats')
        ],
        style = {'text-align': 'center'}
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
            title='Player Efficiency Over Season',
            xaxis={'title': 'Games Into Season', 'range': [0, 40]},
            yaxis={'title': 'Player Efficiency', 'range': [0, 40]},
            showlegend=True,
        ),
    }

@app.callback(dash.dependencies.Output('team-graph', 'figure'), [dash.dependencies.Input('tabs', 'value'), dash.dependencies.Input('team-selector', 'value')])
def display_content(tab, teamNames):
    teamsToGraph = []

    if tab == 0:
        if teamNames:
            for tn in teamNames:
                teamsToGraph.append(offensiveTeamGraphs[tn])
        return {
            'data': teamsToGraph,
            'layout': go.Layout(
                title='Offensive Team Rating Over Season',
                xaxis={'title': 'Games Into Season', 'range': [0, 40]},
                yaxis={'title': 'Rating', 'range': [50, 150]},
                showlegend=True,
            ),
        }
    elif tab == 1:
        if teamNames:
            for tn in teamNames:
                teamsToGraph.append(defensiveTeamGraphs[tn])
        return {
            'data': teamsToGraph,
            'layout': go.Layout(
                title='Defensive Team Rating Over Season',
                xaxis={'title': 'Games Into Season', 'range': [0, 40]},
                yaxis={'title': 'Rating', 'range': [50, 150]},
                showlegend=True,
            ),
        }
    elif tab == 2:
        if teamNames:
            for tn in teamNames:
                teamsToGraph.append(overallTeamGraphs[tn])
        return {
            'data': teamsToGraph,
            'layout': go.Layout(
                title='Overall Team Rating Over Season',
                xaxis={'title': 'Games Into Season', 'range': [0, 40]},
                yaxis={'title': 'Rating', 'range': [50, 150]},
                showlegend=True,
            ),
        }
    else:
    	return {
            'data': teamsToGraph,
            'layout': go.Layout(
                title='Select a Team to View Ratings',
                xaxis={'title': 'Games Into Season', 'range': [0, 40]},
                yaxis={'title': 'Rating', 'range': [50, 150]},
                showlegend=True,
            ),
        }

@app.callback(dash.dependencies.Output('history-graph', 'figure'), [dash.dependencies.Input('history-tabs', 'value')])
def display_content(tab):

    if tab == 0:
        return {
            'data': [go.Scatter(
                x = tdt.getTeamNames(),
                y = tdt.getTeamAverages('offensive'),
                mode = 'lines',
                name = 'Offensive Averages'
            )],
            'layout': go.Layout(
                title='Team Offensive Ratings Over Time',
            )
        }
    elif tab == 1:
        return {
            'data': [go.Scatter(
                x = tdt.getTeamNames(),
                y = tdt.getTeamAverages('defensive'),
                mode = 'lines',
                name = 'Defensive Averages'
            )],
            'layout': go.Layout(
                title='Team Defensive Ratings Over Time',
            )
        }
    elif tab == 2:
        return {
                'data': [go.Scatter(
                    x = tdt.getTeamNames(),
                    y = tdt.getTeamAverages('overall'),
                    mode = 'lines',
                    name = 'Overall Averages'
                )],
                'layout': go.Layout(
                    title='Team Overall Ratings Over Time',
                )
            }

if __name__ == '__main__':
    app.run_server(debug=True)
