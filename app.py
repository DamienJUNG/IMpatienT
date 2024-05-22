# Import packages
from dash import Dash, dash,html,dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import callbacks

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],use_pages=True)

dash._dash_renderer._set_react_version('18.2.0')

# App layout
app.layout = dmc.MantineProvider([
    html.Header([
        dmc.Flex(children=[
            dmc.NavLink([],label="Home",href="/",active=True,color='transparent',variant='filled'),
            dmc.NavLink([],label="Standard vocabulary",href="/vocabulary",active=True,color='transparent',variant='filled'),
            dmc.NavLink([],label="Patient",href="/patient",active=True,color='transparent',variant='filled'),
            dmc.NavLink([],label="Image annotation",href="/image_annotation",active=True,color='transparent',variant='filled'),
            dmc.NavLink([],label="Reports",href="/reports",active=True,color='transparent',variant='filled'),
            dmc.NavLink([],label="Visualisation Dashboard",href="/visualisation_dashboard",active=True,color='transparent',variant='filled'),
        ],style={'backgroundColor':'black','padding':'1em'},className="header")
    ]),
    html.Div(dash.page_container),
    dcc.Store("selected-images",data=[],storage_type='session')
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
