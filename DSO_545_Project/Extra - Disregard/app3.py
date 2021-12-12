# data manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

# plotly 
import plotly.express as px
import plotly.graph_objects as go

# dashboards
import dash
from dash import dcc
from dash import html
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import date
from dash import dash_table

Dest = ['London', 'Paris', 'Mexico City']
LAX = np.array([[53.5500,2.4333], [48.8566, 2.3522],[19.432608,-99.133209]] )
LAX_df = pd.DataFrame(LAX, index=Dest, columns=[['lat', 'lon']]) 

fig = go.Figure()

for i in Dest:
    fig.add_trace(go.Scattergeo(
        lon = [-118.410042, LAX_df.loc[i][1]],
        lat = [33.942791, LAX_df.loc[i][0]],
        hoverinfo = 'text',
        mode = 'lines',
        marker = dict(
            size = 2,
            color = 'rgb(0,0,128)',
            line = dict(
                width = 3,
                color = 'rgb(0,0,128)'
            )
        )))



fig.update_layout(
    title_text = 'Contour lines over globe<br>(Click and drag to rotate)',
    showlegend = False,
    geo = dict(
        showland = True,
        showcountries = True,
        showocean = True,
        countrywidth = 0.5,
        landcolor = 'rgb(102, 204, 0)',
        lakecolor = 'rgb(137, 207, 240)',
        oceancolor = 'rgb(137, 207, 240)',
        projection = dict(
            type = 'orthographic',
            rotation = dict(
                lon = -100,
                lat = 40,
                roll = 0
            )
        ),
        lonaxis = dict(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        ),
        lataxis = dict(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        )
    )
)

tabs_styles = {
    'height': '30px',
    'align-items': 'center'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'border-radius': '15px',
    'background-color': '#F2F2F2',
    'box-shadow': '4px 4px 4px 4px lightgrey',
 
}
 
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'border-radius': '15px',
}

app = dash.Dash(__name__)


app.layout = html.Div([
    
    html.Div([
        html.Div([
        html.H1(children='AIR TRAVEL COVID-19 DATA'),
        html.Label('We are interested in investigating the impact that COVID-19 had on air travel within the United States.', 
                    style={'color':'rgb(33 36 35)'}), 
        html.Img(src=app.get_asset_url('covid.png'), style={'position': 'relative', 'width': '80%', 'left': '10px', 'top': '-800x'}),
    ], className='side_bar'),

    html.Div([
        html.Div([
            html.Div([
                dcc.Tabs(id = "tabs-styled-with-inline", value = 'tab-1', children = [
                dcc.Tab(label = 'Airport Info', value = 'tab-1', style = tab_style, selected_style = tab_selected_style),
                dcc.Tab(label = 'COVID Data', value = 'tab-2', style = tab_style, selected_style = tab_selected_style),
                dcc.Tab(label = 'Airport Data', value = 'tab-3', style = tab_style, selected_style = tab_selected_style),
            ], style = tabs_styles),
            html.Div(id = 'tabs-content-inline')
            ], className = "create_container3 eight columns", ),

            html.Div([
                dbc.RadioItems(
                id='ani_veg', 
                className='radio',
                options=[dict(label='LAX', value=0), dict(label='JFK', value=1), dict(label='ATL', value=2), dict(label='ORD', value=3), dict(label='DFW', value=4)],
                value=0, 
                inline=True,
                labelStyle= {'display':'inline-block'}
            ),
            ], className='box', style={'margin-left': '200px', 'padding-top':'5px', 'padding-bottom':'5px','heigth':'5%'}),

                html.Div([
                    html.Label('Airport Data At A Glance', style={'font-size': 'medium'}),
                    html.Br(),
                    html.Br(),
                    html.Div([
                        html.Div([
                            html.H4('Number of Runways', style={'font-weight':'normal'}),
                            html.H3(id='land_use')
                        ],className='box_emissions', style={'margin-left':'10px'}),

                        html.Div([
                            html.H4('Number of Terminals', style={'font-weight':'normal'}),
                            html.H3(id='animal_feed')
                        ],className='box_emissions', style={'margin-left':'10px'}),
                    
                        html.Div([
                            html.H4('Total Passengers', style={'font-weight':'normal'}),
                            html.H3(id='farm')
                        ],className='box_emissions', style={'margin-left':'10px'}),

                        html.Div([
                            html.H4('Most Popular Route', style={'font-weight':'normal'}),
                            html.H3(25)
                        ],className='box_emissions',style={'margin-left':'10px'}),
                    
                        html.Div([
                            html.H4('2nd Most Popular Route', style={'font-weight':'normal'}),
                            html.H3(id='retail')
                        ],className='box_emissions', style={'margin-left':'10px'}),
                    ], style={'display': 'flex'}),

            ], className='box', style={'heigth':'10%','margin-left':'200px'}),
                
                html.Div([
                    html.H1('Hello World',style={'color': 'black', 'fontSize': '40px','padding-top':'25px'}),
                    dcc.Graph(
                        id='lax',
                        figure = fig
                    ),
                ], className='box_emissions',style={'margin-left':'600px','padding-bottom':'15px'}),
                ]),
        ]),

        html.Div([
            html.Div([
                html.P(['DSO 545 Group:', 
                html.Br(),'Matthew Lee, Vivian Kong, Sadman Rahi, Matthew Schneider, Edwin Wu'], style={'font-size':'12px'}),
                ], style={'width':'60%'}), 
            html.Div([
                html.P(['Sources ', html.Br(), html.A('Bureau of Transportation Statistics', href='https://www.bts.gov/content/passengers-boarded-top-50-us-airports', target='_blank'), ', ', html.A('Food and Agriculture Organization of the United Nations', href='http://www.fao.org/faostat/en/#data', target='_blank')], style={'font-size':'12px'})
                ], style={'width':'37%'}),
            ], className = 'footer', style={'display':'flex'}),
    
    ]),
])


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
 ###################################    GLOBE    ##############################################   
  
