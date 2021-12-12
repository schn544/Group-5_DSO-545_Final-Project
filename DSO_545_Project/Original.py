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

emissions = pd.read_csv("emissions_with_origin.csv")
productions = pd.read_csv("productions.csv")
water = pd.read_csv("water_use.csv")
global_emissions = pd.read_csv("Global_Emissions.csv")

top10 = emissions.sort_values("Total_emissions")[-10:]
top10_vegetal = emissions[emissions.Origin=='Vegetal'].sort_values("Total_emissions")[-10:]
top8_animal = emissions[emissions.Origin=='Animal'].sort_values("Total_emissions")[-5:]



radio_airport = dbc.RadioItems(
        id='airport', 
        className='box_comment',
        options=[dict(label='COVID-19 Airport Data', value=0)],
        value=0, 
        inline=True,
        style= {'font-size': '30pt', 'font-weight':'bold'}
    )

dict_ = {'Apples':'Apples', 'Bananas':'Bananas', 'Barley':'Barley', 'Beet Sugar':'Sugar beet', 'Berries & Grapes':'Berries & Grapes', 'Brassicas':'Brassicas', 
        'Cane Sugar':'Sugar cane', 'Cassava':'Cassava', 'Citrus Fruit':'Citrus', 'Coffee':'Coffee beans', 'Groundnuts':'Groundnuts','Maize':'Maize', 'Nuts':'Nuts', 
        'Oatmeal':'Oats', 'Olive Oil':'Olives', 'Onions & Leeks':'Onions & Leeks','Palm Oil':'Oil palm fruit', 'Peas':'Peas', 'Potatoes':'Potatoes', 'Rapeseed Oil':'Rapeseed',
        'Rice':'Rice', 'Root Vegetables':'Roots and tubers', 'Soymilk':'Soybeans', 'Sunflower Oil':'Sunflower seed', 'Tofu':'Soybeans','Tomatoes':'Tomatoes', 
        'Wheat & Rye':'Wheat & Rye', 'Dark Chocolate':'Cocoa, beans', 'Milk': 'Milk', 'Eggs': 'Eggs','Poultry Meat': 'Poultry Meat', 'Pig Meat': 'Pig Meat', 
        'Seafood (farmed)': 'Seafood (farmed)', 'Cheese': 'Cheese', 'Lamb & Mutton': 'Lamb & Mutton', 'Beef (beef herd)': 'Beef (beef herd)'}

options_veg = [dict(label=key, value=dict_[key]) for key in top10_vegetal['Airport'].tolist()[::-1] if key in dict_.keys()]
options_an = [dict(label=val, value=val) for val in top8_animal["Airport"].tolist()[::-1]]
options_total = [dict(label=key, value=dict_[key]) for key in top10['Airport'].tolist()[::-1] if key in dict_.keys()]

bar_colors = ['#ebb36a','#6dbf9c']
bar_options = [top8_animal, top10_vegetal, top10]

drop_map = dcc.Dropdown(
        id = 'drop_map',
        clearable=False,
        searchable=False, 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}        
    )

drop_continent = dcc.Dropdown(
        id = 'drop_continent',
        clearable=False, 
        searchable=False, 
        options=[{'label': 'World', 'value': 'world'},
                {'label': 'Europe', 'value': 'europe'},
                {'label': 'Asia', 'value': 'asia'},
                {'label': 'Africa', 'value': 'africa'},
                {'label': 'North america', 'value': 'north america'},
                {'label': 'South america', 'value': 'south america'}],
        value='world', 
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
    )

slider_map = daq.Slider(
        id = 'slider_map',
        handleLabel={"showCurrentValue": True,"label": "Year"},
        marks = {str(i):str(i) for i in [1990,1995,2000,2005,2010,2015]},
        min = 1990,
        size=450, 
        color='#4B9072'
    )

fig_table = go.Figure(data=[go.Table(
  header=dict(
    values=['<b>STATE</b>','<b>AVERAGE AIRFARE</b>','<b>AVERAGE WEEKLY COVID CASE(S)<b>'],
    line_color='darkslategray',
    fill_color='black',
    align=['left','center'],
    font=dict(color='white', size=14)
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
    font = dict(color = 'darkslategray', size = 12)
    ))
])

# fig_water = px.sunburst(water, path=['Origin', 'Category', 'Product'], values='Water Used', color='Category', 
#                         color_discrete_sequence = px.colors.sequential.haline_r).update_traces(hovertemplate = '%{label}<br>' + 'Water Used: %{value} L')

# fig_water = fig_water.update_layout({'margin' : dict(t=0, l=0, r=0, b=10),
#                         'paper_bgcolor': '#F9F9F8',
#                         'font_color':'#363535'
#                     })

