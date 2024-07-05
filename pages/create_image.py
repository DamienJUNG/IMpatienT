import base64
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

icon = DashIconify(icon="line-md:upload-outline-loop",width=30)
class Layout:
    def get_layout(args):
        return [dmc.Stack([
        dmc.Title("Modify / Upload a new image"),
        dmc.TextInput(label="Patient ID"),
        dcc.Upload([dmc.Button("Select a file"),dmc.Text(id="uploaded-file")],id="uploader-create",multiple=False),
        dmc.TextInput(label="Biopsy ID"),
        dmc.TextInput(label="Coloration Type"),
        dmc.NumberInput(label="Age of patient at biopsy",min=0),
        dmc.Select(label="Diagnosis",data=["UNCLEAR","HEALTHY","OTHER"]),
        dmc.Button("Save changes",id="save-image",leftSection=icon,rightSection=icon,style={"font-size":"1.15em"})
    ],style={"paddingLeft":"30em","paddingRight":"30em"})]

    @staticmethod
    def registered_callbacks(app):
        @app.callback(
            Output("uploaded-file","children"),
            Input("uploader-create","filename"),
            State("selected-images","data"),    
        )
        def upload_file(new,old):
            if new:
                return new
            if old :
                if type(old) is list:
                    return old[0]
                return old
            return "Aucun fichier choisi"

        @app.callback(
            Output("save-image","n_clicks"),
            Input("save-image","n_clicks"),
            State("uploader-create","filename"),
            State("uploader-create","contents"),
            State("selected-images","data"),  
        )
        def save_to_database(n,names,contents,selected_images):
            if contents:
                for i,file in enumerate(contents):
                    img_str = str.split(file,",")[1]
                    encoded_str = base64.b64decode(img_str)
                    fd = open("assets/images/"+names[i],'+wb')
                    fd.write(encoded_str)
                    fd.close()