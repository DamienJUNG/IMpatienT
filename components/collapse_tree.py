from dash import html,callback,Output,Input,MATCH,State,clientside_callback,dcc
import dash_bootstrap_components as dbc
import uuid

def node_match_filter(node,filter):
    if filter in node['title']:
        return True
    if 'children' not in node or len(node['children'])<1 or node['children'] == None:
        return False
    for item in node['children']:
        if node_match_filter(item,filter):
            return True
    return False

def make_node_match_json(data,json,filter):

    if node_match_filter(json,filter):
        data['props']['style'] = {}
        if data['type']=='div':
            currNode = data['props']['children'][1]
            make_node_match_json(currNode,json,filter)
    
        elif data['type']=='collapse':
            for i,json_node in enumerate(json['children']) :
                make_node_match_json(data['props']['children'][i],json_node,filter)
    else:
        data['props']['style'] = {'display':'none'}
        
            
    return data

def make_view_match_json(data,json,filter):
    if node_match_filter(json,filter):
        data['props']['style'] = {}
        make_node_match_json(data['props']['children'][1],json,filter)
    else:
        data['props']['style'] = {'display':'none'}
    return data

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

        
        _div_props = {'children':[CollapseTreeNodeAIO(item,with_button=False,className='category1') for item in data]}
        if div_props:
            _div_props.update(div_props)

        super().__init__([
            html.Div(id=self.ids.div(aio_id), **_div_props),
            dcc.Store(id=self.ids.store(aio_id),**{'storage_type':'memory','data':[filter,data]})
        ])

    @callback(
    Output(ids.div(MATCH), "children"),
    Input(ids.store(MATCH), 'data'),
    State(ids.div(MATCH), "children")
    )
    def hide_node(store,children):
        for i,item in enumerate(store[1]):
            make_node_match_json(children[i],item,store[0])
        return children
    

class CollapseTreeNodeAIO(html.Div):
    class ids:
        button = lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'img',
            'aio_ids':aio_ids
        }
        group = lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'buttonGroup',
            'aio_ids':aio_ids
        }
        collapse = lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'collapse',
            'aio_ids':aio_ids
        }
        label=lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'label',
            'aio_ids':aio_ids
        }

    ids = ids

    def __init__(
      self,data,
      div_props=None,
      aio_id=None,filter="",
      is_leaf=False,
      with_button = True,
      className=None
    ):
        """CollapseTreeNodeAIO is an All-in-One component that is composed of a parent `html.Div`.
        - `data` - The data used to create children TreeViewNodeAIO
        - `div_props` - A dictionary of properties passed into the html.Div component.
        - `filter` - String to filter displayed content
        - `aio_id` - The All-in-One component ID used to generate components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())
        children = []
        for item in data['children']:
            if len(item['children'])>0:
                children.append(CollapseTreeNodeAIO(item))
            else:
                children.append(CollapseTreeNodeAIO(item,is_leaf=True))
        _div_props = {'children':children,'style':{'marginLeft':'4em'}}
        if div_props:
            _div_props.update(div_props)

        super().__init__([
                html.Div([html.Img(id=self.ids.button(aio_id),style={'height':'2em', 'width':'2em'}) if is_leaf==False else "",
            dbc.RadioItems(id=self.ids.group(aio_id),
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "Option 1", "value": 1},
                {"label": "Option 2", "value": 2},
                {"label": "Option 3", "value": 3},
            ],
            value=1) if with_button else None
            ,html.Label(id=self.ids.label(aio_id),children=data['title'])
        ],className='collapse-div radio-group'),
            dbc.Collapse(id=self.ids.collapse(aio_id),**_div_props) if not is_leaf else None
        ],className=className)

    @callback(
    Output(ids.collapse(MATCH), "is_open"),
    Output(ids.button(MATCH), "src"),
    Input(ids.button(MATCH), "n_clicks"),
    State(ids.collapse(MATCH), "is_open")
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open, "../assets/cross_to_right.jpg" if is_open is True else "../assets/cross_to_down.jpg"
        return is_open,"../assets/cross_to_right.jpg"
    
    # clientside_callback(
    # """
    # function(n,data) {
    #     if(n)
    #         return 
    #     return data
    # }
    # """,
    # Output(ids.group(MATCH), 'options'),
    # [Input(ids.button(MATCH), "n_clicks")],
    # [State(ids.group(MATCH), 'options')]
    # )