fig_gemissions = px.sunburst(global_emissions, path = ['Emissions', 'Group','Subgroup'], values = 'Percentage of food emissions', 
                    color = 'Group', color_discrete_sequence = px.colors.sequential.Peach_r).update_traces(hovertemplate = '%{label}<br>' + 'Global Emissions: %{value}%', textinfo = "label + percent entry") 

fig_gemissions = fig_gemissions.update_layout({'margin' : dict(t=0, l=0, r=0, b=10),
                        'paper_bgcolor': '#F9F9F8',
                        'font_color':'#363535'})


#------------------------------------------------------ APP ------------------------------------------------------ 

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Div([
        html.H1(children='AIR TRAVEL COVID-19 DATA'),
        html.Label('', 
                    style={'color':'rgb(33 36 35)'}), 
        html.Img(src=app.get_asset_url('supply_chain.png'), style={'position': 'relative', 'width': '180%', 'left': '-83px', 'top': '-20px'}),
    ], className='side_bar'),

    html.Div([
        html.Div([
            html.Div([
                html.Br(),
                html.Br(),
                radio_airport
            ], className='box', style={'margin': '1%', 'padding-top':'1%', 'padding-bottom':'1%'}),

            html.Div([
                html.H1(children='Hello Dash'),

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
                            html.Label('Airport Data At A Glance', style={'font-size': 'medium'}),
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

            html.Div([
                html.Div([
                    html.Div([   
                        html.Label(id='title_bar'),           
                        dcc.Graph(id='bar_fig'), 
                        html.Div([              
                            html.P(id='comment')
                        ], className='box_comment'),
                    ], className='box', style={'padding-bottom':'15px'}),

                    html.Div([
                        html.Img(src=app.get_asset_url('Food.png'), style={'width': '100%', 'position':'relative', 'opacity':'80%'}),
                    ]),

                ], style={'width': '40%'}),


                html.Div([

                    html.Div([
                    html.Label(id='choose_product', style= {'margin': '10px'}),
                    drop_map,
                    ], className='box'),

                    html.Div([
                        html.Div([ 
                            html.Div([
                                
                                html.Div([
                                    html.Br(),
                                    html.Label(id='title_map', style={'font-size':'medium'}), 
                                    html.Br(),
                                    html.Label('Most Popular Destinations'),
                                ], style={'width': '70%'}),
                                html.Div([

                                ], style={'width': '5%'}),
                                html.Div([
                                    drop_continent, 
                                    html.Br(),
                                    html.Br(), 
                                ], style={'width': '25%'}),
                            ], className='row'),
                            
                            dcc.Graph(id='map', style={'position':'relative', 'top':'-50px'}), 

                            html.Div([
                                slider_map
                            ], style={'margin-left': '15%', 'position':'relative', 'top':'-38px'}),
                            
                        ], className='box', style={'padding-bottom': '0px'}), 
                    ]),
                ], style={'width': '60%'}),           
            ], className='row'),

            html.Div([
                html.Div([
                    html.Label("Global greenhouse gas emissions from food production, in percentage", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('Drag the columns around!', style={'font-size':'9px'}),
                    html.Br(), 
                    html.Br(), 
                    dcc.Graph(figure=fig_gemissions)
                ], className='box', style={'width': '40%'}), 
                html.Div([
                    html.Label("Freshwater withdrawals per kg of product, in Liters", style={'font-size': 'medium'}),
                    html.Br(),
                    html.Label('', style={'font-size':'9px'}),
                    html.Br(), 
                    html.Br(), 
                    dcc.Graph(figure=fig_table)
                ], className='box', style={'width': '63%'}), 
            ], className='row'),

            ###############################################################################

            html.Div([
                html.Div([
                    html.P(['DSO 545 Project', html.Br(),'Matthew Lee, Vivian Kong, Sadman Rahi, Matthew Schneider, Edwin Wu'], style={'font-size':'12px'}),
                ], style={'width':'60%'}), 
                html.Div([
                    html.P(['Sources ', html.Br(), html.A('Bureau of Transportation Statistics', href='https://www.bts.gov/content/passengers-boarded-top-50-us-airports', target='_blank'), ', ', html.A('Food and Agriculture Organization of the United Nations', href='http://www.fao.org/faostat/en/#data', target='_blank')], style={'font-size':'12px'})
                ], style={'width':'37%'}),
            ], className = 'footer', style={'display':'flex'}),
        ], className='main'),
    ]),
])

#------------------------------------------------------ Callbacks ------------------------------------------------------
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


##################################
@app.callback(
    [
        Output('title_bar', 'children'),
        Output('bar_fig', 'figure'),
        Output('comment', 'children'),
        Output('drop_map', 'options'),
        Output('drop_map', 'value'),
        Output('choose_product', 'children')
    ],
    [
        Input('airport', 'value')
    ], 
)
def bar_chart(top10_select):

    ################## Top10 Plot ##################
    title = '1. Greenhouse emissions (kg CO2 per kg of product)'
    df = bar_options[top10_select]

    if top10_select==2:
        bar_fig = dict(type='bar',
            x=df.Total_emissions,
            y=df["Airport"],
            orientation='h',
            marker_color=['#ebb36a' if x=='Animal' else '#6dbf9c' for x in df.Origin])
    else:
        bar_fig = dict(type='bar',
            x=df.Total_emissions,
            y=df["Airport"],
            orientation='h',
            marker_color=bar_colors[top10_select])

    ################## Dropdown Bar ##################
    if top10_select==0:
        options_return = options_an
        product_chosen = "Choose an Airport:" 
        comment = ["", html.Br(), html.Br()]
    elif top10_select==1:
        options_return = options_veg
        product_chosen = "Choose a vegetal product:" 
        comment = ["Did you know that dark chocolate and coffee are the vegetal-based products that emit more gases?", html.Br(), html.Br()]
    else:
        options_return = options_total
        product_chosen = "Choose an animal or vegetal product:" 
        comment = "Check the difference between animal and vegetal-based products! Beef (top1 animal-based emitter) produces around 3 times more emissions than dark chocolate (top1 plant-based emitter)."

    return title, \
            go.Figure(data=bar_fig, layout=dict(height = 300, font_color = '#363535', paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20), margin_pad=10)), \
            comment, \
            options_return, \
            options_return[0]['value'], \
            product_chosen



