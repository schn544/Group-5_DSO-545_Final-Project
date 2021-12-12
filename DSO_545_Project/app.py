import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

import plotly.express as px
import plotly.graph_objects as go
import numpy as np # for mathematical caluclations
import pandas as pd 
import datetime  # to access datetime
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px # for interactive plotting
import plotly.graph_objects as go # for interactive plotting
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_table

tsa = pd.read_csv('TSA Daily Data.csv', parse_dates=['Date'], index_col= 'Date')
covidWeek = pd.read_csv('CovidCasesPerWeek.csv', parse_dates=['State'], index_col= 'State')
covidWeek_start = pd.to_datetime('02/02/20')
covidWeek_end = pd.to_datetime('11/4/21') 
covidWeek = covidWeek[covidWeek_start:covidWeek_end]
tsaALL_start = pd.to_datetime('2019-1-1')
tsaALL_end = pd.to_datetime('2021-12-31') 
tsaALL = tsa[tsaALL_start:tsaALL_end]
airfare = pd.read_csv('Q airfare.csv', parse_dates=['Date'], index_col= 'Date')
airfare_start = pd.to_datetime('1/1/19')
airfare_end = pd.to_datetime('4/1/2021') 
airfare = airfare[airfare_start:airfare_end]
employment = pd.read_csv('Airline Employment.csv', parse_dates=['Year'], index_col= 'Year')
employment_start = pd.to_datetime('2019-01-01')
employment_end= pd.to_datetime('2021-10-01') 
employment=employment[employment_start:employment_end]
box_data = pd.read_csv('airport_boxes_data.csv',index_col=0)
df = pd.read_csv('tsa_daily_passengers.csv')

radio_airport = dbc.RadioItems(
        id='airport', 
        className='box_comment',
        options=[dict(label='COVID-19 Airport Data', value=0)],
        value=0, 
        inline=True,
        style= {'font-size': '30pt', 'font-weight':'bold'}
    )

fig_table = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>STATE</b>','<b>AVERAGE AIRFARE</b>','<b>AVERAGE WEEKLY COVID CASE(S)<b>'],
    line_color='darkslategray',
    fill_color='black',
    align=['left','center'],
    font=dict(color='white', size=20)
  ),
  cells=dict(
    values=[
      ['California','Illinois','Georgia','New York','Texas'],
      [283.94, 313.15, 411.38, 304.93,264.45],
      [2160000, 798000, 555555,1170000, 1760000]],
    line_color='darkslategray',
    # 2-D list of colors for alternating rows
    fill_color = [['white','white','white', 'white','white']*5],
    align = ['left', 'center'],
    font = dict(color = 'darkslategray', size = 14),
    ))
])


