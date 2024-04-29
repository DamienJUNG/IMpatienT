from dash import html,callback,Output,Input,MATCH,State,dcc
import dash_bootstrap_components as dbc
import json
import uuid
from components import slider

with open("test.json", "r") as read_file:
    data = json.load(read_file)
# graphs = data['graphs']
def add_key(key,data):
    data['key'] = key
    if 'lbl' in data:
        data['title'] = data['lbl'] 
    if 'children' in data:
        for i in range(len(data['children'])):
            add_key(str(key)+ '-'+ str(i),data['children'][i])
    return data

def find(data,filter):
    while len(data['children'])>0:
        for item in data['children']:
            find(item['props'])
    if filter in data['title']:
        data['style'] = {'display':None}
    return data
    
    

class TreeViewRootAIO(html.Div):
    class ids:
        div = lambda aio_ids:{
            'component':'TreeViewRootAIO',
            'subcomponent':'div',
            'aio_ids':aio_ids
        }
        store = lambda aio_ids:{
            'component':'TreeViewRootAIO',
            'subcomponent':'store',
            'aio_ids':aio_ids
        }

    ids = ids

    def __init__(
      self,json,
      div_props=None,
      aio_id=None,filter=""
    ):
        """TreeViewRootAIO is an All-in-One component that is composed
        of a parent `html.Div` and contain TreeViewNodeAIO.
        - `data` - The data used to create children TreeViewNodeAIO
        - `div_props` - A dictionary of properties passed into the html.Div component.
        - `filter` - String to filter displayed content
        - `aio_id` - The All-in-One component ID used to generate the slider and div components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Merge user-supplied properties into default properties
        _div_props = {'children':[TreeViewNodeAIO(item) for item in json]}
        if div_props:
            _div_props.update(div_props)
        super().__init__([ 
            html.Div(id=self.ids.div(aio_id), **_div_props),
            dcc.Store(id=self.ids.store(aio_id),**{'storage_type':'local','data':filter})
        ])
    @callback(
    Output(ids.div(MATCH),'children'),
    Input(ids.store(MATCH),'data'),
    State(ids.div(MATCH),'children'))
    def filter_child(filter,children):
        if filter!="":
            find(children[0]['props'],filter)
        return children


class TreeViewNodeAIO(html.Div):
    class ids:
        accordion = lambda aio_ids:{
            'component':'TreeViewNodeAIO',
            'subcomponent':'accordion',
            'aio_ids':aio_ids
        }
    ids = ids
    def __init__(
      self,
      json,
      accordion_props=None,
      aio_id=None
    ):
        """TreeViewNodeAIO is an All-in-One component that is composed
        of a parent `html.Div` and contain dbc.Accordion.
        - `data` - The data used to create children TreeViewNodeAIO
        - `accordion_props` - A dictionary of properties passed into the dbc.Accordion component.
        - `aio_id` - The All-in-One component ID used to generate the slider and div components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        _accordion_props = {
            'children':[
            dbc.AccordionItem([
                TreeViewNodeAIO(item)
                for item in json['children']],
                title=[json['title'],slider.SliderWithDivAIO(marks={
                -1:"Absent",
                0:"Pas signicatif",
                1:"Très faiblement présent",
                2:"Faiblement présent",
                3:"Présent",
                4:"Fortement présent",
                5:"Très fortement présent"},slider_props={'min':-1, 'max':5,'value':1
            })]
            )]}
        if accordion_props :
            _accordion_props.update(accordion_props)

        super().__init__([ 
            dbc.Accordion(id=self.ids.accordion(aio_id), **_accordion_props),
        ])