@app.callback(
    [ 
        Output('slider_map', 'max'),
        Output('slider_map', 'value'),
    ],
    [
        Input('drop_map', 'value')
    ]
)

def update_slider(product):
    year = productions[productions['Item']==product]['Year'].max()
    return year, year



@app.callback(
    [
        Output('runways', 'children'),
        Output('terminals', 'children'),
        Output('passengers1', 'children'),
        Output('passengers2', 'children'),
        Output('popular1', 'children'),
        Output('popular2', 'children'),
        Output('popular3', 'children'),
        Output('title_map', 'children'),
        Output('map', 'figure')
    ],
    [
        Input('ani_veg', 'value'),
        Input('slider_map', 'value'), 
        Input('drop_continent', 'value')
    ],
    [State("drop_map","options")]
)

def update_map(drop_map_value, year, continent, opt):

    ################## Emissions datset ##################
    
    the_label = [x['label'] for x in opt if x['value'] == drop_map_value]

    data_emissions = emissions[emissions["Airport"]==the_label[0]]
    runways_str = str(int(data_emissions["Land use change"].values[0]))
    terminals_str = str(int(data_emissions["Animal Feed"].values[0]))
    passengers1_str = str(int(data_emissions["Farm"].values[0]))
    passengers2_str = str(int(data_emissions["Processing"].values[0]))
    popular1_str = str(data_emissions["Transport"].values[0])
    popular2_str = str(data_emissions["Packging"].values[0])
    popular3_str = str(data_emissions["Retail"].values[0])

    ################## Choroplet Plot ##################
    
    prod1 = productions[(productions['Item']== drop_map_value) & (productions['Year']== year)]

    title = ' '  #font_color = '#363535',
    data_slider = []
    data_each_yr = dict(type='choropleth',
                        locations = prod1['Area'],
                        locationmode='country names',
                        autocolorscale = False,
                        z=np.log(prod1['Value'].astype(float)),
                        zmin=0, 
                        zmax = np.log(productions[productions['Item']== drop_map_value]['Value'].max()),
                        colorscale = ["#ffe2bd", "#006837"],   
                        marker_line_color= 'rgba(0,0,0,0)',
                        colorbar= {'title':'Tonnes (log)'},#Tonnes in logscale
                        colorbar_lenmode='fraction',
                        colorbar_len=0.8,
                        colorbar_x=1,
                        colorbar_xanchor='left',
                        colorbar_y=0.5,
                        name='')
    data_slider.append(data_each_yr)
 
    layout = dict(geo=dict(scope=continent,
                            projection={'type': 'natural earth'},
                            bgcolor= 'rgba(0,0,0,0)'),
                    margin=dict(l=0,
                                r=0,
                                b=0,
                                t=30,
                                pad=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)')
 
    fig_choropleth = go.Figure(data=data_slider, layout=layout)
    fig_choropleth.update_geos(showcoastlines=False, showsubunits=False,showframe=False)

    return runways_str, \
        terminals_str, \
        passengers1_str, \
        passengers2_str, \
        popular1_str, \
        popular2_str, \
        popular3_str, \
        title, \
        fig_choropleth


if __name__ == '__main__':
    app.run_server(debug=True)