#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([
        html.H1(children='AIR TRAVEL COVID-19 DATA'),
        html.Label('', 
                    style={'color':'rgb(33 36 35)'}), 
        html.Img(src=app.get_asset_url('covid.png'), style={'position': 'relative', 'width': '80%', 'left': '5%', 'top': '12%'}),
    ], className='side_bar'),

    html.Div([
        html.Div([
            html.Div([
                html.Br(),
                html.Br(),
                radio_airport
            ], className='box', style={'margin': '1%', 'padding-top':'1%', 'padding-bottom':'1%'}),

            html.Div([
                html.Div([
                    html.H1('Select an Airport',style={'font-size':'30px', 'color':'black'}),
                    dbc.RadioItems(
                    id='ani_veg', 
                    className='radio',
                    options=[dict(label='LAX', value='LAX'), dict(label='JFK', value='JFK'), dict(label='ATL', value='ATL'), dict(label='ORD', value='ORD'), dict(label='DFW', value='DFW')],
                    value="LAX", 
                    inline=True,
                    labelStyle= {'display':'inline-block'}
                ),
                ], className='box'),
            ]),
            html.Div([
                html.Div([
                dcc.Graph(
                    id = 'globe',
                )
                ]),
            html.Div([
                            html.Label('Airport Data At A Glance', style={'font-size':'20px', 'color':'black'}),
                            html.Br(),
                            html.Br(),
                            html.Div([
                                html.Div([
                                    html.H4('Number of Runways', style={'font-weight':'normal'}),
                                    html.H3(id='runways')
                                ],className='box_emissions'),

                                html.Div([
                                    html.H4('Number of Terminals', style={'font-weight':'normal'}),
                                    html.H3(id='terminals')
                                ],className='box_emissions'),
                            
                                html.Div([
                                    html.H4('Total Passengers (2019)', style={'font-weight':'normal'}),
                                    html.H3(id='passengers1')
                                ],className='box_emissions'),

                                html.Div([
                                    html.H4('Total Passengers (2020)', style={'font-weight':'normal'}),
                                    html.H3(id='passengers2')
                                ],className='box_emissions'),
                            
                                html.Div([
                                    html.H4('Most Popular Route', style={'font-weight':'normal'}),
                                    html.H3(id='popular1')
                                ],className='box_emissions'),

                                html.Div([
                                    html.H4('2nd Most Popular Route', style={'font-weight':'normal'}),
                                    html.H3(id='popular2')
                                ],className='box_emissions'),
                            
                                html.Div([
                                    html.H4('3rd Most Popular Route', style={'font-weight':'normal'}),
                                    html.H3(id='popular3')
                                ],className='box_emissions'),
                            ], style={'display': 'flex'}),

                        ], className='box', style={'heigth':'10%'}),
            ]),
            ]),
            html.Div([
                html.Div([
                    html.H1('Select a Graph',style={'font-size':'20px', 'color':'black','padding-bottom':'2%'}),
                    dbc.RadioItems(
                    id='sel_graph', 
                    className='radio',
                    options=[dict(label='COVID-19 cases over time', value=0), dict(label='TSA volume changes', value=1), dict(label='Airfare changes', value=2), dict(label='Airline Employment changes', value=3)],
                    value=0,  
                    inline=True,
                    labelStyle= {'display':'inline'}
                ),
                ], className='box'),
            ]),
            html.Div([
                html.Div([
                dcc.Graph(
                    id = 'VS_graphs',
                )
                ], className = 'box', style = {'width':'65%'}),
                html.Div([
                    html.Img(src=app.get_asset_url('flight.png'), className = 'box', style = {'width':'95%'}),
                ]),
            ], className = 'row'),

            html.Div([
                html.Div([
                    dbc.Label('Click a cell in the table:'),
                    dash_table.DataTable(
                        id='data_table',
                        columns=[{"name": i, "id": i} for i in df.columns],
                        data=df.to_dict('records'),
                        style_cell={'padding': '0.5%'},
                        style_header={
                            'backgroundColor': 'white',
                            'fontWeight': 'bold',
                            'font-size': '16pt'},
                        ),
                    html.Div(id='output_div')
                        ], className = 'box'),
                ]),
            # html.Div([
            #     html.Div([
            #         html.Br(),
            #         html.Br(), 
            #         html.Br(), 
            #         html.Img(src=app.get_asset_url('Capture.png'), className = 'box', style = {'width':'95%'}),
            #     ], className='box', style={'width': '63%'}), 
            #     html.Div([
            #         html.Br(),
            #         html.Label('', style={'font-size':'9px'}),
            #         html.Br(), 
            #         html.Br(), 
            #         html.Img(src=app.get_asset_url('employment.png'), className = 'box', style = {'width':'95%'}),
            #     ], className='box', style={'width': '63%'}), 
            #     html.Div([
            #         html.Br(),
            #         html.Label('', style={'font-size':'9px'}),
            #         html.Br(), 
            #         html.Br(), 
            #         html.Img(src=app.get_asset_url('airfare.png'), className = 'box', style = {'width':'95%'}),
            #     ], className='box', style={'width': '63%'}), 
            # ], className='row'),

            html.Div([
                html.Div([
                    html.Img(src=app.get_asset_url('boarding.png'), className = 'box', style = {'width':'93%'}),
                ]),
                html.Div([
                    html.Label("Statistics for 5 Major US Airports", style={'font-size': '40px', 'font-weight':'bold'}),
                    html.P('(LAX, JFK, ATL, ORD, DFW)', style={'font-size':'12px'}),
                    html.Label('', style={'font-size':'100px'}),
                    dcc.Graph(figure=fig_table)
                ], className='box', style={'font-size':'100px', 'width': '63%'}), 
            ], className='row'),

            

            ###############################################################################

            html.Div([
                html.Div([
                    html.P(['DSO 545 Project', html.Br(),'Matthew Lee, Vivian Kong, Sadman Rahi, Matthew Schneider, Edwin Wu'], style={'font-size':'12px'}),
                ], style={'width':'60%'}), 
            ], className = 'footer', style={'display':'flex'}),
        ], className='main'),
    ])

#------------------------------------------------------ Callbacks ------------------------------------------------------
@app.callback(
    Output('output_div', 'children'),
    Input('data_table', 'active_cell'),
    State('data_table', 'data')
)
def getActiveCell(active_cell, data):
    if active_cell:
        col = active_cell['column_id']
        row = active_cell['row']
        cellData = data[row][col]
        return html.P(f'row: {row}, col: {col}, value: {cellData}')


