# Import packages
from dash import Dash, html, dcc, callback, State, Input,Output
import dash_bootstrap_components as dbc
from components import tree,collapse_tree

import json
with open("test.json", "r") as read_file:
    data = json.load(read_file)

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
    dbc.Input(placeholder="type something...",id="input",value=''),
    collapse_tree.CollapseTreeRootAIO(data,aio_id='test'),
    # dbc.Container(tree.tree,class_name='')
    # html.Div(id='slider-output-container'),
    # html.Div(children='My First App with Data'),
    # dcc.Dropdown(tab,0,id="book_dropDown"),
    # html.H2("","title"),
    # html.H3("","author",className="slider")
])

@callback(
    Output(component_id=collapse_tree.CollapseTreeRootAIO.ids.store("test"),component_property='data'),
    Input(component_id="input",component_property='value'),
    State(component_id=collapse_tree.CollapseTreeRootAIO.ids.store("test"),component_property='data')
)
def update_filter(i,data):
    print(i)
    data[0] = i
    return data
    

# @callback(
#     Output(component_id="author",component_property='children'),
#     Input(component_id="book_dropDown",component_property='value')
# )
# def update_publication_year(i):
#     return f'{df[i]['author']['firstname']} {df[i]['author']['lastname']}'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
