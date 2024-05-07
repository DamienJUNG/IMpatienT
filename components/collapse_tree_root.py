from dash import html,callback,Output,Input,MATCH,State,clientside_callback,dcc,ALL,ctx,ClientsideFunction
import dash_bootstrap_components as dbc
import uuid
import json
from components import collapse_tree_node as ctn


# def node_match_filter(node,filter):
#     if filter in node['name']['text']:
#         return True
#     if 'children' not in node or len(node['children'])<1 or node['children'] == None:
#         return False
#     for item in node['children']:
#         if node_match_filter(item,filter):
#             return True
#     return False

# def make_node_match_json(data,json,filter):

#     if node_match_filter(json,filter):
#         data['props']['style'] = {}
#         if data['type']=='div':
#             currNode = data['props']['children'][1]
#             make_node_match_json(currNode,json,filter)
    
#         elif data['type']=='collapse':
#             for i,json_node in enumerate(json['children']) :
#                 make_node_match_json(data['props']['children'][i],json_node,filter)
#     else:
#         data['props']['style'] = {'display':'none'}
            
#     return data

# def make_view_match_json(data,json,filter):
#     if node_match_filter(json,filter):
#         data['props']['style'] = {}
#         make_node_match_json(data['props']['children'][1],json,filter)
#     else:
#         data['props']['style'] = {'display':'none'}
#     return data

# def find_checked(checked,children):
#     if children['type']=='div':
#         currNode = children['props']['children'][1]
#         make_node_match_json(currNode,json,filter)
    
#     elif children['type']=='collapse':
#         for i,json_node in enumerate(json['children']) :
#             make_node_match_json(children['props']['children'][i],json_node,filter)

class CollapseTreeRootAIO(html.Div):
    class ids:
        div = lambda aio_ids:{
            'component':'CollapseTreeRootAIO',
            'subcomponent':'div',
            'aio_ids':aio_ids
        }
        store = lambda aio_ids:{
            'component':'CollapseTreeRootAIO',
            'subcomponent':'store',
            'aio_ids':aio_ids
        }
        checked = lambda aio_ids:{
            'component':'CollapseTreeRootAIO',
            'subcomponent':'checked',
            'aio_ids':aio_ids
        }

    ids = ids

    def __init__(
      self,data,
      div_props=None,
      aio_id=None,filter=""
    ):
        """CollapseTreeRootAIO is an All-in-One component that is composed
        of a parent `html.Div`.
        - `data` - The data used to create children TreeViewNodeAIO
        - `div_props` - A dictionary of properties passed into the html.Div component.
        - `filter` - String to filter displayed content
        - `aio_id` - The All-in-One component ID used to generate components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        
        _div_props = {'children':[ctn.CollapseTreeNodeAIO(item,with_button=False,className='category2') for item in data]}
        if div_props:
            _div_props.update(div_props)

        super().__init__([
            html.Div(id=self.ids.div(aio_id), **_div_props),
            dcc.Store(id=self.ids.store(aio_id),**{'storage_type':'memory','data':{'filter':filter,'json':data}}),
            dcc.Store(id=self.ids.checked(aio_id),**{'storage_type':'memory','data':{'Yes':[],'No':[],'NA':[]}})
        ])

    clientside_callback(
        ClientsideFunction(
        namespace='clientside',
        function_name='search_nodes'
        ),
    Output(ctn.CollapseTreeNodeAIO.ids.div(ALL),"style"),
    Input(ids.store(ALL),"data"),
    State(ctn.CollapseTreeNodeAIO.ids.div(ALL), "children"),
    State(ctn.CollapseTreeNodeAIO.ids.div(ALL), "style")
    )

    # @callback(
    # Output(ids.div(MATCH), "children"),
    # Input(ids.store(MATCH), 'data'), # Stocke le filtre à appliquer et le json
    # State(ids.div(MATCH), "children")
    # )
    # def seach_nodes(store,children):
    #     for i,item in enumerate(store[1]):
    #             make_node_match_json(children[i],item,store[0])      
    #     return children
    
