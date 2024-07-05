import base64
import PIL.Image
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH,ctx
import dash
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from flask import current_app
import traceback

import dash_bootstrap_components as dbc

from joblib import Memory
import pickle
from database.models import Image
from database.db import db_session
from skimage import io as skio
import os

import utils.plot_common as plot_common
import utils.common_func as common_func
from utils.shapes_to_segmentations import (
    compute_segmentations,
    blend_image_and_classified_regions_pil,
)
from utils.trainable_segmentation import multiscale_basic_features

import io
import json
import PIL.Image
from urllib import parse

memory = Memory("./joblib_cache", bytes_limit=500000000, verbose=1)
compute_features = memory.cache(multiscale_basic_features)

onto_tree_imgannot = common_func.load_onto()
classes = [
    
]
classes = []
for i in onto_tree_imgannot:
    if i["data"]["image_annotation"] is True:
        obj = {
            'text':i["text"],
            'color':i["data"]["hex_color"],
            'id':int(i["id"].split(":")[1])
        }
        classes.append(obj)
button_list = [
    int(i["id"].split(":")[1])
    for i in onto_tree_imgannot
    if i["data"]["image_annotation"] is True
]
NUM_LABEL_CLASSES = len(classes)
DEFAULT_LABEL_CLASS = classes[0]['id']

def make_default_figure(
    images=None,
    stroke_color="",
    stroke_width=3,
    shapes=[],
    source_img=None,
):
    fig = plot_common.dummy_fig()
    plot_common.add_layout_images_to_fig(fig, images)
    fig.update_layout(
        {
            "dragmode": "drawopenpath",
            "shapes": shapes,
            "newshape.line.color": stroke_color,
            "newshape.line.width": stroke_width,
            "margin": dict(l=0, r=0, b=0, t=0, pad=4),
        }
    )
    if source_img:
        fig._layout_obj.images[0].source = source_img
    return fig


# Converts image classifier to a JSON compatible encoding and creates a
# dictionary that can be downloaded
# see use_ml_image_segmentation_classifier.py
def save_img_classifier(clf, label_to_colors_args, segmenter_args):
    clfbytes = io.BytesIO()
    pickle.dump(clf, clfbytes)
    clfb64 = base64.b64encode(clfbytes.getvalue()).decode()
    return {
        "classifier": clfb64,
        "segmenter_args": segmenter_args,
        "label_to_colors_args": label_to_colors_args,
    }


def class_to_color(ontology, class_number):
    for term in ontology:
        if int(term["id"].split(":")[1]) == class_number:
            return term["data"]["hex_color"]


def color_to_class(ontology, color_hex):
    for term in ontology:
        if term["data"]["hex_color"] == color_hex:
            return int(term["id"].split(":")[1])

def show_segmentation(
    image_path,
    mask_shapes,
    features,
    segmenter_args,
    class_label_colormap,
    onto_tree_imgannot,
):
    """adds an image showing segmentations to a figure's layout"""
    # add 1 because classifier takes 0 to mean no mask
    # shape_layers = [
    #    color_to_class(class_label_colormap, shape["line"]["color"]) + 1
    #    for shape in mask_shapes
    # ]
    shape_layers = [
        color_to_class(onto_tree_imgannot, shape["line"]["color"])
        for shape in mask_shapes
    ]
    label_to_colors_args = {
        "colormap": class_label_colormap,
        "color_class_offset": 0,
    }
    segimg, seg_matrix, clf = compute_segmentations(
        mask_shapes,
        img_path=image_path,
        shape_layers=shape_layers,
        label_to_colors_args=label_to_colors_args,
        features=features,
    )
    # get the classifier that we can later store in the Store
    classifier = save_img_classifier(clf, label_to_colors_args, segmenter_args)
    segimgpng = plot_common.img_array_to_pil_image(segimg)
    return (segimgpng, seg_matrix, classifier)


