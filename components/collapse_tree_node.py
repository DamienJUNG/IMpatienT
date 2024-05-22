from dash import html,Output,Input,MATCH,State,clientside_callback,ClientsideFunction,ALL
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import uuid

class CollapseTreeNodeAIO(html.Div):
    class ids:
        button = lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'img',
            'aio_ids':aio_ids,
        }
        group = lambda aio_ids,parent:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'buttonGroup',
            'aio_ids':aio_ids,
            'parent':parent
        }
        collapse = lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'collapse',
            'aio_ids':aio_ids,
        }
        label=lambda aio_ids,parent:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'label',
            'aio_ids':aio_ids,
            'parent':parent
        }
        id=lambda aio_ids:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'label',
            'aio_ids':aio_ids,
        }
        div = lambda aio_ids,parent:{
            'component':'CollapseTreeNodeAIO',
            'subcomponent':'div',
            'aio_ids':aio_ids,   
            'parent':parent
        }

    ids = ids

    def __init__(
      self,data,
      div_props=None,
      aio_id=None,
      is_leaf=False,
      with_button = True,
      className=None,
      parent=None
    ):
        """CollapseTreeNodeAIO is an All-in-One component that is composed of a parent `html.Div`.
        - `data` - The data used to create children TreeViewNodeAIO
        - `div_props` - A dictionary of properties passed into the html.Div component.
        - `aio_id` - The All-in-One component ID used to generate components's dictionary IDs.
        - `is_leaf` - Whether or not the node is a leaf (has no children)
        - `with_button` - Whether the node needs to display buttons
        - `className` - CSS className of the node
        - `parent` - id of the parent
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())
        children = []
        _div_props = {'children':children,'style':{'marginLeft':'3em'}}
        if div_props:
            _div_props.update(div_props)
        self.ids.button(aio_id)['index']=1

        super().__init__([
                html.Div([html.Img(id=self.ids.button(aio_id),n_clicks=0,src="assets/cross_to_right.jpg",style={'height':'2em', 'width':'2em'}) if is_leaf==False else None,
            dbc.RadioItems(id=self.ids.group(aio_id,parent),
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
            ,dmc.NavLink(id=self.ids.label(aio_id,parent),label=[
                data['name']['text'],*(" ORDO : " if 'id' in data else None,
            data['id'] if 'id' in data else None)]),
        ],className='collapse-div radio-group'),
            dbc.Collapse(id=self.ids.collapse(aio_id),**_div_props,is_open=False,className="") if not is_leaf else None
        ],className=className,id=self.ids.div(aio_id,parent))