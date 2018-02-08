import dash
import dash_core_components as dcc
import dash_html_components as html
import os

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.H2('Hello, Team!'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['Justin Wei', 'Jonathan Michala', 'Miles Todzo']],
        value='Miles Todzo'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    if value == 'Justin Wei':
        return 'Justin Wei is dope!"
    elif value == 'Jonathan Michala':
        return 'Hi, Jonathan!'
    else:
        return 'Error: you requested an invalid team member'

if __name__ == '__main__':
    app.run_server(debug=True)