def load_figure(width=10,color='black'):
        return {
            "newshape.line.width": width,
            "newshape.line.color": color,
            "xaxis":dict(showticklabels=False, showgrid=False),
            "yaxis":dict(showticklabels=False, showgrid=False),
            "margin":dict(l=0, r=0, t=0, b=0)
        }

dash.register_page(__name__, path='/annotate_image')
class Layout:
    def get_layout(args):
        return[
            dcc.Store(id="current-color",data=class_to_color(onto_tree_imgannot,DEFAULT_LABEL_CLASS),storage_type='session'),
            dcc.Store(id="masks",storage_type='memory',data=None),
            dcc.Location(id="loc-annotate",refresh=True),
            dmc.Stack([
                html.Div(id="alertbox"),
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
                                dmc.ButtonGroup(
                                    children=[
                                        dbc.Button(
                                            c['text'],
                                            id={"type": "label-class-button", "color": c['color']},
                                            style={
                                                "backgroundColor": c['color'],
                                                "border" : "1px solid transparent"
                                            },
                                        )
                                        for c in classes
                                    ],
                                ),
                                dmc.Text("Selected color : "),
                                dmc.Text(id="selected-color",miw=20,mih=20),
                                dmc.Divider(),
                                "Paintbrush Size",
                                dcc.Slider(id="brush-width",value=3,min=0,max=6,step=0.1,marks=None),
                                dmc.Divider(),
                                "Segmentation stringency range",
                                dcc.RangeSlider(min=0.01,max=20,step=0.01,marks=None,value=[0.5, 4],id="segmentation-range"),
                            ],style={"padding":"2em 1em 3em 3em"}),
                        dmc.CardSection(dmc.SimpleGrid([
                            dmc.Button("RESET IMAGE",style={'margin':"0 0 1em 0"},color='red',id="reset-image"),
                            dmc.Button([dmc.Checkbox("COMPUTE SEGMENTATION",id="show-segmentation")],style={'margin':"0 0 1em 0"},id="compute-image")
                        ],cols=2,spacing=0),withBorder=True)
                        ],withBorder=True)
                    ],withBorder=True,radius='xl',shadow='md')
                ,span=4)
            ]),
            ],style={'padding':'1em'},id="annotation-stack"),
            dcc.Store(id="current-page",storage_type='memory',data=0)
            ]
    @staticmethod
    def registered_callbacks(app):
        @app.callback(
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
                State("annotate-image","relayoutData"),
                State("current-page","data"),
                State("selected-images","data")
        )
        def save_button(_,layout,current_page,images):
            if _: 
                image = images[current_page]
                with open("./assets/masks/"+str(image).split(".")[0]+".masks", "w") as file:
                        if "shapes" in layout.keys():
                            json.dump(layout["shapes"], file, indent=4) 

            return _

        @app.callback(
                Output("current-color","data"),
                Output("selected-color","style"),
                Input({"type": "label-class-button", "color": ALL},'n_clicks'),
                prevent_initial_call=True
        )
        def update_color(n):
            return ctx.triggered_id['color'],{"backgroundColor":ctx.triggered_id['color']}


        @app.callback(
            Output("annotate-image","figure"),
            Output("current-page","data"),
            Output("current-image","children"),
            Output("image-name","children"),
            Output("loc-annotate","href"),
            Output("masks", "data"),
            Output("annotate-image", "relayoutData"),
            Input("annotate-image", "relayoutData"),
            Input("next","n_clicks"),
            Input("previous","n_clicks"),
            Input("reset-image","n_clicks"),
            Input("segmentation-range","value"),
            Input(
                {"type": "label-class-button", "color": ALL},
                "n_clicks_timestamp",
            ),
            Input("show-segmentation","checked"),
            Input("compute-image","n_clicks"),
            State("brush-width","data"),
            State("current-page","data"),
            State("selected-images","data"),
            State("loc-annotate","href"),
            State("brush-width","value"),
            State("masks", "data"),
            )
        def update_image(graph_relayoutData,next,previous,reset,range_slider_value,any_label,show_seg,n,brush_width,current_page,images,url,width,masks_data):
            if len(images)>0:
                # update current page
                if next and ctx.triggered_id == "next" :
                    if graph_relayoutData and "shapes" in graph_relayoutData.keys():
                        masks_data[current_page]["shapes"] = graph_relayoutData["shapes"]
                        graph_relayoutData =  {}
                    current_page+=1
                elif previous and ctx.triggered_id == "previous":
                    if graph_relayoutData and "shapes" in graph_relayoutData.keys():
                        masks_data[current_page]["shapes"] = graph_relayoutData["shapes"]
                        graph_relayoutData =  {}
                    current_page-=1
                current_page%=len(images)
                # get the current image
                img_path = "./assets/images/"+images[current_page]
                img = skio.imread(img_path)
                masks_path = "./assets/masks/"+str(images[current_page]).split(".")[0]+".masks"
                
                if masks_data==None:
                    masks_data = []
                    for i in range(len(images)):
                        masks_data.append({"shapes":[]})
                # print("1",current_page,masks_data)
                if ctx.triggered_id=="reset-image":
                    masks_data[current_page]["shapes"] = []
                elif graph_relayoutData:
                    if "shapes" in graph_relayoutData.keys():
                        masks_data[current_page]["shapes"] = graph_relayoutData["shapes"]
                    elif os.path.isfile(masks_path):
                        with open(masks_path, "r") as file:
                            try:
                                masks_data[current_page]["shapes"] = json.load(file)
                            except Exception:
                                masks_data[current_page]["shapes"] = []
                if any_label is None:
                    label_class_value = DEFAULT_LABEL_CLASS
                else:
                    label_class_value = button_list[
                        max(
                            enumerate(any_label),
                            key=lambda t: 0 if t[1] is None else t[1],
                        )[0]
                    ]
                fig = make_default_figure(
                    images=[img_path],
                    stroke_color=class_to_color(onto_tree_imgannot, label_class_value),
                    stroke_width=brush_width,
                    shapes=masks_data[current_page]["shapes"],
                    source_img=img_path,
                )

                segimgpng = None
                # print(show_seg,n)
                if len(masks_data[current_page]['shapes'])!=0 and (show_seg or ctx.triggered_id=="compute-image"):
                    try:
                        # On met à jour les paramètres de segmentation ?
                        segmentation_features_dict = {
                            "intensity": True,
                            "edges": True,
                            "texture": True,
                        }
                        features = compute_features(
                            img,
                            **segmentation_features_dict,
                            sigma_min=range_slider_value[0],
                            sigma_max=range_slider_value[1],
                        )
                        # On met à jour les features dcp ?
                        feature_opts = dict(
                            segmentation_features_dict=segmentation_features_dict
                        )
                        # Ah oui là on prend en compte les nouvelles valeurs
                        feature_opts["sigma_min"] = range_slider_value[0]
                        feature_opts["sigma_max"] = range_slider_value[1]
                        # C'est quoi ce genre de syntaxe pitié ;-;
                        segimgpng, seg_matrix, clf = show_segmentation(
                            img_path,
                            masks_data[current_page]["shapes"],
                            features,
                            feature_opts,
                            {
                                int(term["id"]): term["color"]
                                for term in classes
                            },
                            onto_tree_imgannot,
                        )
                    except Exception:
                        print(traceback.format_exc())
                images_to_draw = []
                if segimgpng is not None:
                    images_to_draw = [segimgpng]
                fig = plot_common.add_layout_images_to_fig(fig, images_to_draw)
                fig.update_layout(uirevision="segmentation")
                return fig,current_page,str(current_page+1)+"/"+str(len(images)),images[current_page],url,masks_data,graph_relayoutData
            return {},None,"0/0",None,"/image_annotation",dash.no_update     

        
        
        # @app.callback(
        # [
        #     Output("annotate-image", "figure"),
        #     Output("masks", "data"),
        #     Output("classifier-store", "data"),
        #     Output("classified-image-store", "data"),
        #     Output("alertbox", "children"),
        #     Output("sigma-range-slider", "value"),
        # ],
        # [
        #     Input("global-url", "href"),
        #     Input("annotate-image", "relayoutData"),
        #     Input("brush-width", "value"),
        #     Input("show-segmentation", "value"),
        #     Input("compute-image", "n_clicks"),
        #     Input("download-button", "n_clicks"),
        #     Input("segmentation-range", "value"),
        # ],
        # [
        #     State("masks", "data"),
        #     State("current-page","data"),
        #     State("selected-images","data"),
        # ],
        # )
        # def annotation_react(
        #     href,
        #     graph_relayoutData,
        #     stroke_width_value,
        #     show_segmentation_value,
        #     n,
        #     download_button_n_clicks,
        #     sigma_range_slider_value,
        #     masks_data,
        #     current_page,
        #     images
        # ):
        #     # Ok ici on va init
        #     classified_image_store_data = dash.no_update
        #     classifier_store_data = dash.no_update
        #     alertbox = html.Div()
        #     # Ce truc va servir pour vérifer un truc ?
        #     cbcontext = [p["prop_id"] for p in dash.callback_context.triggered][0]
        #     # print(cbcontext)
        #     # Ugly Source Building to Refactor
        #     # jsp nn plus
        #     key_params = dict(parse.parse_qsl(parse.urlsplit(href).query))
        #     # Je vois pas à quoi ça sert ça
        #     url_splited = parse.urlsplit(href)
        #     # Ah l'id est passé en sous main dans le body
        #     image = Image.query.get(key_params["id"])
        #     image_split_path = image.image_background_path.split("/")
        #     img = skio.imread(image.image_path)
        #     # source ? AAAAAAAH C'est le path de l'image ?
        #     source = "./assets/images/"+images[current_page]
        #     # Si c'est l'url qui trigger on charge l'image
        #     if cbcontext == "url.href":
        #         if image.mask_annot_path is not None and image.mask_annot_path != []:
        #             with open(image.mask_annot_path, "r") as file:
        #                 masks_data["shapes"] = json.load(file)
        #                 sigma_range_slider_value = [
        #                     image.sigma_range_min,
        #                     image.sigma_range_max,
        #                 ]
        #     # Si c'est le slider
        #     if cbcontext in ["sigma-range-slider.value"] or (
        #         ("Show segmentation" in show_segmentation_value)
        #         and (len(masks_data["shapes"]) > 0)
        #     ):
        #         # On met à jour les paramètres de segmentation ?
        #         segmentation_features_dict = {
        #             "intensity": True,
        #             "edges": True,
        #             "texture": True,
        #         }
        #         features = compute_features(
        #             img,
        #             **segmentation_features_dict,
        #             sigma_min=sigma_range_slider_value[0],
        #             sigma_max=sigma_range_slider_value[1],
        #         )
        #     # Si c'est le dessin
        #     if cbcontext == "graph.relayoutData":
        #         if "shapes" in graph_relayoutData.keys():
        #             masks_data["shapes"] = graph_relayoutData["shapes"]
        #         else:
        #             return dash.no_update
        #     # La taille de segmentation je suppose
        #     stroke_width = int(round(2 ** (stroke_width_value)))
        #     label_class_value = DEFAULT_LABEL_CLASS
        #         # label_class_value = class_labels[label_class_value]
        #     # AH LA PARTIE COMMUNE
        #     # Ok ici on refait une figure à partir de l'image de base et des nouveaux paramètres je suppose
        #     fig = make_default_figure(
        #         images=[image.image_path],
        #         stroke_color=class_to_color(onto_tree_imgannot, label_class_value),
        #         stroke_width=stroke_width,
        #         shapes=masks_data["shapes"],
        #         source_img=source,
        #     )

        #     # We want the segmentation to be computed
        #     # Si on veut effectivement segmenter
        #     if ("Show segmentation" in show_segmentation_value) and (
        #         len(masks_data["shapes"]) > 0
        #     ):
        #         segimgpng = None
        #         try:
        #             # On met à jour les features dcp ?
        #             feature_opts = dict(
        #                 segmentation_features_dict=segmentation_features_dict
        #             )
        #             # Ah oui là on prend en compte les nouvelles valeurs
        #             feature_opts["sigma_min"] = sigma_range_slider_value[0]
        #             feature_opts["sigma_max"] = sigma_range_slider_value[1]
        #             # C'est quoi ce genre de syntaxe pitié ;-;
        #             segimgpng, seg_matrix, clf = show_segmentation(
        #                 image.image_path,
        #                 masks_data["shapes"],
        #                 features,
        #                 feature_opts,
        #                 class_label_colormap,
        #                 onto_tree_imgannot,
        #             )
        #             # Si on veut sauver
        #             if cbcontext == "download-button.n_clicks":
        #                 classifier_store_data = clf
        #                 classified_image_store_data = plot_common.pil_image_to_uri(
        #                     blend_image_and_classified_regions_pil(
        #                         PIL.Image.open(image.image_path), segimgpng
        #                     )
        #                 )
        #                 image.sigma_range_min = sigma_range_slider_value[0]
        #                 image.sigma_range_max = sigma_range_slider_value[1]
        #                 image.seg_matrix_path = os.path.join(
        #                     current_app.config["IMAGES_FOLDER"],
        #                     image.patient_id,
        #                     image.image_name + "_seq_matrix.npy",
        #                 )
        #                 image.mask_annot_path = os.path.join(
        #                     current_app.config["IMAGES_FOLDER"],
        #                     image.patient_id,
        #                     image.image_name + "_mask_annot.json",
        #                 )
        #                 np.save(image.seg_matrix_path, seg_matrix)
        #                 image.mask_image_path = os.path.join(
        #                     current_app.config["IMAGES_FOLDER"],
        #                     image.patient_id,
        #                     image.image_name + "_mask_image.png",
        #                 )
        #                 segimgpng.save(image.mask_image_path)
        #                 image.blend_image_path = os.path.join(
        #                     current_app.config["IMAGES_FOLDER"],
        #                     image.patient_id,
        #                     image.image_name + "_blend_image.png",
        #                 )
        #                 blend_image_and_classified_regions_pil(
        #                     PIL.Image.open(image.image_path), segimgpng
        #                 ).save(image.blend_image_path)
        #                 image.classifier_path = os.path.join(
        #                     current_app.config["IMAGES_FOLDER"],
        #                     image.patient_id,
        #                     image.image_name + "_classifier.pkl",
        #                 )
        #                 # image.class_info_path = os.path.join(
        #                 #     current_app.config["IMAGES_FOLDER"],
        #                 #     image.patient_id,
        #                 #     image.image_name + "_class_info.csv",
        #                 # )
        #                 # class_to_file(seg_matrix, onto_tree_imgannot, image.class_info_path)
        #                 with open(image.mask_annot_path, "w") as file:
        #                     json.dump(masks_data["shapes"], file, indent=4)
        #                 with open(image.classifier_path, "wb") as file:
        #                     pickle.dump(clf, file)
        #                 db_session.commit()
        #                 alertbox = dbc.Alert("Annotation Saved to Database !", color="info")

        #         except Exception:
        #             print(traceback.format_exc())
        #             alertbox = dbc.Alert(
        #                 "Issues Saving to Database Please Reload The Page...", color="error"
        #             )
        #         images_to_draw = []
        #         if segimgpng is not None:
        #             images_to_draw = [segimgpng]
        #         fig = plot_common.add_layout_images_to_fig(fig, images_to_draw)
        #     # Aucune idée de à quoi ça sert ça
        #     fig.update_layout(uirevision="segmentation")
        #     return (
        #         fig,
        #         masks_data,
        #         classifier_store_data,
        #         classified_image_store_data,
        #         alertbox,
        #         sigma_range_slider_value,
        #     )
