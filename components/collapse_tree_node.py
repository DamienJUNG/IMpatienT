from dash import html,Output,Input,MATCH,State,clientside_callback,ALL,ClientsideFunction
import dash_bootstrap_components as dbc
import uuid  

class CollapseTreeNodeAIO(html.Div):
    class ids:
        button = lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'img',
            'aio_ids':aio_ids,
        }
        group = lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'buttonGroup',
            'aio_ids':aio_ids
        }
        collapse = lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'collapse',
            'aio_ids':aio_ids,
        }
        label=lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'label',
            'aio_ids':aio_ids,
        }
        id=lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'label',
            'aio_ids':aio_ids,
        }
        div = lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'div',
            'aio_ids':aio_ids,   
        }

    ids = ids

    def __init__(
      self,data,
      div_props=None,
      aio_id=None,
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
        self.ids.button(aio_id)['index']=1

        super().__init__([
                html.Div([html.Img(id=self.ids.button(aio_id),n_clicks=0,style={'height':'2em', 'width':'2em'}) if is_leaf==False else None,
            dbc.RadioItems(id=self.ids.group(aio_id),
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": "NA", "value": 0,'label_id':'NA'},
                {"label": "Y", "value": 1,'label_id':'YES'},
                {"label": "N", "value": 2,'label_id':'NO'}
            ],
            value=0) if with_button else None
            ,html.Label(id=self.ids.label(aio_id),children=[data['name']['text'],*(" ORDO : " if 'id' in data else None
                                                                                  ,data['id'] if 'id' in data else None)]),
        ],className='collapse-div radio-group'),
            dbc.Collapse(id=self.ids.collapse(aio_id),**_div_props,is_open=False,className="") if not is_leaf else None
        ],className=className,id=self.ids.div(aio_id))


    clientside_callback(
        ClientsideFunction(
        namespace='clientside',
        function_name='update_collapse'
        ),
    Output(ids.collapse(MATCH), "is_open"),
    Output(ids.button(MATCH), "src"),
    Input(ids.button(MATCH), "n_clicks"),
    State(ids.collapse(MATCH), "is_open")
    )

    # clientside_callback(
    #     ClientsideFunction(
    #     namespace='clientside',
    #     function_name='update_checked'
    #     ),
    # Output(ids.group(ALL), "value"),
    # Input(ctr.CollapseTreeRootAIO.ids.checked(ALL), "data"),
    # State(ids.group(ALL), "value"),
    # State(ids.label(ALL), "children")
    # )