import pandas as pd
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH,ctx,no_update
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path='/reports')

with open("assets/text_reports.csv") as file:
    data = pd.read_csv(file,sep=',')
labels = ["biopsie_id","patient_id","gene_diag","conclusion","BOQA_prediction","BOQA_prediction_score"]
# on ajoute l'id uniquement pour les données
data = data[[*labels,'id']].fillna("N/A").to_dict('records')

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
                dmc.Title(" entries",order=4),
                dmc.Pagination(id="pagination",total=1,style={'marginLeft':'30%'})
            ],columnGap=20),
            dmc.Table(id='reports-table'),
        ],
    style={'padding':'2em'})]

    @staticmethod
    def registered_callbacks(app):
        @app.callback(
            Output("reports-table","children"),
            Output("pagination","total"),
            Output("pagination","value"),
            Input("page-size-selector-reports","value"),
            Input("pagination","value"),
        )
        def udpate_page_size(page_size,page_number):
            page_size = int(page_size)
            total = (len(data)//page_size)
            if (len(data)%page_size)!=0 : total+=1
            if not page_number or page_number>total:
                page_number=1
            return [
                dmc.TableThead(
                dmc.TableTr(
                        [
                            *[dmc.TableTh(i.replace("_"," ").capitalize()) for i in labels],
                            dmc.TableTh("Action"),
                        ]
                    )
                ),
                dmc.TableTbody([
                    dmc.TableTr(
                        [
                            *[dmc.TableTd(item[label]) for label in labels],
                            dmc.TableTd([
                                dmc.Button("Resume",color='green',id={'action':'resume','type':'report','id':item['id']}),
                                dmc.Button("Delete",color='red',id={'action':'delete','id':item['id']})
                                ])
                        ]
                    )
                    for item in data[(page_number-1) * page_size : (page_number) * page_size]
                ])
            ],total,page_number