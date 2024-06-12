from dash import Dash, dash,html,dcc,callback,Output,Input,State,ctx,no_update
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash
from dash_iconify import DashIconify
from database.roles import get_all_roles
import database.users as users

data = [{"value":str(item['name']),"label":item['name']} for item in get_all_roles()]
class Layout:
    def get_layout(args):
        return [
    dmc.Stack([
        dmc.Title("Sign In"),
        dmc.Text("New user ? Contact admin to create an account !"),
        dmc.TextInput(id="create-username",label="Username",placeholder="Username"),
        dmc.PasswordInput(id="create-password",label="Password",placeholder="Password"),
        dmc.Select(data=data,id="select-role"),
        dmc.Button("Create account",id="create-user")
    ],style={"marginLeft":"25%","width":"50%"})
]
    @staticmethod
    def registered_callbacks(app):
        @app.callback(
        Output("global-url","pathname",allow_duplicate=True),
        Input("create-user","n_clicks"),
        State("create-user","id"),
        State("create-username","value"),
        State("create-password","value"),
        State("select-role","value"),
        prevent_initial_call=True
        )
        def create_user(n,id,username,password,role):
            if ctx.triggered_id==id and n:
                if username=="" or password=="" or role==None:
                    return no_update
                print(role)
                users.add_user(username,password,role)
                return "/"
            return no_update


