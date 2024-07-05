import base64
from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from database import reports,images
from flask_login import current_user

icon = DashIconify(icon="line-md:upload-outline-loop",width=30)
class Layout:
    def get_layout(args):
        return [dmc.Stack([
        dmc.Title("Upload a new image"),
        dmc.TextInput(label="Patient ID",id="input-patient-id"),
        dmc.TextInput(label="Image name",id="input-image-name"),
        dcc.Upload([dmc.Button("Select a file"),dmc.Text(id="uploaded-file")],id="uploader-create",multiple=False),
        dmc.TextInput(label="Biopsy ID",id="input-biopsy-id"),
        dmc.TextInput(label="Coloration Type"),
        dmc.NumberInput(label="Age of patient at biopsy",id="input-biopsy-age",min=0),
        # dmc.Select(label="Diagnosis",data=["UNCLEAR","HEALTHY","OTHER"]),
        dmc.Select(label="Report",id="input-report-id",data=[{'label':report.name,'value':str(report.id)} for report in reports.get_all_report()]),
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
            State("input-patient-id","value"), 
            State("input-biopsy-age","value"), 
            State("input-biopsy-id","value"), 
            State("input-image-name","value"), 
            State("input-report-id","value"), 
        )
        def save_to_database(n,names,contents,selected_images,patient_id,biopsy_age,biopsy_id,img_name,report_id):
            if contents:
                img_str = str.split(contents,",")[1]
                encoded_str = base64.b64decode(img_str)
                img_path = "data/images/"+img_name+names.split(".")[-1] if not "." in img_name else ""
                fd = open(img_path,'+wb')
                fd.write(encoded_str)
                fd.close()
                images.create_image(img_name,current_user.get_id(),patient_id,biopsy_id,biopsy_age,img_path,report_id)
            return n