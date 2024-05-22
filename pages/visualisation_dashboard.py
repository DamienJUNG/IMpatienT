# Import packages
import dash
from dash import dcc
import plotly.graph_objs as go
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.metrics import confusion_matrix

with open("assets/text_reports.csv", "r") as read_file:
    onto = pd.read_csv(read_file,sep=',')

dash.register_page(__name__, path='/visualisation_dashboard')

# Récupération de la partie du df sur les genes
corr_columns = onto.columns[15:]
threshold = 10
corr_values = onto[corr_columns].dropna(axis=1, thresh=threshold).replace({0:-1})
corr_values = corr_values.corr().fillna(0)

# Récupération de la partie du df sur les diagnostiques et leur prédiction
boqa_values = onto[onto.columns[11:13]]

df_no_unclear = boqa_values[(boqa_values["conclusion"] != "UNCLEAR") & (boqa_values["conclusion"] != "OTHER")]
y_true = df_no_unclear["conclusion"].to_list()
y_pred = df_no_unclear["BOQA_prediction"].to_list()
labels = ["No_Pred"] + df_no_unclear["conclusion"].unique().tolist()

matrix_results = confusion_matrix(
        y_true,
        y_pred,
        labels=labels,
    )

fig_matrix = ff.create_annotated_heatmap(
    z=matrix_results,
    x=labels,
    y=labels,
    colorscale="Viridis",
)
fig_matrix.update_layout(
    title="Confusion matrix of histologic reports classification by BOQA",
    xaxis_title="Predicted Class (BOQA)",
    yaxis_title="True Class",
    showlegend=False,
)
fig_matrix["layout"]["yaxis"]["autorange"] = "reversed"
fig_matrix["layout"]["xaxis"]["side"] = "bottom"
# On récupère la liste des prédictions là où le diagnostique était UNCLEAR
df_unclear = boqa_values[(boqa_values["conclusion"] == "UNCLEAR")]['BOQA_prediction']


# C'était présent dans le code initial mais on obtient le même jeu de données avec et sans ce morceau là
# col_row_to_drop = []
# for i in range(len(corr_values)):
#     if corr_values.iloc[i, i] == 0:
#         col_row_to_drop.append(corr_values.columns[i])

# corr_values.drop(col_row_to_drop, axis=1, inplace=True)
# corr_values.drop(col_row_to_drop, axis=0, inplace=True)

# Remplacement des NA et extraction du reste
onto = onto.fillna('N/A')
def make_it_heatmap(data,x_label,y_label,title="",x_axis="",y_axis="",text=False,colorbar=True):
    fig = go.Figure(data=
        go.Heatmap(
        x=x_label,
        y=y_label,
        z=data,
        colorscale="RdBu",
        texttemplate="%{z}" if text else "",
        showscale=colorbar
    ),layout={
        'xaxis':{'title':x_axis},
        'yaxis':{'title':y_axis},
        'title':title
    })
    fig.update_layout(width = 800, height = 800,autosize = True)
    return dcc.Graph(figure=fig)

def make_it_graph(data,title="",xaxis="",yaxis=""):
    df = pd.DataFrame({
        'label':data.unique(),
        'count':[data.value_counts()[item] for item in data.unique()]
    }).sort_values(by='count',ascending=False)
    fig = go.Figure(
        data={
            'x':df['label'],
            'y':df['count'],
            'type':'bar',
            'marker' : { "color" : (df['count'].index)},
            'text':df['count']
            }
            ,
        layout={
            'xaxis':{'title':xaxis},
            'yaxis':{'title':yaxis},
            'title':title
        }
    )
    return dcc.Graph(figure=fig)

age_biopsie = []
for item in onto['age_biopsie']:
    if item=='N/A':age_biopsie.append('N/A')
    elif item>=18: age_biopsie.append('Adult (>=18 years)')
    elif item>=3: age_biopsie.append('Child (3-17)')
    else : age_biopsie.append('Newborn (2<=years)')
onto['age_biopsie'] = pd.DataFrame(age_biopsie)

layout = [
    dmc.Grid(children=[
        # Muscles
        dmc.GridCol(make_it_graph(onto['muscle_prelev'],'Cohort repartition by muscle','Biopsy muscle','Number of reports'),span=6),
        dmc.GridCol(make_it_graph(onto['age_biopsie'],'Cohort repartition by age','Age','Number of reports'),span=6),
        # Genes
        dmc.GridCol(make_it_graph(onto['gene_diag'],'Cohort repartition by muscle','Biopsy muscle','Number of reports'),span=6),
        dmc.GridCol(make_it_graph(onto['conclusion'],'Cohort repartition by myopathy diagnosis','Myopathy class','Number of reports'),span=6),
        # Correlation
        dmc.GridCol(make_it_heatmap(corr_values,corr_values.columns,corr_values.columns,"Standard Vocabulary terms correlation matrix (treshold n>=%s)"%threshold)),
        dmc.GridCol(dcc.Graph(figure=fig_matrix),span=6),
        dmc.GridCol(make_it_graph(df_unclear,"Prediction of UNCLEAR reports by BOQA"),span=6),

    ],style={'padding':'0 10em 0 10em'})
]