airport="JFK"

### For LAX
if airport == "LAX":
    LAX_Dest_Names = ['London', 'Paris', 'Mexico City']
    LAX_Dest_coor = np.array([[52.5500,0.1276], [48.8566, 2.3522],[19.432608,-99.133209]] )
    LAX_df = pd.DataFrame(LAX_Dest_coor, index=LAX_Dest_Names, columns=[['lat', 'lon']])
    Dest = LAX_Dest_Names
    df = LAX_df
    base = [33.942791, -118.410042]

### For JFK
elif airport == "JFK":
    JFK_Dest_Names = ['London', 'Paris', 'Mexico City']
    JFK_Dest_coor = np.array([[52.5500,0.1276], [48.8566, 2.3522],[19.432608,-99.133209]] )
    JFK_df = pd.DataFrame(JFK_Dest_coor, index=JFK_Dest_Names, columns=[['lat', 'lon']])
    Dest = JFK_Dest_Names
    df = JFK_df
    base = [40.6409, -73.7717]

### For ORD
elif airport == "ORD":
    ORD_Dest_Names = ['London', 'Toronto', 'Los Angeles']
    ORD_Dest_coor = np.array([[52.5500,0.1276], [43.67956, -79.62430],[33.942791, -118.410042]] )
    ORD_df = pd.DataFrame(ORD_Dest_coor, index=ORD_Dest_Names, columns=[['lat', 'lon']])
    Dest = ORD_Dest_Names
    df = ORD_df
    base = [41.9801, -87.9055]
    
### For ATL
elif airport == "ATL":
    ATL_Dest_Names = ['Fort Lauderdale', 'Orlando', 'Paris']
    ATL_Dest_coor = np.array([[26.0754, -80.1511], [28.4194, -81.3008],[49.0064, 2.5792]] )
    ATL_df = pd.DataFrame(ATL_Dest_coor, index=ATL_Dest_Names, columns=[['lat', 'lon']])
    Dest = ATL_Dest_Names
    df = ATL_df
    base = [33.64183, -84.4288]
    
### For DFW
elif airport == "DFW":
    DFW_Dest_Names = ['Los Angeles', 'Cancun', 'London']
    DFW_Dest_coor = np.array([[32.9023, -97.0422], [21.04169, -86.8678],[51.4721, -0.4429]] )
    DFW_df = pd.DataFrame(DFW_Dest_coor, index=DFW_Dest_Names, columns=[['lat', 'lon']])
    Dest = DFW_Dest_Names
    df = DFW_df
    base = [32.9023, -97.0422]

fig = go.Figure()

############################ MARKER
for i in Dest:
    fig.add_trace(go.Scattergeo(
        lon = [base[1], df.loc[i][1]],
        lat = [base[0], df.loc[i][0]],
        hoverinfo = 'text',
        text = i,
        mode = 'markers',
        marker = dict(
            size = 10,
            color = 'rgb(255, 0, 0)',
            line = dict(
                width = 3,
                color = 'rgba(68, 68, 68, 0)'
            )
        )))

fig.add_trace(go.Scattergeo(
    lon = [base[1], base[1]],
    lat = [base[0], base[0]],
    hoverinfo = 'text',
    text = airport,
    mode = 'markers',
    marker = dict(
        size = 10,
        color = 'rgb(255, 0, 0)',
        line = dict(
            width = 3,
            color = 'rgba(68, 68, 68, 0)'
        )
    )))

############################ LINE

route_colors = ['rgb(0,0,128)', 'rgb(255,128,0)', 'rgb(167,20,220)']

for i,c in zip(Dest, route_colors):
    fig.add_trace(go.Scattergeo(
        lon = [base[1], df.loc[i][1]],
        lat = [base[0], df.loc[i][0]],
        hoverinfo = 'text',
        mode = 'lines',
        marker = dict(
            size = 5,
            color = c,
            line = dict(
                width = 3,
                color = c
            )
        )))



fig.update_layout(
    title_text = 'Three highest traffic routes',
    showlegend = False,
    geo = dict(
        showland = True,
        showcountries = True,
        showocean = True,
        countrywidth = 0.5,
        landcolor = 'rgb(102, 204, 0)',
        lakecolor = 'rgb(137, 207, 240)',
        oceancolor = 'rgb(137, 207, 240)',
        projection = dict(
            type = 'orthographic',
            rotation = dict(
                lon = -100,
                lat = 40,
                roll = 0
            )
        ),
        lonaxis = dict(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        ),
        lataxis = dict(
            showgrid = True,
            gridcolor = 'rgb(102, 102, 102)',
            gridwidth = 0.5
        )
    )
)