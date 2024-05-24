from dash import callback, State, Input,Output,clientside_callback,ClientsideFunction,dcc,html,ALL,MATCH
import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify

dash.register_page(__name__, path='/create_image')

icon = DashIconify(icon="line-md:upload-outline-loop",width=30)

layout = [dmc.Stack([
        dmc.Title("Modify/Upload a new image"),
        dmc.TextInput(label="Patient ID"),
        dcc.Upload([dmc.Button("Select a file"),dmc.Text(id="uploaded-file")],id="uploader-create",multiple=False),
        dmc.TextInput(label="Biopsy ID"),
        dmc.TextInput(label="Coloration Type"),
        dmc.NumberInput(label="Age of patient at biopsy",min=0),
        dmc.Select(label="Diagnosis",data=["UNCLEAR","HEALTHY","OTHER"]),
        dmc.Button("Save changes",leftSection=icon,rightSection=icon,style={"font-size":"1.15em"})
    ],style={"paddingLeft":"30em","paddingRight":"30em"})]

@callback(
    Output("uploaded-file","children"),
    Input("uploader-create","filename"),
    State("selected-images","data")
)
def upload_file(new,old):
    if new:
        return new
    if old :
        if type(old)==type(""):
            return old
        else:
            return old[0]
    return "Aucun fichier choisi"