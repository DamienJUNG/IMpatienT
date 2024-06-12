from dash import Dash, dash,html,dcc,callback,Output,Input,State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash
from dash_iconify import DashIconify

class Layout:
    def get_layout(args):
        return [
    dmc.Stack([
        dmc.Text("IMPatienT 🗂️️ : an integrated web application to digitize, process and explore multimodal patient data.",style={'textAlign':'center'},size='2rem'),
        dmc.Image(src="assets/banner.png",radius='xl',maw='70%'),
        dmc.Container([
            html.Strong("IMPatienT"),
            " (",html.Strong("I"),html.Strong("M"),"ultimodal ",html.Strong("PATIEN"),"t da",html.Strong("T"),"a) is a web application developped in the ",html.Strong("MYO-xIA project")," for patient data digitalization and exploration.",
            dmc.Text("It features a standard vocabulary creator, optical character recognition (OCR), natural language processing (NLP), image annotation and segmentation using machine learning, interactive visualizations and automatic diagnosis prediction.")
        ],style={'textAlign':'center'})
        
    ],style={"marginLeft":"25%","width":"50%",'marginTop':'2em'},align='center')
]
    @staticmethod
    def registered_callbacks(app):
        return

# @callback(
#     Output("login","storage_type"),
#     Input("remember-me","checked")
# )
# def remember_me(checked):
#     return "session" if checked else "local"