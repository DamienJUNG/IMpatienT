from dash import clientside_callback, MATCH, Output, Input, State, ALL, ClientsideFunction,callback
from components.collapse_tree_node import CollapseTreeNodeAIO
from components.collapse_tree_root import CollapseTreeRootAIO
from dash import ctx
import PIL.Image
import plotly.express as px

def find_children(json,text):
    if json['name']['text']==text:
        return json['children']
    children = []
    for node in json['children']:
        children.extend(find_children(node,text))
    return children

clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_collapse'
        ),
    Output(CollapseTreeNodeAIO.ids.collapse(MATCH), "is_open"),
    Output(CollapseTreeNodeAIO.ids.button(MATCH), "src"),
    Input(CollapseTreeNodeAIO.ids.button(MATCH), "n_clicks"),
    State(CollapseTreeNodeAIO.ids.collapse(MATCH), "is_open")
    )

clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='search_nodes'
        ),
    Output({
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'div',
            'aio_ids':ALL,   
            'parent':ALL
        },"style"),
    Input({
            'component':'CollapseTreeRootAIO',
            'subcomponent':'store',
            'aio_ids':ALL,
            'parent':ALL
        },"data"),
    State({
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'div',
            'aio_ids':ALL,   
            'parent':ALL
        }, "children"),
    State({
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'div',
            'aio_ids':ALL,   
            'parent':ALL
        }, "style")
    )

@callback(
    Output(CollapseTreeNodeAIO.ids.collapse(MATCH), "children"),
    Input(CollapseTreeNodeAIO.ids.collapse(MATCH), "is_open"),
    State(CollapseTreeNodeAIO.ids.collapse(MATCH), "children"),
    State(CollapseTreeRootAIO.ids.store(ALL,ALL), "data"),
    State(CollapseTreeNodeAIO.ids.label(MATCH,ALL), "label")
)
def load_children(is_open,children,json,label):
    if len(children)!=0:
        return children
    
    new_children = []
    for node in json[0]['json']:
        for item in find_children(node,label[0][0]):
            new_children.append(CollapseTreeNodeAIO(item,is_leaf=len(item['children'])==0,parent=''))
    return new_children