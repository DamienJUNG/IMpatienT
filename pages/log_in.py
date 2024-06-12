from dash import Dash, dash,html,dcc,callback,Output,Input,State,ctx,no_update
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash
from dash_iconify import DashIconify
from flask_login import login_user
from database import users
import database.users as users

class Layout:

    def get_layout(args):
        return [
    dmc.Alert("",title="   You have to be logged  in to acces this page !",style={"margin":"2%","fontSize":"1.2em"},className='invisible',color="blue",id="not-logged"),
    dmc.Alert("",title="   Username or password incorrect !",style={"margin":"2%","fontSize":"2em"},icon=DashIconify(icon="mdi:alert"),className='invisible',color="red",id="wrong-id"),
    dmc.Stack([
        dmc.Title("Sign In"),
        dmc.Text("New user ? Contact admin to create an account !"),
        dmc.TextInput(id="username",label="Username",placeholder="Username"),
        dmc.PasswordInput(id="password",label="Password",placeholder="Password"),
        dmc.Checkbox(id='remember-me',label="Remember me"),
        dmc.Button(["Sign In"],id="sign-in",leftSection=DashIconify(icon="mdi:sign-in-variant",width=25)),
        dmc.Anchor("I don't have an account",href="/create_user")
    ],style={"marginLeft":"25%","width":"50%",'marginTop':'2em'})
]
    @staticmethod
    def registered_callbacks(app):
        @app.callback(
            Output("login","data",allow_duplicate=True),
            Output("global-url","pathname",allow_duplicate=True),
            Output("wrong-id","className"),
            # Output("not-logged","className"),
            Input("sign-in","n_clicks"),
            State("username","value"),
            State("password","value"),
            State("global-url","pathname"),
            prevent_initial_call=True
        )
        def log_in(n,username,password,url):
            if ctx.triggered_id=="sign-in" and n and username and password:
                print(users.verify_user(username,password))
                if not users.verify_user(username,password):
                    return (
                        no_update,no_update,""
                    )
                user = users.get_user(username)
                # print("user",user)
                login_user(user)
                return user.as_dict(),"/","invisible"
            return no_update,no_update,no_update
# @callback(
#     Output("login","storage_type"),
#     Input("remember-me","checked")
# )
# def remember_me(checked):
#     return "session" if checked else "local"