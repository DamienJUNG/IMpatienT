# Import packages
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH
import dash
import dash_bootstrap_components as dbc
from components import collapse_tree_root as ctr,orphanet_parser,collapse_tree_node as ctn
import dash_mantine_components as dmc
import datetime

import json
with open("test.json", "r") as read_file:
    data = json.load(read_file)
with open("en_product3_146.json", "r") as read_file:
    onto = json.load(read_file)

dash.register_page(__name__, path='/patient')

layout = dmc.MantineProvider([
    dmc.Title("Patient Information"),
    dmc.Grid(
        grow=True,
        gutter="md",
        children=[
            dmc.GridCol([
                dmc.TextInput(label="Patient ID",placeholder="Patient_ID")
            ], span=3),
            dmc.GridCol([
                dmc.TextInput(label="Biopsy ID",placeholder="Biopsy_ID"),
            ], span=3),
            dmc.GridCol([
                dmc.DateInput(label="Biopsy Date"),
            ], span=3),
            dmc.GridCol([
                dmc.TextInput(label="Muscle",placeholder="Muscle"),
            ], span=3),
            dmc.GridCol([
                dmc.NumberInput(label="Patient age at biopsy",allowNegative=False,value=18)
            ], span=6),
            dmc.GridCol([
                dmc.TextInput(label="Diagnosed Gene (HGNC API)",placeholder="Diagnosed Gene"),
            ], span=6),
            dmc.GridCol([
                dmc.TagsInput(label="Phenotype terms (HPO API)",placeholder="HPO Phenotype Description"),
            ], span=6),
            dmc.GridCol([
                dmc.TextInput(label="Mutation"),
            ], span=6),
        ],style={'padding':'2em'}
    ),
    dmc.SimpleGrid(cols=2,spacing="md",verticalSpacing="sm",
    children=[
        dbc.Container([
            html.H1("Vocabulary Tree"),
            dmc.Grid([
                dmc.GridCol(dbc.Input(placeholder="type something...",id="input",value=""),span='auto'),
                dmc.GridCol(dmc.Button("Search",id='button',variant='gradient'),span='content')],grow=True),
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
                dmc.Grid(id="selection",align='stretch',grow=True,justify='center')
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
                dmc.Button("Predict !",variant="gradient")
            ]),
            dmc.GridCol([
                dmc.Text("Method BOQA (Stats):"),
                dmc.Badge("Placeholder"),dmc.Badge("Placeholder")
            ]),
            dmc.GridCol([
                dmc.Title("Final Diagnosis",order=4),
                dmc.Select(placeholder="Diagnosis",data=[
                    {"value": "unclear", "label": "UNCLEAR"},
                    {"value": "healthy", "label": "HEALTHY"},
                    {"value": "other", "label": "OTHER"},
                ]),
                dmc.Button("Save to Database",variant="gradient")
            ]),
        ],style={'padding':'2em'}
    ),
    ])

clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_filter'
    ),
    Output(component_id=ctr.CollapseTreeRootAIO.ids.store("test",ALL),component_property='data'),
    Input(component_id="button",component_property='n_clicks'),
    State(component_id="input",component_property='value'),
    State(component_id=ctr.CollapseTreeRootAIO.ids.store("test",ALL),component_property='data')
)

@callback(
    Output("selection", "children"),
    Input(ctn.CollapseTreeNodeAIO.ids.group(ALL,ALL), "value"),
    State(ctn.CollapseTreeNodeAIO.ids.label(ALL,ALL), "label"),)
def update_checked(value,label):
    children = []
    # On veut récupérer le tous les noeuds qui ont un numéro (item[2])
    label = [item for item in label if item[2]!=None]
    for i,item in enumerate(value):
        if item>=1: 
            children.append(
                dmc.GridCol(
                    dmc.Text(
                        label[i],
                        size='lg',
                        style={'color':'green' if item==1 else 'red'}
                    ),span=9,style={'paddingLeft':'2em'}));
            children.append(
                dmc.GridCol(
                    dmc.ButtonGroup([
                        dmc.Button("Delete"),
                        dmc.Button("Add details")
                    ]),span=3))
    return children