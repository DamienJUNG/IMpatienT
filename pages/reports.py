import pandas as pd
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path='/reports')

with open("assets/text_reports.csv") as file:
    data = pd.read_csv(file,sep=',')
labels = ["biopsie_id","patient_id","gene_diag","conclusion","BOQA_prediction","BOQA_prediction_score"]
data = data[labels].fillna("N/A").to_dict('records')

class Layout:
    def get_layout(args):
        return [
    dmc.Stack([
        dmc.Title("Upload a new report"),
        dmc.Anchor(
            dmc.Button("New Report",rightSection=DashIconify(icon="mdi:file-plus-outline",width=25)),
            href="/patient"
        )
    ],justify="center",align="center",gap=0),
    dmc.Stack(
        children=[
            dmc.Title("Report Database "),
            dmc.Flex([
                dmc.Title("Show ",order=4),
                dmc.Select(id="page-size-selector-reports",data=[{"label":"10","value":"10"},{"label":"25","value":"25"},{"label":"100","value":"100"}],value='10',w=80),
                dmc.Title(" entries",order=4)
            ],columnGap=20),
            dash.dash_table.DataTable(id="reports-table",filter_action='native',data=data,columns=[{'name': i.replace("_"," ").capitalize(), 'id': i} for i in labels])],
    style={'padding':'2em'})]

    @staticmethod
    def registered_callbacks(app):
        @app.callback(
            Output("reports-table","page_size"),
            Input("page-size-selector-reports","value"),
        )
        def udpate_page_size(page_size):
            return int(page_size)