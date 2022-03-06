from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


import callbacks
from utils.Facade import Facade

app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])
server = app.server
app.layout = html.Div([
dcc.Store(id='file_uploaded', storage_type='local'),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
global facade
facade=Facade()



if __name__ == '__main__':
    app.run_server(debug=True)
