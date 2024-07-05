import pandas as pd
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH,ctx,no_update
import dash
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from database import db,models,users,pages,modules,roles

dataPages = [{"label":str(item['name']),"value":str(item['id'])} for item in pages.get_all_pages()]
dataModules = [{"label":str(item['name']),"value":str(item['id'])} for item in modules.get_all_modules()]

data = users.get_all_users()

class Layout:
    def get_layout(args):
        return [
            dcc.Store(id="to-delete",storage_type='session',data=[]),
            dmc.Modal(
            title="Confirm deletion",
            id="modal-confirm",
            zIndex=10000,
            children=[
                dmc.Text("Do you really want to delete this ?"),
                dmc.Space(h=20),
                dmc.Group(
                    [
                        dmc.Button(
                            "No",
                            color="red",
                            variant="outline",
                            id="abort-delete",
                        ),
                        dmc.Button("Yes !", id="confirm-delete"),
                    ],
                    justify="space-between",
                ),
            ]),
            dmc.Tabs([
                dmc.TabsList(
                [
                    dmc.TabsTab(dmc.Text("Users"),
                        leftSection=DashIconify(icon="mdi:person",width=25),
                        value="users",className="normal-text"
                    ),
                    dmc.TabsTab(
                        dmc.Text("Roles"),
                        leftSection=DashIconify(icon="mdi:people",width=25),
                        value="roles",
                    ),
                    dmc.TabsTab(
                        dmc.Text("Modules"),
                        leftSection=DashIconify(icon="mdi:folder-cog",width=25),
                        value="modules",
                    ),
                ],grow=True),
                dmc.TabsPanel([
                    dmc.Stack([
                    dmc.Title("Create a new user"),
                    dmc.Anchor(
                        dmc.Button("Add new user",id="add-user",rightSection=DashIconify(icon="mdi:person-plus",width=25)),
                        href="/create_user"
                    )
                    ],justify="center",align="center",gap=0),
                    dmc.Stack([
                        dmc.Table(id="users-table"),
                        dmc.ButtonGroup([
                            dmc.Button("Save changes",color='green',id='save-users'),
                            dmc.Button("Reset changes",color='yellow',id='reset-users')
                        ])
                    ],style={'padding':'2em'})
                ], value="users", pb="xs"),
                dmc.TabsPanel([
                    dcc.Store(id="selected-access-role",storage_type='memory'),
                    dmc.Stack([
                        dmc.Title("Roles access"),
                        dmc.Button("Add new role",id='button-collapse-role',rightSection=DashIconify(icon="mdi:people-plus",width=25)),
                        dbc.Collapse([
                            dmc.Center([
                                dmc.TextInput(id='role-input'),dmc.Button("Add role",id="add-role")
                            ],style={'margin':'2em'})
                        ],id="collapse-role")
                    ],justify="center",align="center",gap=0),
                    dmc.Table(id="roles-access-table"),
                    dmc.ButtonGroup([
                        dmc.Button("Save changes",color='green',id='save-access-role'),
                        dmc.Button("Reset changes",color='yellow',id='reset-access-role')
                    ])
                ], value="roles", pb="xs"),
                dmc.TabsPanel([
                    dcc.Store(id="selected-access-module",storage_type='memory'),
                    dmc.Stack([
                        dmc.Title("Modules access"),
                        dmc.Button("Add new module",id='button-collapse-module',rightSection=DashIconify(icon="mdi:folder-plus",width=25)),
                        dbc.Collapse([
                            dmc.Center([
                                dmc.TextInput(id='module-input'),dmc.Button("Add module",id="add-module")
                            ],style={'margin':'2em'})
                        ],id="collapse-module")
                    ],justify="center",align="center",gap=0),
                    dmc.Table(id="modules-access-table"),
                    dmc.ButtonGroup([
                        dmc.Button("Save changes",color='green',id='save-access-module'),
                        dmc.Button("Reset changes",color='yellow',id='reset-access-module')
                    ])
                ], value="modules", pb="xs")
            ],value="users",persistence=True)
        ]

    @staticmethod
    def registered_callbacks(app):
        @app.callback(
            Output("users-table","data"),
            Input("add-user","n_clicks")
        )
        def update_table(n):
            return users.get_all_users()
        
        @app.callback(
            Output("save-access-role","n_clicks"),
            Input("save-access-role","n_clicks"),
            State("selected-access-role","data")
        )
        def save_roles_changes(n,data):
            # print("save role",data)
            if data :
                for role in data.keys():
                    roles.update_role_access(role,data[role])
            return n
        
        @app.callback(
            Output("selected-access-role","data", allow_duplicate=True),
            Input({'module':ALL,'role':ALL},"checked"),
            State("selected-access-role","data"),
            prevent_initial_call=True
        )
        def update_selected_roles(n,data):
            if len(ctx.triggered)!=1:
                return data
            if ctx.triggered_id['module'] in data[ctx.triggered_id['role']]:
                data[ctx.triggered_id['role']].remove(ctx.triggered_id['module'])
            else:
                data[ctx.triggered_id['role']].append(ctx.triggered_id['module'])
            return data


        @app.callback(
            Output("roles-access-table","children"),
            Output("selected-access-role","data"),
            Input("reset-access-role","n_clicks"),
            State("selected-access-role","data"),
        )
        def reset_role_access(n,data):

            all_modules = modules.get_all_modules()
            all_roles = roles.get_all_roles()
            new_data = dict()
            for role in all_roles: new_data[role['name']] = []

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh("Role name \\ Module Name"),
                        *[dmc.TableTh(moduleName['name']) for moduleName in all_modules]
                    ]
                )
            )
            for role in all_roles:
                for module in all_modules:
                    # print(module['name'] in roles.get_role_access(role['name']),module['name'],roles.get_role_access(role['name']))
                    can_access = module['name'] in roles.get_role_access(role['name'])
                    role[module['name']] = dmc.Checkbox(checked=can_access,id={'module':module['name'],'role':role['name']})
                    if can_access : new_data[role['name']].append(module['name'])

            rows = [
                dmc.TableTr(
                    [
                        dmc.TableTd(role["name"]),
                        *[dmc.TableTd(role[module['name']]) for module in all_modules],
                        dmc.TableTd(dmc.Button("Delete",color='red',id={'action':'delete','type':'role','value':role['name']}))
                    ]
                )
                for role in all_roles
            ]
            body = dmc.TableTbody(rows)
            return [head,body],new_data
        
        @app.callback(
            Output("modules-access-table","children"),
            Output("selected-access-module","data"),
            Input("reset-access-module","n_clicks"),
            State("selected-access-module","data"),
        )
        def reset_module_access(n,data):

            all_modules = modules.get_all_modules()
            new_data = dict()
            for module in all_modules: new_data[module['name']] = []

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh("Module name \\ Page Name"),
                        *[dmc.TableTh(page['name']) for page in pages.get_all_pages()],
                    ]
                )
            )
            allPages = pages.get_all_pages()
            for module in all_modules:
                modulePages = modules.get_pages_of_module(module['name'])
                for page in allPages:
                    can_access = page['id'] in modulePages
                    module[str(page['name'])] = dmc.Checkbox(checked=can_access,id={'module':module['name'],'page':page["name"]})
                    if can_access : new_data[module['name']].append(page['name'])
            rows = [
                dmc.TableTr(
                    [
                        dmc.TableTd(module["name"]),
                        *[dmc.TableTd(module[page['name']]) for page in pages.get_all_pages()],
                        dmc.TableTd(dmc.Button("Delete",color='red',id={'action':'delete','type':'module','value':module['name']}))
                    ]
                )
                for module in all_modules
            ]
            body = dmc.TableTbody(rows)

            return [head,body],new_data
        data=data,columns=[{'name': str(item).capitalize(), 'id': str(item)} for item in ["username","role"]]

        @app.callback(
            Output("users-table","children"),
            Input("reset-users","n_clicks"),
        )
        def reset_user_access(n):

            all_users = users.get_all_users()

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        *[dmc.TableTh(item) for item in ["Username","Role"]],
                        dmc.TableTh("Action")
                    ]
                )
            )
            rows = [
                dmc.TableTr(
                    [
                        dmc.TableTd(user['username']),
                        dmc.TableTd(user['role']),
                        dmc.TableTd(dmc.Button("Delete",color='red',id={'action':'delete','type':'user','value':user['username']}))
                    ]
                )
                for user in all_users
            ]
            body = dmc.TableTbody(rows)

            return [head,body]

        @app.callback(
            Output("save-access-module","n_clicks"),
            Input("save-access-module","n_clicks"),
            State("selected-access-module","data")
        )
        def save_modules_changes(n,data):
            # print("save module",data)
            if data :
                for module in data.keys():
                    modules.update_module_access(module,data[module])
            return n
        
        @app.callback(
            Output("selected-access-module","data", allow_duplicate=True),
            Input({'module':ALL,'page':ALL},"checked"),
            State("selected-access-module","data"),
            prevent_initial_call=True
        )
        def update_selected_modules(n,data):
            if len(ctx.triggered)!=1:
                return data
            if ctx.triggered_id['page'] in data[ctx.triggered_id['module']]:
                data[ctx.triggered_id['module']].remove(ctx.triggered_id['page'])
            else:
                data[ctx.triggered_id['module']].append(ctx.triggered_id['page'])
            return data
        
        @app.callback(
            Output("collapse-role","is_open"),
            Input("button-collapse-role","n_clicks"),
            State("collapse-role","is_open"),
        )
        def update_role_collapse(n,is_open):
            if n:
                return not is_open 
            return is_open
        
        @app.callback(
            Output("collapse-module","is_open"),
            Input("button-collapse-module","n_clicks"),
            State("collapse-module","is_open"),
        )
        def update_module_collapse(n,is_open):
            if n:
                return not is_open 
            return is_open
        
        @app.callback(
            Output("module-input","value"),
            Input("add-module","n_clicks"),
            State("module-input","value"),
        )
        def add_module(n,new_module):
            # print(n,new_module)
            if n and str(new_module).replace(" ","")!="":
                print(modules.create_module(str(new_module).lower()))
                return "" 
            return new_module
        
        @app.callback(
            Output("role-input","value"),
            Input("add-role","n_clicks"),
            State("role-input","value"),
        )
        def add_role(n,new_role):
            # print(n,new_role)
            if n and str(new_role).replace(" ","")!="":
                print(roles.create_role(str(new_role).upper()))
                return "" 
            return new_role
        
        @app.callback(
            Output({'action':'delete','type':ALL,'value':ALL},"n_clicks"),
            Output("to-delete","data"),
            Output("modal-confirm","opened"),
            Input({'action':'delete','type':ALL,'value':ALL},"n_clicks"),
            State("to-delete", "data"),
        )
        def delete_row(n,delete):
            # print(n)
            if n and len(ctx.triggered)==1:
                delete.append({'type':ctx.triggered_id['type'],'value':ctx.triggered_id['value']})
                return n,delete,True
            return no_update
        

        @app.callback(
            Output("to-delete","data",allow_duplicate=True),
            Output("modal-confirm","opened",allow_duplicate=True),
            Input("confirm-delete","n_clicks"),
            Input("abort-delete","n_clicks"),
            State("to-delete", "data"),
            prevent_initial_call=True
        )
        def confirm_delete(n,m,delete):
            print(delete)
            if len(delete)==1 and ctx.triggered_id=="confirm-delete":
                item = delete[0]
                if item['type']=='module':
                    modules.delete_module(item['value'])
                elif item['type']=='role':
                    roles.delete_role(item['value'])
                elif item['type']=='user':
                    users.delete_user(item['value'])
                return [],False
            return delete,False