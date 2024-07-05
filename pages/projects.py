from dash import Dash, dash,html,dcc,callback,Output,Input,State,ALL,ctx,no_update
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash
from dash_iconify import DashIconify
from database import db,projects
from flask_login import current_user

labels = ["name","director_id","archived"]

class Layout:
    def get_layout(args):
        return [
    dmc.Stack([
        dmc.Title("Create a new project"),
        dmc.Button("Add new project",id="button-collapse-project",rightSection=DashIconify(icon="mdi:flask-plus",width=25)),
        dbc.Collapse([
            dmc.Center([
                dmc.TextInput(id='project-input'),dmc.Button("Add project",id="add-project")
            ],style={'margin':'2em'})
        ],id="collapse-project"),
        dmc.Table(id="projects-table"),
    ],justify="center",align="center",gap=0),
]
    @staticmethod
    def registered_callbacks(app):
        @app.callback(
            Output("collapse-project","is_open"),
            Input("button-collapse-project","n_clicks"),
            State("collapse-project","is_open"),
        )
        def update_role_collapse(n,is_open):
            if n:
                return not is_open 
            return is_open
        
        @app.callback(
            Output("projects-table","children"),
            Input("projects-table","id"),
        )
        def reset_projects(n):

            all_projects = projects.get_all_project()

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        *[dmc.TableTh(item) for item in labels],
                        dmc.TableTh("Action")
                    ]
                )
            )
            for project in all_projects:
                for label in labels:
                    print(label,project[label])

            rows = [
                dmc.TableTr(
                    [
                        *[dmc.TableTd(project[label]) for label in labels],
                        dmc.TableTd([
                            dmc.Button("Resume",color='green',id={'action':'resume','type':'project','id':project['id']}),
                            dmc.Button("Delete",color='red',id={'action':'delete','type':'project','id':project['id']})
                    ])
                ])for project in all_projects
            ]
            body = dmc.TableTbody(rows)
            return [head,body]
        
        @app.callback(
            Output("project-input","value"),
            Input("add-project","n_clicks"),
            State("project-input","value"),
        )
        def add_project(n,project):
            if n and str(project).replace(" ","")!="":
                print(projects.create_project(str(project).replace(" ","_"),current_user.get_id()))
                return "" 
            return project
        
        @app.callback(
            Output({'action':'delete','type':'project','id':ALL},"n_clicks"),
            Input({'action':'delete','type':'project','id':ALL},"n_clicks"),
        )
        def delete_project(n):
            if ctx.triggered_id and len(ctx.triggered)==1:
                projects.delete_project(ctx.triggered_id['id'])
            return n
        
        @app.callback(
            Output("selected-project","data"),
            Output("global-url","href",allow_duplicate=True),
            Input({'action':'resume','type':'project','id':ALL},"n_clicks"),
            prevent_initial_call=True
        )
        def resume_report(n):
            if len(ctx.triggered)==1 and ctx.triggered_id:
                print("------------- coucou ----------------",ctx.triggered_id)
                return ctx.triggered_id['id'],"/view_project"
            return no_update