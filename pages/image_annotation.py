from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH,ctx,no_update
import dash
import os
import dash_mantine_components as dmc
import base64
from dash_iconify import DashIconify

annotate_icon = DashIconify(icon="mdi:image-edit-outline",width=25)
modify_icon = DashIconify(icon="mdi:text-box-edit-outline",width=25)
delete_icon = DashIconify(icon="mdi:delete-outline",width=25)
dash.register_page(__name__, path='/image_annotation')

layout = [
    dcc.Store(id="page-config",storage_type="memory",data={'page_size':10,'current_page':1,'nb_page':0}),
    dcc.Store(id="display-mode",storage_type="session",data="table"),
    dcc.Store(id="data-to-display",storage_type="memory",data={'images':[],'info':{'nb_pages':0,'current_page':0,'page_size':10}}),
    dcc.Location(id="loc",refresh=True),
    dmc.Stack([
        dmc.Title("Upload a new image"),
        dcc.Upload(dmc.Button("New Image",rightSection=DashIconify(icon="mdi:image-plus-outline",width=25)),multiple=True,id='uploader'),
    ],justify="center",align="center",gap=0),
    dmc.Stack(
        children=[
                dmc.Title("Image Database "),
                dmc.Flex([
                    dmc.Title("Show",order=4),
                    dmc.Select(id="page-size-selector-images",data=[{"label":"10","value":"10"},{"label":"25","value":"25"},{"label":"100","value":"100"}],value="10",w=80),
                    dmc.Title("entries",order=4)
                ],columnGap=20,align='center'),
                dmc.Group([
                    dmc.ButtonGroup([
                        dmc.Button("Annotate selection",id="annotate-selection",color='yellow',rightSection=annotate_icon),
                        dmc.Button("Modify selection",id="modify-selection",color='green',rightSection=modify_icon),
                        dmc.Button("Delete selection",id="delete-selection",color='red',rightSection=delete_icon),
                    ]),
                    dmc.Pagination(id="image-pagination",total=1,value=1,style={'display':'None'}),
                    dmc.ButtonGroup([
                        dmc.Button("Card mode",id="card-mode",color='gray'),
                        dmc.Button("Table mode",id="table-mode",color='purple'),
                    ]),
                ],justify='space-between'),
                html.Div(dash.dash_table.DataTable(id="image-table",row_selectable='multi',page_current=0,selected_rows=[]),id="image-div"),
                dmc.Grid([

                ],id="image-cards")
            ],
    style={'padding':'2em'})
    ]

# Fais le lien entre le composant de pagination et le store page-config
@callback(
        Output("page-config","data",allow_duplicate=True),
        Input("image-pagination","value"),
        State("page-config","data"),
        prevent_initial_call=True
)
def update_cards(current_page,config):
    config['current_page'] = current_page
    return config
    
# Génère ou non les cartes à afficher, et rend visible ou non le tableau selon le mode choisi
@callback(
        Output("image-table","data"),
        Output("image-cards","children"),
        Output("image-div","style"),
        Output("image-pagination","style"),
        Input("data-to-display","data"),
        Input("display-mode","data"),
        Input("page-config","data"),
        State("image-table","selected_rows")
)
def update_displayer(data,mode,config,ids):
    if mode=="table":
        return data,None,{},{'display':'None'}
    else:
        start = (config['current_page']-1)*config['page_size']
        end = config['current_page']*config['page_size']
        cards = []
        for i,item in enumerate(data[start:end]):    
            cards.append(dmc.Card([
                dmc.CardSection(dmc.Group([dmc.Checkbox(item['Image Name'],labelPosition='left',id={'index':i+start,'type':'checkbox'},checked=(start+i) in ids)],align='center',justify='space-between'),withBorder=True,className='card-title'),
                dmc.CardSection(dmc.Grid([
                    dmc.GridCol(dmc.Image(src="assets/images/"+item['Image Name'],mih=400),span=8,w=400,h=350),
                    dmc.GridCol([
                        dmc.Stack([
                            dmc.Text("Biopsy ID : "+item["Biopsy ID"]),
                            dmc.Text("Patient ID : "+item["Patient ID"]),
                            dmc.Text("Diagnostic : "+item["Diagnostic"]),
                            dmc.Divider(style={'margin':'2em 0 2em 0'}),
                            dmc.ButtonGroup([
                                dmc.Button("Annotate",id={"action":"annotate","index":i+start},color='yellow',rightSection=annotate_icon),
                                dmc.Button("Modify",id={"action":"modify","index":i+start},color='green',rightSection=modify_icon),
                                dmc.Button("Delete",id={"action":"delete","index":i+start},color='red',rightSection=delete_icon),
                            ],orientation='vertical',style={'paddingRight':'1em'})
                        ],gap='sm',style={'padding':'1em 0 0 0'})
                    ],span=4)
                ]))
            ],withBorder=True,radius='xl'))
        return data,dmc.SimpleGrid(cards,cols=3),{"display":"None"},{}

