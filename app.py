# Import packages
from dash import Dash, callback, State, Input,Output
import dash_bootstrap_components as dbc
from components import collapse_tree_root as ctr,orphanet_parser

import json
with open("test.json", "r") as read_file:
    data = json.load(read_file)
with open("en_product3_146.json", "r") as read_file:
    onto = json.load(read_file)
# Incorporate data
# r = requests.get('http://localhost:3000/api/books?include=author')
# df = r.json()

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# tab = []
# for i,book in enumerate(df):
#     tab.append({'label':book['title'],'value':i})
#     print(tab[i])


# App layout
app.layout = dbc.Container([
    dbc.Input(placeholder="type something...",id="input",value=""),dbc.Button("Search",id='button'),
    dbc.Button("Make diagnostic",id='diagnosis'),
    ctr.CollapseTreeRootAIO(orphanet_parser.parse_ontology(onto),aio_id='test'),
    #print(orphanet_parser.parse_ontology(onto))
    # dbc.Container(tree.tree,class_name='')
    # html.Div(id='slider-output-container'),
    # html.Div(children='My First App with Data'),
    # dcc.Dropdown(tab,0,id="book_dropDown"),
    # html.H2("","title"),
    # html.H3("","author",className="slider")
])

@callback(
    Output(component_id=ctr.CollapseTreeRootAIO.ids.store("test"),component_property='data'),
    Input(component_id="button",component_property='n_clicks'),
    State(component_id="input",component_property='value'),
    State(component_id=ctr.CollapseTreeRootAIO.ids.store("test"),component_property='data')
)
def update_filter(i,input,data):
    if str(input)!=str(data['filter']): data['filter'] = input
    return {'filter':input,'json':data['json']}

@callback(
    Output(component_id=ctr.CollapseTreeRootAIO.ids.checked("test"),component_property='data'),
    Input(component_id="diagnosis",component_property='n_clicks'),
    State(component_id=ctr.CollapseTreeRootAIO.ids.checked("test"),component_property='data')
)
def make_diagnosis(click,checked):
    if click:
        checked = {} 
    return checked

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
