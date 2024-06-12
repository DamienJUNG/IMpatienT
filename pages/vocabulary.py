# Import packages
import time
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,html,ALL
import dash
import dash_bootstrap_components as dbc
from components import collapse_tree_root as ctr,orphanet_parser
import dash_mantine_components as dmc

import json
with open("test.json", "r") as read_file:
    data = json.load(read_file)
with open("en_product3_146.json", "r") as read_file:
    onto = json.load(read_file)

class Layout:
    def get_layout(args):
        return dmc.MantineProvider(dmc.SimpleGrid(cols=2,spacing="md",verticalSpacing="sm",
    children=[dmc.LoadingOverlay(visible=True,
                    id="loading-overlay",
                    zIndex=1000,
                    overlayProps={"radius": "sm", "blur": 2}),
        dbc.Container([html.H1("Tree"),dbc.Input(placeholder="type something...",id="input",value=""),dbc.Button("Search",id='button'),
    ctr.CollapseTreeRootAIO(orphanet_parser.parse_ontology(onto),aio_id='onto')]),
    dbc.Container([
        html.H1("Properties"),
        dmc.Stack(
            children=[
                dmc.TextInput(label="Vocabulary ID",placeholder="Vocab_Id",disabled=True),
                dmc.TextInput(label="Vocabulary Name",placeholder="Vocab_Name",disabled=True),
                dmc.TextInput(label="Alternative Language",placeholder="Alt_Lang",disabled=True),
                dmc.TagsInput(label="Synonyms"),
                dmc.Checkbox(label="Show as Image Annotation Class"),
                dmc.TagsInput(label="Associated HPO Terms (Extracted from reports)",disabled=True),
                dmc.TagsInput(label="Associated Genes (Extracted from reports)",disabled=True),
                dmc.TagsInput(label="Associated Disease (Extracted from reports)",disabled=True),
                dmc.TagsInput(label="Positively Correlates with (Extracted from reports ; >0.5)",disabled=True),
                dmc.Textarea(label="Description",autosize=True,minRows=7),
            ],style={'padding':'3em','paddingTop':'0px'}
        )
    ],className='not_implemented')]))

    @staticmethod
    def registered_callbacks(app):
        @app.callback(
            Output("loading-overlay", "visible"),
            Input("loading-overlay", "visible"),
        )
        def update(n_clicks):
            time.sleep(1)
            return False

        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_filter'
                ),
            Output(component_id=ctr.CollapseTreeRootAIO.ids.store("onto",ALL),component_property='data'),
            Input(component_id="button",component_property='n_clicks'),
            State(component_id="input",component_property='value'),
            State(component_id=ctr.CollapseTreeRootAIO.ids.store("onto",ALL),component_property='data')
        )