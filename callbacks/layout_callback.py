from dash import Output, Input

import importlib
from callbacks.base import BaseCallback

from dash import clientside_callback, MATCH, Output, Input, State, ALL, ClientsideFunction,callback,no_update,ctx
from components.collapse_tree_node import CollapseTreeNodeAIO
from components.collapse_tree_root import CollapseTreeRootAIO
import plotly.express as px
import sqlite3 as sq
import dash._get_app
from database import users, models,db
import dash_mantine_components as dmc 
from dash_iconify import DashIconify

from flask_login import logout_user, current_user

def find_children(json,text):
    if json['name']['text']==text:
        return json['children']
    children = []
    for node in json['children']:
        children.extend(find_children(node,text))
    return children

class LayoutCallback(BaseCallback):

    def __init__(self, app, args) -> None:
        super().__init__(app, args)

    def register_callback(self):
        @self.app.callback(
            Output('page-content', 'children'),
            Input('global-url', 'pathname')
        )
        def render_app_layout(pathname: str):
            if pathname=="/":
                pathname="home"
            module = importlib.import_module("."+pathname.replace("/",""),"pages")
            # print(module)
            layout = module.Layout
            return layout.get_layout(self.args)
            
        self.app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_click'
                ),
            Output(CollapseTreeNodeAIO.ids.collapse(MATCH), "is_open"),
            Input(CollapseTreeNodeAIO.ids.button(MATCH), "n_clicks"),
            Input(CollapseTreeNodeAIO.ids.label(MATCH,ALL), "n_clicks"),
            State(CollapseTreeNodeAIO.ids.collapse(MATCH), "is_open")
            )

        self.app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_collapse'
                ),
            Output(CollapseTreeNodeAIO.ids.button(MATCH), "src"),
            Input(CollapseTreeNodeAIO.ids.collapse(MATCH), "is_open")
            )

        self.app.clientside_callback(
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
                # Output({
                #     'component':'CollapseTreeNodeAIO',
                #     'subcomponent':'collapse',
                #     'aio_ids':ALL,
                # },"is_open",allow_duplicate=True)],
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
                }, "style"),
            )

        @self.app.callback(
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

        @self.app.callback(
            Output(CollapseTreeNodeAIO.ids.group(MATCH),"value"),
            Input({"action":"delete","aio_ids":MATCH},"n_clicks"),
            State(CollapseTreeNodeAIO.ids.group(MATCH),"value"),
        )
        def delete_selection(n,value):
            if n:
                return 0
            else :
                return value

