# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 22:46:28 2021
@author: rosie
"""
#VISIT http://127.0.0.1:8050/ IN YOUR BROWSER TO VIEW DASHBOARD
#Some modules may have to be installed .... 
#pip install pyproj
#pip install dash_bootstrap_components 
#pip install dash
#pip install plotly

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output
from pyproj import Proj, transform
import dash_bootstrap_components as dbc


#this is necessary to run, otherwise the urls used to fetch pictures for cottages was shortened to 50
pd.options.display.max_colwidth = 100


#---------------FUNCTIONS--------------------------------
#FUNCTIONS TO EXTRACT PARTS FROM THE ADDRESS IN ORIGINAL DATA
def extracttown(address ):
    try:
        word_list = address.split(', ')
        return word_list[-2]
    except ValueError:
        return ""
    
def extractname(address ):
    try:
        word_list = address.split(', ')
        return word_list[0]
    except ValueError:
        return ""
    
#FUNCTION TO CONVERT LONG/LAT TO ITM COORDS SO ALL DATASETS HAVE MATCHING COORDS
#Source: https://gis.stackexchange.com/questions/32418/python-script-to-convert-lat-long-to-itm-irish-transverse-mercator
def reproject_wgs_to_itm(longitude, latitude):
    prj_wgs = Proj(init='epsg:4326')
    prj_itm = Proj(init='epsg:2157')
    x, y = transform(prj_wgs, prj_itm, longitude, latitude)
    return x, y    





#----------------------DATA READING AND CLEANING----------------------------------------
#THATCED HOUSING DF1
df1 = pd.read_csv('https://data-roscoco.opendata.arcgis.com/datasets/93be4fedbb424e2dad79dc1f36a42d24_0.csv?outSR=%7B%22latestWkid%22%3A2157%2C%22wkid%22%3A2157%7D')
#extract town from address
df1['Name']=""
df1['Town']=""
df1['Type']="Thatched Building"
for index, row in df1.iterrows():
    df1.at[index,'Town'] = extracttown(row['Address']) 
    df1.at[index,'Name'] = extractname(row['Address']) 


df1['NIAH_Ref_No'].fillna('Not Registered', inplace=True)
df1.loc[(df1.NIAH_Ref_No != 'Not Registered'),'NIAH_Ref_No']='NIAH Registered'
df1=df1.drop(['Address','FID','RPS_Ref_No','Site_Name'], axis=1)
df1.rename(columns={'NIAH_Ref_No':'Facility_type'},inplace=True)


#GRAVEYARD FACILITIES DF2
df2 = pd.read_csv('https://data-roscoco.opendata.arcgis.com/datasets/bdc41fe8ffb242e3a97e06780a4634ee_0.csv?outSR=%7B%22latestWkid%22%3A2157%2C%22wkid%22%3A2157%7D')
df2.columns
df2["Notes"] = df2["DescriptionOfGraveyard"] +" " +df2["Notes"]
df2.rename(columns={'WebsiteLink':'Web','Parish':'Town','Denomination':'Facility_type','GraveyardName':'Name',"URL_1":"Photo"},inplace=True)
df2 = df2[df2['Type'].isin(['Graveyard']) == True]
df2 = df2[df2['CurrentStatusOfGraveyard'].isin(['OPEN']) == True]
df2=df2.drop(['DescriptionOfGraveyard','Townland','DateOfOpeningOfGraveyard','TitlesOfPublishedLocalReferenc','RecordOfMonumentsAndPlaces_RMP','FID','LocationOfInscriptions','ID','Diocese','NationalInventoryOfArchitectur','RecordOfProtectedStructure_RPS','CurrentStatusOfGraveyard','Owner','NearestRoad','RegisterOfBurialsStartDate'], axis=1)
df2.columns


#SPORTS FACILITIES DF3
df3 = pd.read_csv('https://data-roscoco.opendata.arcgis.com/datasets/b8342d8e1ef6420caa0c2f3e12624e61_0.csv?outSR=%7B%22latestWkid%22%3A2157%2C%22wkid%22%3A2157%7D')
df3['Town']=""
df3['Facility_type']=df3['Type']
df3['Type']="Sports Facility"
for index, row in df3.iterrows():
    df3.at[index,'Town'] = extracttown(row['Address'])
    co_ords= (reproject_wgs_to_itm(df3.at[index,'WGS84Longitude'], df3.at[index,'WGS4Latitude']))
    df3.at[index,'WGS84Longitude'] = co_ords[0]
    df3.at[index,'WGS4Latitude'] = co_ords[1]
    
df3.rename(columns={'NAME':'Name','WGS84Longitude':'X','WGS4Latitude':'Y'},inplace=True)
df3=df3.drop(['Telephone','OBJECTID', 'Eircode','Address',], axis=1)



#merge dataframes
pieces = (df1,df2,df3)
amenities = pd.concat(pieces, ignore_index = True)
#Reorder columes
amenities = amenities[[  'Name','Type','Facility_type', 'Town','Photo', 'Notes',   'Web',
       'Streetview_Link', 'Civil_Parish', 'ConditionOfGraveyard', 'Access', 'WheelchairAccess',
       'RegisterOfBurials', 'Parking','X', 'Y']]

#change some town names as some have different spellings
amenities.loc[(amenities.Town == 'Ballintubber'),'Town']='Ballintober'
amenities.loc[(amenities.Town == 'Kiltoom & Cam'),'Town']='Kiltoom'
amenities.loc[(amenities.Town == 'Nr Lanesborough'),'Town']='Lanesborough'
amenities.loc[(amenities.Town == 'Kiltullagh.'),'Town']='Kiltullagh'
amenities.loc[(amenities.Town == 'Castlerera'),'Town']='Castlerea'
amenities.loc[(amenities.Town == 'Loughglinn'),'Town']='Loughglynn'
amenities.loc[(amenities.Town == 'Lanesboro'),'Town']='Lanesborough'
amenities.loc[(amenities.Town == 'Lecarrow Village'),'Town']='Lecarrow'
amenities.loc[(amenities.Town == 'Porteen'),'Town']='Ballinasloe'#porteen is a neighbourhood in ballinasloe
amenities.loc[(amenities.Town == 'Roscommon Town'),'Town']='Roscommon'
amenities.loc[(amenities.Town == 'Athlone Road'),'Town']='Athlone'
amenities.loc[(amenities.Town == 'Lecarrow Village'),'Town']='Lecarrow'
amenities.loc[(amenities.Town == 'Glinsk'),'Town']='Suck Valley Way'#group these smaller towns into their collective area
amenities.loc[(amenities.Town == 'Ballintober'),'Town']='Suck Valley Way'
amenities.loc[(amenities.Town == 'Castlerea'),'Town']='Suck Valley Way'
amenities.loc[(amenities.Town == 'Mount Talbot'),'Town']='Suck Valley Way'
amenities.loc[(amenities.Town == 'Athleague'),'Town']='Suck Valley Way'

#fix some wonky values
amenities.loc[(amenities.Facility_type == 'Cof I'),'Facility_type']='C of I'

#Combine some sports as 'other' as only one of each
amenities.loc[(amenities.Facility_type == 'Motor Sports'),'Facility_type']='Other'
amenities.loc[(amenities.Facility_type == 'Boxing'),'Facility_type']='Other'
amenities.loc[(amenities.Facility_type == 'Outdoor Water Sports'),'Facility_type']='Other'
amenities.loc[(amenities.Facility_type == 'Equestrian'),'Facility_type']='Other'
amenities.loc[(amenities.Facility_type == 'Athletics'),'Facility_type']='Other'

#extend ambigious names/shorten lengthy ones
amenities.loc[(amenities.Facility_type == 'RC'),'Facility_type']='Roman Catholic'
amenities.loc[(amenities.Facility_type == 'C of I'),'Facility_type']='Church of Ireland'
amenities.loc[(amenities.Facility_type == 'Handball Courts & Alleys'),'Facility_type']='Handball Courts'
amenities.loc[(amenities.Facility_type == 'Swimming Pools & Leisure Centres'),'Facility_type']='Swim/Leisure'


#drop rows with no town specified
amenities['Town'].replace('', np.nan, inplace=True)
amenities.dropna(subset=['Town'], inplace=True)












#-----------------Dashboard CREATION-------------------------------
#-----------setting up environment---------------
#colour codes - https://htmlcolorcodes.com/
colors = {
    'background': '#F5F9F6',
    'text': '#0C2D5B'
}

#external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app = dash.Dash(external_stylesheets=[dbc.themes.GRID])

#change default plotly colours
pio.templates["myname"] = go.layout.Template(
    layout=go.Layout(
        colorway=['#225EB2', '#6F6FBD', '#902E49']
    )
)
pio.templates.default = 'myname'



#--------------------create our figures----------------
#------------------------hist 1 -----------------------------------
#CREATES hist1 A HIST X(TOWN NAME) Y(COUNT) BY FACILITY TYPE
amenities_grouped = amenities.groupby(['Type','Town']).count()
amenities_grouped=amenities_grouped.reset_index(level=[0, 1])
amenities_grouped.rename(columns={'Name':'Count'},inplace=True)
hist1 = px.bar(amenities_grouped, x="Town", y="Count",color="Type",barmode='group',title='COUNT BY TOWN ')

hist1.update_xaxes(title='', visible=True, showticklabels=True)

hist1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
        legend=dict(
        x=0.8,
        y=0.9,
        title='Click to filter',
        traceorder="normal",
        font=dict(
            family="sans-serif",
            size=12,
            color="black"
        ),
    )
)
hist1.update_layout(margin = dict(t=50, l=50, r=30, b=140))

#------------------------pie1 -----------------------------------NOT USED IN THE END!!!
#CREATES pie1 A pie chart of sports types available

#sports = amenities[amenities['Type']=='Sports Facility']
#sports_grouped = sports.groupby(['Facility_type','Town']).count()
#sports_grouped=sports_grouped.reset_index(level=[0, 1])
#sports_grouped.rename(columns={'Name':'Count'},inplace=True)
#pie1 = px.pie(sports_grouped, values='Count', names='Facility_type')
#pie1.update_layout(
#    plot_bgcolor=colors['background'],
#    paper_bgcolor=colors['background'],
#    font_color=colors['text']
#)

#pie1.update_layout(margin = dict(t=0, l=0, r=0, b=0))



#------------------------scat1 -----------------------------------
#scatters points according to ITM coordinates... ....tred geo scatter to underlay map to be difficult/time consuming at present as we're in itm coords
scat1 = px.scatter(x=amenities['X'], y=amenities['Y'],color=amenities['Type'],width=780, height=450, 
                title="AMENITIY LOCATION ")

scat1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


scat1.update_layout(
     xaxis_title="longitude",
    yaxis_title="latitude",
    legend=dict(
        x=0.1,
        y=.1,
        title='Click to filter',
        traceorder="normal",
        font=dict(
            family="sans-serif",
            size=12,
            color="black"
        ),
    )
)

scat1.update_layout(margin = dict(t=52))


#------------------------sun1 -----------------------------------
#CREATES sun1 a sunburst chart of facility types
sunburst_df = amenities.groupby(by=["Type", "Town", "Facility_type"]).count()
sunburst_df = sunburst_df.reset_index(level=[0, 1,2])
sunburst_df.rename(columns={'Name':'Count'},inplace=True)
sun1 = px.sunburst(sunburst_df,
                  path=["Type", "Facility_type"],
                  values='Count',
                  width=700, height=480,title='PROPORTION OF AMENITIES<br>(click centre to expand)<br>',)


sun1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
sun1.update_layout(margin = dict(t=100, l=0, r=0, b=15))






#-------------------subsetting df for use later in picture div--------
just_thatch = amenities[amenities["Type"] == "Thatched Building"]
just_thatch = just_thatch[["Name", "Photo"]]
just_thatch.dropna(subset=['Photo'], inplace=True)

just_grave = amenities[amenities["Type"] == "Graveyard"]
just_grave = just_grave[["Name", "Photo"]]
just_grave.dropna(subset=['Photo'], inplace=True)


#----------------------------DASH app layout-----------------
app.layout = html.Div( style={'backgroundColor': colors['background']},children=[
  #div for heading
    html.H1(
        children='ROSCOMMON AREA AMENITES - HERITAGE, SPORTS & BURIAL GROUNDS',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    #div for hist
    html.Div([
        dcc.Graph(
            id='hist_town',
            figure=hist1
            ),
        ],
        style={'width': '66.5%','height':'70%','float': 'left', 'display': 'inline-block'}
        ),
    
    
    
     
      
      #DIV for picture finding    
           html.Div([
      html.Div(children=[
    html.P(['']),
    dcc.Dropdown(id='my-input', options=[
        {'label': i, 'value': i} for i in just_thatch.Name.unique()
    ], multi=False, placeholder='Choose a Cottage in Roscommon to view...'),

    html.Div(id='my-output'),
        ], style={"width": "100%"},),
        ],
        style={'width': '30%', 'display': 'inline-block', 'float': 'right','backgroundColor': colors['background']},
        ),
    
     
     #div for scatter plot
    html.Div([
        dcc.Graph(
            id='scatter',
            figure=scat1
            )
        ],
        style={'width': '34%', 'display': 'inline-block', 'float': 'left','backgroundColor': colors['background']},
        ),
                
    
           #div sunburst plot amenities
      html.Div([
        dcc.Graph(
            id='amenitiy_sunburst',
            figure=sun1
            )
        ],
        style={'width': '33.9%', 'display': 'inline-block', 'float': 'middle','backgroundColor': colors['background']},
        ),
           
          
        #div for graveyard pic
             html.Div([
      html.Div(children=[
    html.P(['']),
    dcc.Dropdown(id='my-input1', options=[
        {'label': i, 'value': i} for i in just_grave.Name.unique()
    ], multi=False, placeholder='Choose a Graveyard in Roscommon to view...'),

    html.Div(id='my-output1'),
        ], style={"width": "100%"},),
        ],
        style={'width': '30%', 'display': 'inline-block', 'float': 'right','backgroundColor': colors['background']},
        ),
          
 
    
       





    ],
)          
    


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)

#Code to update cottage picture
def update_output_div(input_value):
    input_value=str(input_value)
    want=just_thatch.loc[just_thatch['Name']==input_value, 'Photo'].to_string(index=False).strip()
    url = want
    return html.Img(id='pic_thatch', src=url,style={'height':'85%', 'width':'90%'})



@app.callback(
    Output(component_id='my-output1', component_property='children'),
    Input(component_id='my-input1', component_property='value')
)
def update_output_div_but_make_it_graveyards(input_value):
    input_value=str(input_value)
    want=just_grave.loc[just_grave['Name']==input_value, 'Photo'].to_string(index=False).strip()

    url = want
    return html.Img(id='pic_grave', src=url,style={'height':'85%', 'width':'90%'})






if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)