@app.callback(
    Output('globe', 'figure'),
    Input('ani_veg', 'value'))
    
def Globe(airport="LAX"):

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
        DFW_Dest_coor = np.array([[32.9023, -97.0422], [21.04169, -86.8678], [51.4721, -0.4429]] )
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
            color = 'rgb(25.5, 41.2, 100)',
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
        title_text = '(Drag to rotate Globe)',
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

    return fig

@app.callback([
        Output('runways', 'children'),
        Output('terminals', 'children'),
        Output('passengers1', 'children'),
        Output('passengers2', 'children'),
        Output('popular1', 'children'),
        Output('popular2', 'children'),
        Output('popular3', 'children')],
        Input('ani_veg', 'value'))

def data(x='LAX'):
    runways = box_data.loc[x][0]
    terminals = box_data.loc[x][1]
    passen_19 = box_data.loc[x][2]
    passen_20 = box_data.loc[x][3]
    top1 = box_data.loc[x][4]
    top2 = box_data.loc[x][5]
    top3 = box_data.loc[x][6]
    
    return runways,terminals, passen_19, passen_20, top1, top2, top3


@app.callback(
    Output('VS_graphs', 'figure'),
    Input('sel_graph', 'value'))

def VS_graphs(graph):

    ############ COVID Cases ##############
    if graph == 0:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.update_layout(
            title=dict(text='Weekly Covid Case Count February 2020 - November 2021'),font=dict(size = 14))
        fig.update_layout(paper_bgcolor="white", height =700 , width= 1000)
        fig.update_layout(plot_bgcolor='white')
        fig.add_trace(
            go.Scatter(x=covidWeek.index, y=covidWeek.USA, name="Weekly Covid Cases"),
            secondary_y=False,)
        fig.update_xaxes(title_text="Timeline", color = 'black')
        fig.update_yaxes(title_text="Weekly Case Count", secondary_y=False, color = 'blue')


    ############# TSA vs. COVID ###########
    elif graph == 1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.update_layout(
            title=dict(text='TSA Passenger Throughput Vs Weekly Covid Cases January 2019-November 2021'),font=dict(size = 14))
        fig.update_layout(paper_bgcolor="white")
        fig.update_layout(plot_bgcolor='white')
        fig.add_trace(
            go.Scatter(x=tsaALL.index, y=tsaALL.Count, name="TSA Daily Throughput"),
            secondary_y=False,)
        fig.add_trace(
            go.Scatter(x=covidWeek.index, y=covidWeek.USA, name="Weekly Covid Cases"),
            secondary_y=True,)
        fig.update_xaxes(title_text="Timeline")
        fig.update_yaxes(title_text="Passenger Flow", secondary_y=False, color= 'blue')
        fig.update_yaxes(title_text="Weekly Case Count", secondary_y=True, color = 'red')
    


    ########### Aifare vs. COVID ############
    elif graph == 2:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.update_layout(
            title=dict(text='U.S. Average Airfare Price 2018-2021 vs. Weekly Case Count'),font=dict(size = 14))
        fig.update_layout(paper_bgcolor="white")
        fig.update_layout(plot_bgcolor='white')
        fig.add_trace(
            go.Scatter(x=airfare.index, y=airfare['U.S. Average (Current $) '], name="Airfare"),
            secondary_y=False,)
        fig.add_trace(
            go.Scatter(x=covidWeek.index, y=covidWeek.USA, name="Weekly Covid Cases"),
            secondary_y=True,)
        fig.update_xaxes(title_text="Timeline", color = 'black')
        fig.update_yaxes(title_text="Weekly Case Count", secondary_y=True, color = 'red')
        fig.update_yaxes(title_text="U.S. Average Airfare Price (Current $) ", secondary_y=False, color= 'blue')
    


   ############ Employment vs. COVID ##########
    else:
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.update_layout(
            title=dict(text='Airline Employment vs. Weekly Covid Case Count January 2019 - November 2021'),font=dict(size = 14))
        fig.update_layout(paper_bgcolor="white", height =700 , width= 1000)
        fig.update_layout(plot_bgcolor='white')
        fig.add_trace(
            go.Scatter(x=employment.index, y=employment['Full-Time'], name='Airline Employment Full-Time'),
            secondary_y=False,)
        fig.add_trace(
            go.Scatter(x=covidWeek.index, y=covidWeek.USA, name="Weekly Covid Cases"),
            secondary_y=True,)
        fig.update_xaxes(title_text="Timeline", color = 'black')
        fig.update_yaxes(title_text="Weekly Case Count", secondary_y=True, color = 'red')
        fig.update_yaxes(title_text="Airline Employment Full-Time ", secondary_y=False, color= 'blue')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)