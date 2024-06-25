from dash import Output, Input, State,no_update,ctx
from flask_login import login_user,current_user,logout_user
from callbacks.base import BaseCallback
from database.models import User
import dash_mantine_components as dmc
from dash_iconify import DashIconify 
import flask_login as flog
from database import roles

#Liste des urls autorisées pour les personnes ne possédant pas de compte
without_account = ["/","/create_user"]

class AuthCallback(BaseCallback):
    def __init__(self, app, args) -> None:
        super().__init__(app, args)

    def register_callback(self):
        
        @self.app.callback(
            Output("nav-bar","children"),
            Input("login","data"),
            State("nav-bar","children"),
            prevent_initial_call=True
        )
        def update_navBar(path,children):
            # print("login ici",current_user.get_role(),"i")
            # print("logged in",current_user.is_authenticated)
            if current_user.is_authenticated:
                accessible_pages = roles.get_role_accessible_pages(current_user.get_role())
                dmc.GridCol(dmc.NavLink([],className='normal-text bold-text',rightSection=DashIconify(icon='mdi:log-out-variant',width=30,color='white'),active=True,color='transparent',variant='filled',id='log-link'),span='content')
                if "/vocabulary" in accessible_pages:
                    children.insert(-1,dmc.GridCol(dmc.NavLink([],className='normal-text bold-text',label="Standard vocabulary",leftSection=DashIconify(icon="icon-park-solid:tree-diagram",width=30),href="/vocabulary",active=True,color='transparent',variant='filled'),span='content'))
                if "/patient" in accessible_pages: 
                    children.insert(-1,dmc.GridCol(dmc.NavLink([],className='normal-text bold-text',label="Patient",leftSection=DashIconify(icon="mdi:person",width=30),href="/patient",active=True,color='transparent',variant='filled'),span='content'))
                if "/image_annotation" in accessible_pages: 
                    children.insert(-1,dmc.GridCol(dmc.NavLink([],className='normal-text bold-text',label="Image annotation",leftSection=DashIconify(icon='mdi:folder-image',width=30,color='white'),href="/image_annotation",active=True,color='transparent',variant='filled'),span='content'))
                if "/reports" in accessible_pages:                     
                    children.insert(-1,dmc.GridCol(dmc.NavLink([],className='normal-text bold-text',label="Reports",leftSection=DashIconify(icon="fluent:folder-person-16-filled",width=30),href="/reports",active=True,color='transparent',variant='filled'),span='content'))
                if "/visualisation_dashboard" in accessible_pages:                    
                    children.insert(-1,dmc.GridCol(dmc.NavLink([],className='normal-text bold-text',label="Visualisation Dashboard",leftSection=DashIconify(icon='gridicons:stats',width=30,color='white'),href="/visualisation_dashboard",active=True,color='transparent',variant='filled'),span='content'))
                if "/settings" in accessible_pages: 
                    children.insert(-1,dmc.GridCol(dmc.NavLink([],href="/settings",className='normal-text bold-text',label="Settings",leftSection=DashIconify(icon='mdi:settings-outline',width=30,color='white'),active=True,color='transparent',variant='filled',hiddenFrom={'display':'none'}),span='content'))
            else: 
                children[-1] = dmc.GridCol(dmc.NavLink([],href="/log_in",className='normal-text bold-text',rightSection=DashIconify(icon='mdi:person-circle-outline',width=30,color='white'),active=True,color='transparent',variant='filled',id='log-link'),span='content')
            return children
        
        @self.app.callback(
            Output("global-url","pathname"),
            Output("log-link","label"),
            Output("old-url","data"),
            Input("global-url","pathname"),
            State("old-url","data")
            )
        def is_logged(url,old_url):
            max = 20
            id = "Logged as : "+(current_user.username if len(current_user.username)<=max else current_user.username[:max]+"..." ) if current_user.is_authenticated else "Not logged in"
            # print("ici",old_url,url,url in without_account)
            # print("login ",login)
            # print("current user ",flog.current_user.is_authenticated)
            # Si'il n'y a pas besoin de compte
            if url in without_account:
                return url,id,url
            # Sinon, si on est pas connecté
            elif not current_user.is_authenticated:
                return "/log_in","Not logged in","/log_in"
            role = current_user.get_role()
            accessible_pages = roles.get_role_accessible_pages(current_user.get_role())
            if url in accessible_pages:
                return url,id,url
            else: return old_url,no_update,no_update

        @self.app.callback(
            Output("login","data"),
            Output("global-url","pathname",allow_duplicate=True),
            Input("log-link","n_clicks"),
            prevent_initial_call=True
        )
        def log_out(m): 
            if ctx.triggered_id=="log-link" and m:
                logout_user()
                return None,"/log_in"
            return no_update