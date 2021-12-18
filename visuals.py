import Starter
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_daq as daq
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

premium = pd.read_csv("premium.csv")
price = pd.read_csv("price.csv")
change = pd.read_csv("sales.csv")
share = pd.read_csv("wallet.csv")

team = dbc.Row([dbc.NavbarBrand("Brought to you by the Claremont Team")], className="g-0 ms-auto flex-nowrap mt-3 mt-md-0", align="center")    

title = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [   dbc.Col(html.Img(src="https://d3hid44mqnfbhw.cloudfront.net/precisagms/wp-content/uploads/2020/08/Logo-Full-4.png", height="30px")),
                        dbc.Col(html.Img(src="https://www.cmc.edu/sites/default/files/about/identity-guidelines/Solo_Box_vFA.jpg", height="30px")),
                        dbc.Col(dbc.NavbarBrand("Customer Loyalty Scoreboard", className="ms-2", style={"fontWeight": "bold", "fontFamily": "Open Sans", "width": "125%"})),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
            dbc.Collapse(
                team,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="light",
    dark=False,
)


client = dbc.Card([
    html.Div("Client Number (Select or Type Client Number)", style={"color": "#ffffff"}),
    dcc.Dropdown(
        id='client dropdown',
        options=
            [{'label': i, 'value': i} for i in premium.client_id]
        ,
        value=[],
    )
], color="secondary", inverse=False)

dashboard = html.Div([dbc.Row([
        html.Center(client),
    ], align="center"),
    html.Center(html.Div(id='loyalty-gauge')),
    html.Center(html.Div(id='loyalty-led'))])

scores_1 = dbc.Card([
    html.Div([        
    dcc.Checklist(
    id = "price premium",
    options=[
        {'label': 'Price Premium', 'value': 'price premium'}
    ],
    value=[]
    )]),
    dcc.RangeSlider(
    id = 'price premium disabled',
    count = 0,
    min=0,
    max=10,
    tooltip={"placement": "bottom", "always_visible": True}
)
], color="secondary", outline=True, body = True)

scores_2 = dbc.Card([
    html.Div([   
    dcc.Checklist(
    id = "sales growth",
    options=[
        {'label': 'Year-on-Year Sales Growth', 'value': 'year on year growth'}
    ],
    value=[]
    )]),
    dcc.RangeSlider(
    id = "year on year growth disabled",
    count = 0,
    min=0,
    max=10,
    tooltip={"placement": "bottom", "always_visible": True}
)
], color="secondary", outline=True, body = True)

scores_3 = dbc.Card([
    html.Div([   
    dcc.Checklist(
    id = "wallet share",
    options=[
        {'label': 'Wallet Share', 'value': 'wallet share'}
    ],
    value=[]
    )]),
    dcc.RangeSlider(
    id = "wallet share disabled",
    count = 0,
    min=0,
    max=10,
    tooltip={"placement": "bottom", "always_visible": True}
)
], color="secondary", outline=True, body = True)

graph_1 = dbc.Card([
    html.Center(html.Div(id='Price Premium Percentile')),
    dcc.Graph(id='Price Premium')
], color='secondary', inverse=True)

graph_2 = dbc.Card([
    html.Center(html.Div(id='Year on Year Sales Growth Percentile')),
    dcc.Graph(id='Year on Year Sales Growth')
], color='secondary', inverse=True)

graph_3 = dbc.Card([
    html.Center(html.Div(id='Wallet Share Percentile')),
    dcc.Graph(id='Wallet Share')
], color='secondary', inverse=True)


premium_combo = html.Div([html.Center(scores_1),
                          html.Center(graph_1)],
                          )

growth_combo = html.Div([html.Center(scores_2),
                         html.Center(graph_2)])

share_combo = html.Div([html.Center(scores_3),
                        html.Center(graph_3)])



app.layout = dbc.Container([
    # Row: Title
    html.Center(title),
    html.Hr(),
    

    html.Hr(),
    # Row: Filter + References
    # row: checklist
    
    html.Hr(),
    dbc.Row(html.Center([dbc.Col(dashboard, md=4)]), align="center"),
    html.Hr(),
    html.Hr(),
    dbc.Row([
            dbc.Col(premium_combo, md=4), 
            dbc.Col(growth_combo, md=4),
            dbc.Col(share_combo, md=4)],
            align="center"),

    # dash_table.DataTable(
    #     id='table',
    #     columns=[{"name": i, "id": i} for i in df_selected.columns],
    #     data=df_selected.to_dict('records'),
    # ),
    dbc.Row([dbc.Col([html.Center(html.Div(id='breakdown'))], md=4), 
            dbc.Col([html.Center(dcc.Graph(id='trend'))], md=4),
            dbc.Col([html.Center(dcc.Graph(id='share percent'))], md=4)], align="center"),
    html.Div(id="client selected"),
    html.Div(id="selection output"),
    html.Div(id="weights debugger")
], fluid = True, style={'background-image': 'url("https://miro.medium.com/max/1400/1*z04nmhhPKVTmlW3E1g9u5g.jpeg"), url("https://miro.medium.com/max/1400/1*CDBU43VD7zqqjPQGk3Cn2w.jpeg")',
'background-repeat': 'no-repeat, repeat', 'background-size': 'contain, contain'})

@app.callback(
    Output("selection output", "children"),
    Output("weights debugger", "children"),
    Output("price premium disabled", "disabled"),
    Output("year on year growth disabled", "disabled"),
    Output("wallet share disabled", "disabled"),
    Input("price premium", "value"),
    Input("sales growth", "value"),
    Input("wallet share", "value"))
def update_children(premium, growth, share):
    return 'This project is created by the Claremont Team for AgVend under the supervision of Professor Batta and Professor Dass through the Financial Economics Institute', '12/02/2021', (not('price premium' in premium)), (not('year on year growth' in growth)), (not('wallet share' in share))

@app.callback(Output('client selected', 'children'),
              Input('client dropdown', 'value'))
def update_children(dropdown):
    return 'Development Tools: Numpy, Pandas, R, Plotly Express, Dash'

@app.callback(Output('Price Premium', 'figure'),
             Output('Price Premium Percentile', 'children'),
            #  Output('premium figure', 'value'),
             Input("client dropdown", "value"))
def update_graph(this_client):
    if (this_client == []):
        client = 3993
    else:
        client = this_client
    data = premium.percentile
    thisVal = premium[premium.client_id == client].percentile.values[0]
    pct = premium[premium.client_id == client].percentile.values[0]
    fig = px.histogram(data, nbins=30, range_x=[0,5])
    fig.add_vline(x=thisVal, line_dash = 'dash', line_color = 'firebrick')
    fig.update_layout(showlegend=False)
    return fig, "Beats {} percent of clients".format(int(pct*100))

@app.callback(Output('Year on Year Sales Growth', 'figure'),
              Output('Year on Year Sales Growth Percentile', 'children'),
             Input("client dropdown", "value"))
def update_graph(this_client):
    if (this_client == []):
        client = 3993
    else:
        client = this_client
    data = change[change.aggChange < 10]
    data = data[data.aggChange > 0].aggChange
    thisVal = change[change.client_id == client].aggChange.values[0]
    pct = change[change.client_id == client].percentile.values[0]
    fig = px.histogram(data, nbins=30, range_x=[0,10])
    fig.add_vline(x=thisVal, line_dash = 'dash', line_color = 'firebrick')
    fig.update_layout(showlegend=False)
    return fig, "Beats {} percent of clients".format(int(pct*100))

@app.callback(Output('Wallet Share', 'figure'),
              Output('Wallet Share Percentile', 'children'),
             Input("client dropdown", "value"))
def update_graph(this_client):
    if (this_client == []):
        client = 3993
    else:
        client = this_client
    data = share.wallet_share
    thisVal = share[share.client_id == client].wallet_share.values[0]
    pct = share[share.client_id == client].percentile.values[0]
    fig = px.histogram(data, nbins=30, range_x=[0,1])
    fig.add_vline(x=thisVal, line_dash = 'dash', line_color = 'firebrick')
    fig.update_layout(showlegend=False)
    return fig, "Beats {} percent of clients".format(int(pct*100))

@app.callback(Output('loyalty-led', 'children'),
            Output('loyalty-gauge', 'children'),
            Input('price premium disabled', 'value'),
            Input('year on year growth disabled', 'value'),
            Input('wallet share disabled', 'value'),
            Input('client dropdown', 'value'))
def update_score(premium_weight, growth_weight, share_weight, id):
    if ((premium_weight == None) and (growth_weight == None) and (share_weight == None)):
        return html.Div(html.Center(daq.LEDDisplay(
        label="Loyalty Score",
        color="#ffffff",
        value="0.00",
        backgroundColor="#858481",
        size=30,
    ))), daq.Gauge(
    color={"gradient":True,"ranges":{"#ffffff":[0,4],"#92e0d3":[4,6],"#34abeb":[6,10]}},
    size=260,
    value=0,
    max=10,
    min=0,
)
    
    else:
        if (premium_weight == None):
            pw = 0
        else: 
            pw = premium_weight[0]
        if (growth_weight == None):
            gw = 0
        else:
            gw = growth_weight[0]
        if (share_weight == None):
            sw = 0
        else:
            sw = share_weight[0]
        total = pw + gw + sw
        ppct = premium[premium.client_id == id].percentile.values[0] * 10
        tpct = change[change.client_id == id].percentile.values[0] * 10
        spct = share[share.client_id == id].percentile.values[0] * 10
        score = round(pw/total*ppct + gw/total*tpct + sw/total*spct, 2)
        if (score == None):
            return html.Div(html.Center(daq.LEDDisplay(
        label="Loyalty Score",
        color="#ffffff",
        value="0.00",
        backgroundColor="#858481",
        size=30,
    ))), daq.Gauge(
    color={"gradient":True,"ranges":{"#ffffff":[0,4],"#92e0d3":[4,6],"#34abeb":[6,10]}},
    size=260,
    value=0,
    max=10,
    min=0,
)
        else:
            return html.Div(html.Center(daq.LEDDisplay(
        label="Loyalty Score",
        color="#ffffff",
        value=score,
        backgroundColor="#858481",
        size=30,
    ))), daq.Gauge(
    color={"gradient":True,"ranges":{"#ffffff":[0,4],"#92e0d3":[4,6],"#34abeb":[6,10]}},
    size=260,
    value=score,
    max=10,
    min=0,
)

@app.callback(Output('breakdown', 'children'),
              Input('client dropdown', 'value'))
def update_table(this_client):
    if (this_client == []):
        client = 3993
    else:
        client = this_client

    rawData = price[price.client_id == client]
    rawData = rawData.drop(rawData.columns[0], axis = 1)
    return dt.DataTable(
        id='tbl', data=rawData.to_dict('records'),
        columns=[{"name": i, "id": i} for i in rawData.columns],
        style_table={'height': '450px', 'overflowY': 'auto', 'overflowX':'auto'}
    )

@app.callback(Output('trend', 'figure'),
              Input('client dropdown', 'value'))
def update_table(this_client):
    if (this_client == []):
        client = 3993
    else:
        client = this_client
    rawData = change[change.client_id == client]
    dataframe = pd.DataFrame(dict(
    x = [2016, 2017, 2018, 2019, 2020],
    y = [rawData.total_16.values[0],
    rawData.total_17.values[0],
    rawData.total_18.values[0],
    rawData.total_19.values[0],
    rawData.total_20.values[0]]
))
    return px.line(dataframe, x="x", y="y") 

@app.callback(Output('share percent', 'figure'),
             Input('client dropdown', 'value'))
def update_pie(this_client):
    if (this_client == []):
        client = 3993
    else:
        client = this_client
    rawData = int(share[share.client_id == client].wallet_share * 100)
    labels = ['Wallet Share','Rest']
    values = [rawData, 100 - rawData, 1053, 500]
    return go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])


if __name__ == '__main__':
    app.run_server(debug=False)