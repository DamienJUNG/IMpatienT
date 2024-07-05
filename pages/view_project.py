from dash import Dash, dash,html,dcc,callback,Output,Input,State,ctx,no_update
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash
from dash_iconify import DashIconify
from flask_login import current_user
from database import users,projects,reports

class Layout:

    def get_layout(args):
        return [
        dcc.Store(id="report-store",storage_type='memory'),
        dmc.SimpleGrid([
            dmc.Card([
                dmc.CardSection(dmc.Center(dmc.Title("Reports",order=2)),withBorder=True),
                dmc.CardSection(dmc.Stack(id="reports-grid"),withBorder=True),
                dmc.CardSection(dmc.Stack(id="reports-grid"),withBorder=True)
            ],mih=300,withBorder=True,radius="xl",style={'padding':'3%'}),
            dmc.Stack(id="images-grid"),
            dmc.Stack([
                dmc.SimpleGrid([
                    dmc.TextInput(id="input-report-name",label="Report name"),
                    dmc.TextInput(id="input-patient-id",label="Patient ID")
                ],cols=2),
                dmc.Button("Add blank report",id="add-blank-report"),
            ])
        ],cols=2,id="project-grid",style={'margin':'1%'})
    ]
    @staticmethod
    def registered_callbacks(app):
        @app.callback(
            Output("reports-grid","children"),
            Input("selected-project","data")
        )
        def get_project(project_id):
            project = projects.get_project(project_id)
            children = []
            for report in project.reports:
                children.append(dmc.NavLink(label=[dmc.Text(report.name)],description=dmc.Text("Patient : "+report.patient_id),rightSection=dmc.ButtonGroup([
                    dmc.Button(DashIconify(icon="mdi:edit-box-outline",width=30),id={'action':'resume','type':'report','id':report.id}),
                    dmc.Button(DashIconify(icon="mdi:bin-outline",width=30),color='red',id={'action':'delete','type':'report','id':report.id})
                ])))
            return children
        
        @app.callback(
            Output("add-blank-report","n_clicks"),
            Input("add-blank-report","n_clicks"),
            State("input-report-name","value"),
            State("input-patient-id","value"),
            State("selected-project","data"),
        )
        def add_blank_report(n,report_name,patient_id,project_id):
            if n and report_name.replace(" ","")!="" and patient_id.replace(" ","")!="":
                reports.create_report(project_id,current_user.get_id(),report_name.replace(" ","_"),patient_id.replace(" ","_"))
                return n
            return no_update
        
            