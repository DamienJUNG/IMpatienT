# Import packages
import importlib
import os

from dash import Dash, dash,html,dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from database.db import db_session,try_connection,generate_all
from database.models import User
from database import users,pages

from flask import Flask
from flask_login import LoginManager

import hydra

from dash import Dash, html, dcc
from omegaconf import DictConfig
from callbacks.callback_loader import load_callbacks


server = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(server)

# manage sessions per request - make sure connections are closed and returned
server.teardown_appcontext(lambda exc: db_session.close())

@login_manager.user_loader
def load_user(user_id):
    return users.get_user_by_id(user_id)

app = Dash(server=server,external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

dash._dash_renderer._set_react_version('18.2.0')

server.config.from_pyfile('config.py')

# Chargement des callbacks de l'application
load_callbacks(app,None)
for file in os.listdir("./pages"):
    if ".py" in file:
        # print(file)
        pages.create_page(file.replace(".py",""))

# App layout
app.layout = dmc.MantineProvider([
    dmc.Grid(children=[
            dmc.GridCol(dmc.NavLink([],className='normal-text bold-text',label="Home",leftSection=DashIconify(icon="fa:home",width=30,color="white"),href="/",active=True,color='transparent',variant='filled'),span='content'),
            
            dmc.GridCol(dmc.NavLink([],className='normal-text bold-text',rightSection=DashIconify(icon='mdi:log-out-variant',width=30,color='white'),active=True,color='transparent',variant='filled',id='log-link'),span='content'),
        ],style={'backgroundColor':'black','padding':'1em'},align='center',justify='space-between',className="header",id="nav-bar"),
    html.Div(id='page-content'),
    dcc.Store("selected-images",data=[],storage_type='session'),
    dcc.Store("login",storage_type='session'),
    dcc.Location("global-url",refresh=True),
    dcc.Store("old-url",data="/",storage_type='session'),
])

# # one time setup
# with server.app_context():
#     generate_all()
#     # Create a user and role to test with
#     db_session.commit()
#     if not server.security.datastore.find_user(username="test"):
#         server.security.datastore.create_user(username="test",
#         password=hash_password("test"), roles=["ADMIN"])
#     db_session.commit()

modules = [importlib.import_module("."+page.replace(".py",""),"pages") for page in os.listdir("pages") if ".py" in page]
for module in modules :
    module.Layout.registered_callbacks(app)
# Run the app
if __name__ == '__main__':
    try_connection()
    generate_all()
    app.run(debug=False)