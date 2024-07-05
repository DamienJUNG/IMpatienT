# Import packages
import base64
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH,ctx,no_update
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from components import collapse_tree_root as ctr,orphanet_parser,collapse_tree_node as ctn
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils import ocr
import json
with open("test.json", "r") as read_file:
    data = json.load(read_file)
with open("en_product3_146.json", "r") as read_file:
    onto = json.load(read_file)

class Layout:
    def get_layout(args):
        return dmc.Stack([
    dcc.Store(id="selected-terms",data=dict(),storage_type='memory'),
    dcc.Store(id="report-data",data=dict(),storage_type='memory'),

    dmc.Card(
            children=[
                dmc.CardSection(dmc.Center(html.H1("OCR/NLP analysis")),withBorder=True),
                dmc.CardSection(dmc.Grid([
                    dmc.GridCol(dcc.Upload([dmc.Button("Select a file"),dmc.Text("No file selected",id="uploaded-pdf")],id="uploader-pdf"),span=1),
                    dmc.GridCol(dmc.Select(id="selected-langage",value="eng",data=[{"value":"eng","label":"English"},{"value":"fra","label":"French"}]),span='auto'),
                    dmc.GridCol(dmc.Button("Perform analysis",id="analysis-pdf"),span='auto')
                ],style={'padding':'2em','marginLeft':"1em"}))
            ],style={'margin':'6em','padding':'1em',"marginBottom":"1em","marginTop":"3em"},
            shadow='lg',
            radius='xl',
            withBorder=True),

    dmc.Title("Patient Information"),
    dmc.Grid(
        grow=True,
        gutter="md",
        children=[
            dmc.GridCol([
                dmc.TextInput(id="patient-id",label="Patient ID",placeholder="Patient_ID")
            ], span=3),
            dmc.GridCol([
                dmc.TextInput(id="biopsy-id",label="Biopsy ID",placeholder="Biopsy_ID"),
            ], span=3),
            dmc.GridCol([
                dmc.DateInput(id="biopsy-date",label="Biopsy Date"),
            ], span=3),
            dmc.GridCol([
                dmc.TextInput(id="muscle-name",label="Muscle",placeholder="Muscle"),
            ], span=3),
            dmc.GridCol([
                dmc.NumberInput(id="patient-age",label="Patient age at biopsy",allowNegative=False,value=18)
            ], span=6),
            dmc.GridCol([
                dmc.TextInput(id="diagnosed-gene",label="Diagnosed Gene (HGNC API)",placeholder="Diagnosed Gene"),
            ], span=6),
            dmc.GridCol([
                dmc.TagsInput(id="used-ontology",label="Phenotype terms (HPO API)"),
            ], span=6),
            dmc.GridCol([
                dmc.TextInput(id="mutation-name",label="Mutation"),
            ], span=6),
        ],style={'padding':'2em'}
    ),
    dmc.SimpleGrid(cols=2,spacing="md",verticalSpacing="sm",
    children=[
        dbc.Container([
            html.H1("Vocabulary Tree"),
            dmc.Grid([
                dmc.GridCol(dbc.Input(placeholder="type something...",id="input",value=""),span='auto'),
                dmc.GridCol(dmc.Button("Search",id='button',variant='gradient',rightSection=DashIconify(icon="mdi:search",width=20)),span='content')],grow=True),
            ctr.CollapseTreeRootAIO(orphanet_parser.parse_ontology(onto),aio_id='test')
        ]),
        dbc.Container([
            dmc.Card(
            children=[
                dmc.CardSection(dmc.Center(html.H1("Current selection")),withBorder=True),
                dmc.CardSection(
                    dmc.Flex([
                        dmc.Text("How informative is your description : ",size='lg'),
                        dmc.Rating(fractions=2,value=2.5)
                    ],
                    align='center',style={'margin':'1em'})
                ,withBorder=True),
                dmc.CardSection(dmc.Grid(id="selection",align='stretch',grow=True,justify='center',mih=300,style={'marginTop':'1em'}))
            ],style={'marginTop':'3em','padding':'1em'},
            shadow='lg',
            radius='xl',
            withBorder=True)
    ])]),
     dmc.Grid(
        grow=True,
        gutter="md",
        children=[
            dmc.GridCol([
                dmc.Title("Commentaries and Conclusions",order=3),
                dmc.Textarea(placeholder="Commentaries and Conclusions",autosize=True,minRows=3),
            ]),
            dmc.GridCol([
                dmc.Title("Diagnosis Prediction : ",order=3),
                dmc.Button("Predict !",color='blue')
            ]),
            dmc.GridCol([
                dmc.Text("Method BOQA (Stats):"),
                dmc.Badge("Placeholder",color='orange'),dmc.Badge("Placeholder",color='orange')
            ]),
            dmc.GridCol([
                dmc.Title("Final Diagnosis",order=4),
                dmc.Select(placeholder="Diagnosis",data=[
                    {"value": "unclear", "label": "UNCLEAR"},
                    {"value": "healthy", "label": "HEALTHY"},
                    {"value": "other", "label": "OTHER"},
                ]),
                dmc.Button("Save to Database",rightSection=DashIconify(icon="ic:outline-save",width=25),color='green')
            ]),
        ],style={'padding':'2em'}
    ),
    ])
    @staticmethod
    def registered_callbacks(app):

        # Sert à mettre à jour le composant qui garde en mémoire le filtre du CollapseTreeRoot
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_filter'
            ),
            Output(component_id=ctr.CollapseTreeRootAIO.ids.store("test",ALL),component_property='data'),
            Input(component_id="button",component_property='n_clicks'),
            State(component_id="input",component_property='value'),
            State(component_id=ctr.CollapseTreeRootAIO.ids.store("test",ALL),component_property='data')
        )

        @app.callback(
            Output("patient-id", "value"),
            Output("biopsy-id", "value"),
            Output("muscle-name", "value"),
            Output("patient-age", "value"),
            Output("biopsy-date", "value"),
            Output("diagnosed-gene", "value"),
            Output("mutation-name", "value"),
            Output("used-ontology", "value"),
            Input("selected-reports", "data"),
        )
        def get_report_data(report_id):
            if report_id:
                with open("assets/text_reports.csv") as file:
                    report = pd.read_csv(file,sep=',').fillna("")
                    report_id-=1
                    return (report["patient_id"].to_list()[report_id],
                            report["biopsie_id"].to_list()[report_id],
                            report["muscle_prelev"].to_list()[report_id],
                            report["age_biopsie"].to_list()[report_id],
                            report["date_envoie"].to_list()[report_id],
                            report["gene_diag"].to_list()[report_id],
                            report["mutation"].to_list()[report_id],
                            [i for i in str(report["pheno_terms"].to_list()[report_id]).split(',')])
        
            return no_update

        # On vient récupérer dans un dictionnaire les termes qui ont été cliqué, on ne s'intéresse qu'à celui qui déclenche l'évenement
        # On le conserve dans un Store pour unifier le flux de données et permettre plus tard une synchronisation + poussée
        # Entre la sélection et l'arbre
        @app.callback(
            Output("selected-terms", "data"),
            Input(ctn.CollapseTreeNodeAIO.ids.group(ALL), "value"),
            Input("analysis-pdf","n_clicks"),
            State("uploader-pdf","contents"),
            State("selected-terms", "data"),
            State("selected-langage", "value"),
        )
        def perform_ocr(value,n,content,children,langage):
            if ctx.triggered_id :
                if ctx.triggered_id == "analysis-pdf":
                    if content:
                        pdf_object = ocr.TextReport(file_obj=base64.b64decode(content.split(',')[1]), lang=langage)
                        pdf_object.pdf_to_text()
                        # pdf_object.detect_sections()
                        # pdf_object.extract_section_text()
                        match_list = pdf_object.analyze_text()
                        results = {"full_text": pdf_object.sentence_as_list, "match_list": match_list}
                        print(results)
                else:
                    id = ctx.triggered_id['aio_ids']
                    text = ""
                    for key,value in ctx.states.items() :
                        if id in key:
                            for str in value:
                                text+=str
                            
                    children[text] = {'value':ctx.triggered[0]['value'],'id':id}
            return children
        
        # On met à jour la sélection (partie de droite) en fonction des données du Store
        @app.callback(
            Output("selection", "children"),
            Input("selected-terms", "data"),
        )
        def update_selection(selection):
            children = []
            for label,data in selection.items():
                    if data['value']!=0:
                        children.append(
                            dmc.GridCol(
                                dmc.Text(
                                    label,
                                    size='lg',
                                    style={'color':'green' if data['value']==1 else 'red'}
                                ),span=9,style={'paddingLeft':'2em'}));
                        children.append(
                            dmc.GridCol(
                                dmc.ButtonGroup([
                                    dmc.Button("Delete",id={"action":"delete","aio_ids":data['id']}),
                                    dmc.Button("Add details",id={"action":"add-details","id":data['id']}),
                                ]),span=3))
                        children.append(
                            dmc.GridCol(
                                dbc.Collapse(dmc.Textarea(spellCheck=True,maxRows=3,minRows=3,autosize=True,style={'paddingLeft':'2em','paddingRight':'2em'}),id={"action":"collapse","id":data['id']},is_open=False)
                                ))
            return children

        # Gère le petit volet de détail pour les champs du panneau de sélection (toujours à droite)
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_click'
                ),
            Output({"action":"collapse","id":MATCH}, "is_open"),
            Input({"action":"add-details","id":MATCH}, "n_clicks"),
            State({"action":"collapse","id":MATCH}, "is_open")
            )
        
        @app.callback(
            Output("uploaded-pdf","children"),
            Input("uploader-pdf","filename"),
        )
        def upload_file(file):
            if file:
                return file
            return "No file selected"
            