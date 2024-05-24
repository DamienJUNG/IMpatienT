import base64
import PIL.Image
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH,ctx
import dash
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def load_figure(width=10,color='black'):
        return {
            "newshape.line.width": width,
            "newshape.line.color": color,
            "xaxis":dict(showticklabels=False, showgrid=False),
            "yaxis":dict(showticklabels=False, showgrid=False),
            "margin":dict(l=0, r=0, t=0, b=0)
        }

dash.register_page(__name__, path='/annotate_image')

layout = [
            dcc.Store(id="current-color",data='black',storage_type='memory'),
            dcc.Location(id="loc-annotate",refresh=True),
            dmc.Stack([
                dmc.Card([
                dmc.CardSection("Explanation",withBorder=True,className="card-title"),
                dmc.CardSection(dmc.Stack([
                    dmc.Text("If your image is not displayed please hit F5 to refresh the page, it should solve most issues.",style={'fontWeight':'bold'}),
                    dmc.Text("This is the image annotation tool interface. Select the standard vocabulary term and draw on the image to annotate parts of the image. Then check the 'Compute Segmentation' tickbox to automatically expands your annotations to the whole image. You may add more marks to clarify parts of the image where the classifier was not successful"),
                    dmc.Group([
                        dmc.Text("You are currently editting : "),
                        dmc.Text(id="image-name",style={'fontWeight':'bold'})
                    ],gap='sm')
                ],style={'padding':'1em'})),
                ],withBorder=True,radius='xl',shadow='md'),
            dmc.Grid([
                dmc.GridCol(
                    dmc.Card([
                        dmc.CardSection(dmc.Flex([
                            dmc.ActionIcon(DashIconify(icon="line-md:arrow-left",width=25,color="black"),id="previous",variant='outline',color='dark',radius='xl',style={'display':'None'}),
                            "Image Viewer",dmc.Text(id="current-image"),
                            dmc.ActionIcon(DashIconify(icon="line-md:arrow-right",width=25,color="black"),id="next",variant='outline',color='dark',radius='xl',style={'display':'None'})
                        ],justify='stretch',align='center',gap='1em'),withBorder=True,className="card-title"),
                        dmc.CardSection(dmc.Flex(dcc.Graph(id="annotate-image",
                            config={"modeBarButtonsToAdd": [
                                "drawline",
                                "drawopenpath",
                                "drawclosedpath",
                                "drawcircle",
                                "drawrect",
                                "eraseshape",
                            ]}),justify='center')),
                        dmc.CardSection(dmc.Button("Save changes to database",id="save-button",fullWidth=True,color='darkGreen'),withBorder=True)
                    ],withBorder=True,radius='xl',shadow='md')
                ,span=8),
                dmc.GridCol(            
                    dmc.Card([
                        dmc.CardSection("Tool-Box",withBorder=True,className='card-title'),
                        dmc.CardSection([
                            dmc.Stack([
                                "Standard Vocabulary Term",
                                dmc.ButtonGroup([
                                    # Si les couleurs changent, modifier dans color ET dans l'id
                                    dmc.Button("Cytoplasm",color='green',id={'name':'color-button','color':'green'}),
                                    dmc.Button("Intercellular spaces",color="black",id={'name':'color-button','color':'black'}),
                                    dmc.Button("Nuclei",color="red",id={'name':'color-button','color':'red'}),
                                    dmc.Button("Rods",color="cyan",id={'name':'color-button','color':'cyan'}),
                                    dmc.Button("Core",color="orange",id={'name':'color-button','color':'orange'}),
                                ]),
                                dmc.Divider(),
                                "Paintbrush Size",
                                dmc.Slider(id="brush-width",value=10),
                                dmc.Divider(),
                                "Segmentation stringency range",
                                dmc.RangeSlider(value=[0,10],id="segmentation-range"),
                            ],style={"padding":"2em 1em 3em 3em"}),
                        dmc.CardSection(dmc.ButtonGroup([
                            dmc.Button("RESET IMAGE",fullWidth=True,style={'margin':"0 0 1em 0"},color='red',id="reset-image"),
                            dmc.Button("COMPUTE SEGMENTATION",fullWidth=True,style={'margin':"0 0 1em 0"},id="compute-image")
                        ]),withBorder=True)
                        ],withBorder=True)
                    ],withBorder=True,radius='xl',shadow='md')
                ,span=4)
            ]),
            ],style={'padding':'1em'},id="annotation-stack"),
            dcc.Store(id="current-page",storage_type='memory',data=0)
        ]

@callback(
        Output("previous","style"),
        Output("next","style"),
        Input("current-page","data"),
        State("selected-images","data")
)
def display_button(_,images):
    if len(images)<2: return {'display':'None'},{'display':'None'}
    else:return {},{}

@callback(
        Output("save-button","n_clicks"),
        Input("save-button","n_clicks"),
        State("annotate-image","figure")
)
def display_button(_,fig):
    if _: 
        fig['layout']['xaxis'] = {}
        fig['layout']['yaxis'] = {}
        new_fig = go.Figure(fig)
        new_fig.update_layout(load_figure()),
        new_fig.write_image("assets/images/"+"teeeeeeeeeeeeeeeeeeeeeeeest.png")

    return _

@callback(
        Output("current-color","data"),
        Input({'name':'color-button','color':ALL},'n_clicks'),
        prevent_initial_call=True
)
def update_color(n):
    return ctx.triggered_id['color']

@callback(
        Output("annotate-image","figure",allow_duplicate=True),
        Input("brush-width","value"),
        Input("current-color","data"),
        State("annotate-image","figure"),
        prevent_initial_call=True
)
def update_brush_width(width,color,fig):
    fig['layout']['xaxis'] = {}
    fig['layout']['yaxis'] = {}
    new_fig = go.Figure(fig)
    new_fig.update_layout(load_figure(width,color))
    return new_fig


@callback(
    Output("annotate-image","figure"),
    Output("current-page","data"),
    Output("current-image","children"),
    Output("image-name","children"),
    Output("loc-annotate","href"),
    Input("next","n_clicks"),
    Input("previous","n_clicks"),
    Input("reset-image","n_clicks"),
    State("current-page","data"),
    State("selected-images","data"),
    State("loc-annotate","href"),
    State("brush-width","value"),
    State("current-color","data"),
    )
def update_image(next,previous,reset,current_page,images,url,width,color):
    if len(images)>0:
        if next or previous :
            if ctx.triggered_id == "next": current_page+=1
            elif ctx.triggered_id == "previous": current_page-=1
        current_page%=len(images)
        img = PIL.Image.open("./assets/images/"+images[current_page])
        fig = go.Figure(px.imshow(img,
                        width=img.width if img.width<1200 else 1200,
                        height=img.height if img.height<1200 else 1200))
        fig.update_layout(load_figure(width,color))
        return fig,current_page,str(current_page+1)+"/"+str(len(images)),images[current_page],url
    return {},None,"0/0",None,"/image_annotation"