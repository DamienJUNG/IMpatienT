import base64
import PIL.Image
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH,ctx
import dash
import plotly.express as px
import dash_mantine_components as dmc

dash.register_page(__name__, path='/annotate_image')

layout = [
            dcc.Location(id="loc-annotate",refresh=True),
            dmc.Stack([
                dmc.Card([
                dmc.CardSection("Explanation",withBorder=True,className="card-title"),
                dmc.CardSection(dmc.Stack([
                    dmc.Text("If your image is not displayed please hit F5 to refresh the page, it should solve most issues.",style={'font-weight':'bold'}),
                    dmc.Text("This is the image annotation tool interface. Select the standard vocabulary term and draw on the image to annotate parts of the image. Then check the 'Compute Segmentation' tickbox to automatically expands your annotations to the whole image. You may add more marks to clarify parts of the image where the classifier was not successful"),
                    dmc.Group([
                        dmc.Text("You are currently editting : "),
                        dmc.Text(id="image-name",style={'font-weight':'bold'})
                    ],gap='sm')
                ],style={'padding':'1em'})),
                ],withBorder=True,radius='xl',shadow='md'),
            dmc.Grid([
                dmc.GridCol(
                    dmc.Card([
                        dmc.CardSection(dmc.Flex([
                            dmc.Button("<-",id="previous",variant='outline',color='dark'),
                            "Image Viewer",dmc.Text(id="current-image"),
                            dmc.Button("->",id="next",variant='outline',color='dark')
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
                                    dmc.Button("Cytoplasm",color='green'),
                                    dmc.Button("Intercellular spaces",color="black"),
                                    dmc.Button("Nuclei",color="red"),
                                    dmc.Button("Rods",color="cyan"),
                                    dmc.Button("Core",color="orange"),
                                ]),
                                dmc.Divider(),
                                "Paintbrush Size",
                                dmc.Slider(),
                                dmc.Divider(),
                                "Segmentation stringency range",
                                dmc.RangeSlider(),
                            ],style={"padding":"2em 1em 3em 3em"}),
                        dmc.CardSection(dmc.Button("COMPUTE SEGMENTATION",fullWidth=True,style={'margin':"0 1em 1em 1em"}),withBorder=True)
                        ],withBorder=True)
                    ],withBorder=True,radius='xl',shadow='md')
                ,span=4)
            ]),
            ],style={'padding':'1em'}),
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
        print(fig['data'])
        img_str = str.split(fig['data'][0]['source'],",")[1]
        encoded_str = base64.b64decode(img_str)
        fd = open("assets/images/"+"teeeeeeeeeeeeeeeeeeeeeeeest.png",'wb')
        fd.write(encoded_str)
        fd.close()

    return _

@callback(
    Output("annotate-image","figure"),
    Output("current-page","data"),
    Output("current-image","children"),
    Output("image-name","children"),
    Output("loc-annotate","href"),
    Input("next","n_clicks"),
    Input("previous","n_clicks"),
    State("current-page","data"),
    State("selected-images","data"),
    State("loc-annotate","href")
    )
def update_image(next,previous,current_page,images,url):
    if len(images)>0:
        if next or previous :
            if ctx.triggered_id == "next": current_page+=1
            elif ctx.triggered_id == "previous": current_page-=1
        current_page%=len(images)
        img = PIL.Image.open("./assets/images/"+images[current_page])
        return px.imshow(img,binary_format=format,
                        binary_compression_level=0,
                        width=img.width if img.width<1200 else 1200,
                        height=img.height if img.height<1200 else 1200),current_page,str(current_page+1)+"/"+str(len(images)),images[current_page],url
    return {},None,"0/0",None,"/image_annotation"