# Met à jour le mode d'affichage
@callback(
        Output("display-mode","data"),
        Input("card-mode","n_clicks"),
        Input("table-mode","n_clicks"),
        prevent_initial_call=True
)
def update_mode(card,table):
    return "table" if ctx.triggered_id=="table-mode" else "card"

# Recharge toutes les images à l'upload
@callback(
    Output("data-to-display","data"),
    Input("uploader","contents"),
    State("uploader","filename"),
)
def upload(contents,names):
    if contents:
        for i,file in enumerate(contents):
            img_str = str.split(file,",")[1]
            encoded_str = base64.b64decode(img_str)
            fd = open("assets/images/"+names[i],'+wb')
            fd.write(encoded_str)
            fd.close()
    data = []
    for file in os.listdir("./assets/images/"):
        data.append({"Biopsy ID":'Not available','Patient ID':'Not available','Image Name':file,'Diagnostic':'Not available'})
    return data

# Change le nombre d'images affichés dans le tableau
@callback(
        Output("image-table","page_size"),
        Output("page-config","data"),
        Output("image-pagination","total"),
        Output("image-pagination","value"),
        Input("page-size-selector-images","value"),
        Input("data-to-display","data"),
        State("page-config","data"),
)
def update_page_size(page_size,data,config):
    size = int(page_size)
    config['page_size'] = size
    nb_page = (len(data)/size)+1
    if nb_page<1 : nb_page=1
    config['nb_page'] = nb_page
    config['current_page'] = 1
    return size,config,nb_page,1

# Gère le passage à la page d'annotation et à la modification de ou des élements séelctionnés
@callback(
        Output('loc', 'href'),
        Output('selected-images', 'data'),
        Input('image-table', 'active_cell'),
        Input("annotate-selection","n_clicks"),
        Input({"action":"annotate","index":ALL},"n_clicks"),
        Input("modify-selection","n_clicks"),
        Input({"action":"modify","index":ALL},"n_clicks"),
        State("image-table", "selected_rows"),
        State('loc', 'href'),
        State('image-table', 'data'),
        State('image-table', 'page_current'),
        State('image-table', 'page_size'),
)
def update_graphs(active_cell,n,ns,m,ms,images,url,data,current_page,page_size):
    # Si l'utilisateur clique directement sur une ligne
    if active_cell: 
        index = active_cell['row']+page_size*current_page
        return '/annotate_image',[data[index]['Image Name']]
    # Si c'est bien une seule carte qui a été cliqué
    if len(ctx.triggered)==1 and ctx.triggered_id!="annotate-selection" and ctx.triggered_id!="modify-selection":
        index = ctx.triggered_id['index']
        if "annotate" in ctx.triggered_id['action'] and len(ns)>=index%page_size and ns[index%page_size]!=None:
            return '/annotate_image',[data[index]['Image Name']]
        elif len(ms)>index%page_size and ms[index%page_size]!=None:
            return '/create_image',[data[index]['Image Name']]
    # Sinon s'il a sélectionné plusieurs images
    elif len(images)>0:
        if "annotate" in ctx.triggered_id: return '/annotate_image',[data[item]['Image Name'] for item in images]
        elif "modify" in ctx.triggered_id: return '/create_image',[data[item]['Image Name'] for item in images]
    # Sinon on ne fait rien
    return url,[]

# Permet la suppression de ou des élements sélectionnés
@callback(
        Output("data-to-display","data",allow_duplicate=True),
        Input("delete-selection","n_clicks"),
        Input({"action":"delete","index":ALL},"n_clicks"),
        State("image-table", "selected_rows"),
        State('image-table', 'data'),
        State('image-table', 'page_size'),
        prevent_initial_call=True
)
def update_graphs(n,ns,image_ids,data,page_size):
    images_to_delete = []
    if ctx.triggered_id=="delete-selection":
        images_to_delete.append(data[i]['Image Name'] for i in image_ids)
    elif len(ctx.triggered)==1:
        index = ctx.triggered_id['index']
        if len(ns)>=index%page_size and ns[index%page_size]!=None:
            images_to_delete.append(data[index]['Image Name'])

    if len(images_to_delete)==0:
        return no_update
    images = []
    for file in os.listdir("./assets/images/"):
        if file in images_to_delete : os.remove("./assets/images/"+file)
        else : images.append({"Biopsy ID":'Not available','Patient ID':'Not available','Image Name':file,'Diagnostic':'Not available'})
    return images

# Fais le lien entre les cartes et le tableau pour la sélection
clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='update_selected_rows'
        ),
    Output("image-table","selected_rows"),
    Input({'index':ALL,'type':'checkbox'},"checked"),
    State("image-table","selected_rows")
    )

