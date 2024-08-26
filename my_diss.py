import dash
from dash import html, dcc, callback, Output, Input, dash_table, State
import dash
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import datetime
import webbrowser
from threading import Timer
from datetime import datetime, timedelta
    
data = pd.read_csv('data_nifty.csv')
is_data = pd.read_csv('is_data_nifty.csv')
bs_data = pd.read_csv('bs_data_nifty.csv')
cf_data = pd.read_csv('cf_data_nifty.csv')
ratios = pd.read_csv('ratios_nifty.csv')
val_ratios = pd.read_csv('val_ratio.csv')
company_basic_data = pd.read_csv('nifty50.csv')

data['Datetime'] = pd.to_datetime(data['Datetime'], dayfirst=True)
val_ratios['Datetime'] = pd.to_datetime(val_ratios['Datetime'],dayfirst=True)
merged_df = pd.merge(val_ratios, data, on=['symbol', 'Datetime'], how='outer')
is_list = is_data['Particulars'].unique().tolist()
bs_list = bs_data['Particulars'].unique().tolist()
cf_list = cf_data['Particulars'].unique().tolist()
ratios_list = ratios['Particulars'].unique().tolist()

ratios_dict = {
    'Return on Assets %': 'ROA',
    'Return on Capital %': 'ROC',
    'Return on Equity %': 'ROE',
    'Return on Common Equity %': 'ROCE',
    'Margin Analysis': 'Margin Analysis',
    'Gross Margin %': 'Gross Margin',
    'SG&A Margin %': 'SG&A Margin',
    'EBITDA Margin %': 'EBITDA Margin',
    'EBITA Margin %': 'EBITA Margin',
    'EBIT Margin %': 'EBIT Margin',
    'Earnings from Cont. Ops Margin %': 'Earnings Margin',
    'Net Income Margin %': 'Net Income Margin',
    'Net Income Avail. for Common Margin %': 'Net Income Common Margin',
    'Normalized Net Income Margin %': 'Normalized Net Income Margin',
    'Levered Free Cash Flow Margin %': 'Levered FCF Margin',
    'Unlevered Free Cash Flow Margin %': 'Unlevered FCF Margin',
    'Asset Turnover': 'Asset Turnover',
    'Total Asset Turnover': 'Total Asset Turnover',
    'Fixed Asset Turnover': 'Fixed Asset Turnover',
    'Accounts Receivable Turnover': 'A/R Turnover',
    'Inventory Turnover': 'Inventory Turnover',
    'Short Term Liquidity': 'Short Term Liquidity',
    'Current Ratio': 'Current Ratio',
    'Quick Ratio': 'Quick Ratio',
    'Cash from Ops. to Curr. Liab.': 'Cash/Current Liab.',
    'Avg. Days Sales Out.': 'Avg. Days Sales Out.',
    'Avg. Days Inventory Out.': 'Avg. Days Inventory Out.',
    'Avg. Days Payable Out.': 'Avg. Days Payable Out.',
    'Avg. Cash Conversion Cycle': 'Avg. Cash Conversion',
    'Long Term Solvency': 'Long Term Solvency',
    'Total Debt/Equity': 'Debt/Equity',
    'Total Debt/Capital': 'Debt/Capital',
    'LT Debt/Equity': 'LT Debt/Equity',
    'LT Debt/Capital': 'LT Debt/Capital',
    'Total Liabilities/Total Assets': 'Liabilities/Assets',
    'EBIT / Interest Exp.': 'EBIT/Interest Exp.',
    'EBITDA / Interest Exp.': 'EBITDA/Interest Exp.',
    '(EBITDA-CAPEX) / Interest Exp.': 'EBITDA-CAPEX/Interest Exp.',
    'Total Debt/EBITDA': 'Debt/EBITDA',
    'Net Debt/EBITDA': 'Net Debt/EBITDA',
    'Total Debt/(EBITDA-CAPEX)': 'Debt/EBITDA-CAPEX',
    'Net Debt/(EBITDA-CAPEX)': 'Net Debt/EBITDA-CAPEX',
    'Altman Z Score': 'Altman Z Score'}

checklist_options = [{'label': full, 'value': short} for short, full in ratios_dict.items()]

val_ratios_columns = val_ratios.columns.tolist()
filter_list = val_ratios_columns

symbols = is_data['Company Symbol'].unique().tolist()

# Tab 2 - Competitor Analysis
competitor_analysis_tab = dbc.Tab(
    label='Filter using Multiples',
    tab_id='tab-2',
    children=[
        dbc.Row([
            dbc.Col([
                # First Table for Criteria Selection
                dbc.Table([
                    html.Thead(html.Tr([html.Th("Criteria"), html.Th("Min Value"), html.Th("Max Value")])),
                    html.Tbody([
                        html.Tr([
                            html.Td(
                                dcc.Dropdown(
                                    id='criteria-dropdown-1',
                                    options=[{'label': item, 'value': item} for item in filter_list],
                                    placeholder="Select Criteria"
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='min-value-input-1',
                                    type='number',
                                    placeholder='Min Value'
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='max-value-input-1',
                                    type='number',
                                    placeholder='Max Value'
                                )
                            )
                        ]),
                        html.Tr([
                            html.Td(
                                dcc.Dropdown(
                                    id='criteria-dropdown-2',
                                    options=[{'label': item, 'value': item} for item in filter_list],
                                    placeholder="Select Criteria"
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='min-value-input-2',
                                    type='number',
                                    placeholder='Min Value'
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='max-value-input-2',
                                    type='number',
                                    placeholder='Max Value'
                                )
                            )
                        ]),
                        
                        html.Tr([
                            html.Td(
                                dcc.Dropdown(
                                    id='criteria-dropdown-3',
                                    options=[{'label': item, 'value': item} for item in filter_list],
                                    placeholder="Select Criteria"
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='min-value-input-3',
                                    type='number',
                                    placeholder='Min Value'
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='max-value-input-3',
                                    type='number',
                                    placeholder='Max Value'
                                )
                            )
                        ]),
                        
                        html.Tr([
                            html.Td(
                                dcc.Dropdown(
                                    id='criteria-dropdown-4',
                                    options=[{'label': item, 'value': item} for item in filter_list],
                                    placeholder="Select Criteria"
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='min-value-input-4',
                                    type='number',
                                    placeholder='Min Value'
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='max-value-input-4',
                                    type='number',
                                    placeholder='Max Value'
                                )
                            )
                        ]),
                        
                        html.Tr([
                            html.Td(
                                dcc.Dropdown(
                                    id='criteria-dropdown-5',
                                    options=[{'label': item, 'value': item} for item in filter_list],
                                    placeholder="Select Criteria"
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='min-value-input-5',
                                    type='number',
                                    placeholder='Min Value'
                                )
                            ),
                            html.Td(
                                dcc.Input(
                                    id='max-value-input-5',
                                    type='number',
                                    placeholder='Max Value'
                                )
                            )
                        ]),
                        # Add more rows for additional criteria as needed
                    ])
                ], bordered=True, dark=False, hover=True, responsive=True, striped=True),

                # Second Table for displaying Symbol and Close
                html.Div(id='dynamic-table-container')
            ], width={'size': 10, 'offset': 1})
        ])
    ]
)

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import plotly.express as px
from datetime import datetime, timedelta

app = dash.Dash(
    external_stylesheets=[dbc.themes.MINTY]
)

server=app.server
# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Stock Market Dashboard", className='text-center text-primary mb-4 mt-4' ),
                width=12)
    ], justify='center', align='middle'),

    dbc.Tabs([
        dbc.Tab(label='Company Analysis', tab_id='tab-1', children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card(
    dbc.Row(
        dbc.Col(
            [
                html.Div(
                    dcc.Dropdown(
                        options=symbols,
                        value='RELIANCE',
                        id='select_company',
                        style={
                            'background-color': '#007bff',  # Bootstrap's primary blue
                            'color': 'black',
                            'border': 'none',
                            'border-radius': '5px',
                            'padding': '5px',
                            'font-weight': 'bold',
                            'width': '100%',
                            'text-align': 'center',
                        },
                        placeholder='Search for company',
                        className='dropdown-highlight'
                    ),
                    style={
                        'background-color': '#007bff',  # Match background of dropdown
                        'padding': '5px',
                        'border-radius': '5px',
                        'display': 'flex',
                        'align-items': 'center',
                        'justify-content': 'center',
                        'width': '100%'
                    }
                ),
                html.H5(
                    id="latest_close_price", 
                    className="sub-title", 
                    style={
                        'color': 'black',
                        'font-weight': 'bold',
                        'margin-top': '10px'
                    }
                ),
                html.P(
                    id="close_price_date", 
                    className='text-muted', 
                    style={
                        'color': 'black'
                    }
                )
            ],
            width=12,
            className="d-flex flex-column align-items-center justify-content-center"
        )
    ),
    style={
        'border': '2px solid #007bff',  
        'border-radius': '10px',
        'padding': '15px',
        'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'
    }
)

                ], width={'size': 2, 'offset': 1}),
                
            dbc.Col([
                dbc.Card(
    dbc.Row(
        dbc.Col(
            [
                html.Div(
                    html.H4(
                        id="company_name",
                        style={
                            'background-color': '#007bff',  # Bootstrap's primary blue
                            'color': 'white',  # White text
                            'border-radius': '5px',
                            'padding': '10px',
                            'text-align': 'center',
                            'margin-bottom': '10px',
                            'font-weight': 'bold',
                        }
                    ),
                    style={
                        'background-color': '#007bff',  # Match background of title
                        'padding': '5px',
                        'border-radius': '5px',
                        'display': 'flex',
                        'align-items': 'center',
                        'justify-content': 'center',
                        'width': '100%'
                    }
                ),
                html.H6(
                    id="industry",
                    className="card-subtitle mb-2 text-muted",
                    style={
                        'color': 'black',
                        'text-align': 'center',
                        'margin-top': '10px'
                    }
                ),
                html.P(
                    id="isin_code",
                    className="card-text",
                    style={
                        'color': 'black',
                        'text-align': 'center'
                    }
                )
            ],
            width=12,
            className="d-flex flex-column align-items-center justify-content-center"
        )
    ),
    style={
        'border': '2px solid #007bff',  # Add border with the same blue color
        'border-radius': '10px',
        'padding': '15px',
        'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'  # Subtle shadow for depth
    }
)
            ], width={'size': 3, 'offset': 4})
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(options=['P/E', 'Close', 'Div_Yield'], value='Close', id='graph_metric', style={'width': '50%'}),
                ], width={'size': 5, 'offset': 1}),

                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("1m", id="n1m", outline=True, color="primary"),
                        dbc.Button("3m", id="n3m", outline=True, color="primary"),
                        dbc.Button("6m", id="n6m", outline=True, color="primary"),
                        dbc.Button("1Y", id="n1Y", outline=True, color="primary"),
                        dbc.Button("3Y", id="n3Y", outline=True, color="primary"),
                        dbc.Button("5Y", id="n5Y", outline=True, color="primary"),
                        dbc.Button("10Y", id="n10Y", outline=True, color="primary", n_clicks=1),
                    ], size="sm"),
                ], width={'size': 4, 'offset': 2})
            ]),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure={}, id='stock_price_chart')
                ], width={'size': 10, 'offset': 1})
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(options=is_list, value="Total Revenue" ,id='is_list', multi=True)
                ], width={'size': 3, 'offset': 1}),
                
                dbc.Col([
                    html.H4("Income Statement Graphs", className='text-center text-primary mb-4')
                ], width={'size': 4, 'offset': 1}),
                
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure={}, id='earning_analysis')
                ], width={'size': 10, 'offset': 1}),
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(options=bs_list, value="Total Assets" ,id='bs_list', multi=True)
                ], width={'size': 3, 'offset': 1}),
                
                dbc.Col([
                    html.H4("Balance Sheet Graphs", className='text-center text-primary mb-4')
                ], width={'size': 4, 'offset': 1}),
                
            ]),
            
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure={}, id='bs_earning_analysis')
                ], width={'size': 10, 'offset': 1}),
            ]),
        
            dbc.Row([
                dbc.Col([
                    dcc.Dropdown(options=cf_list, value="Cash from Ops." ,id='cf_list', multi=True)
                ], width={'size': 3, 'offset': 1}),
                
                dbc.Col([
                    html.H4("Cash Flow Graphs", className='text-center text-primary mb-4')
                ], width={'size': 4, 'offset': 1}),
                
            ]),
            
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure={}, id='cf_earning_analysis')
                ], width={'size': 10, 'offset': 1}),
            ]),
            
            dbc.Row([
                dbc.Col([
                    dcc.Checklist(id='ratios_checklist', options=checklist_options,
                        value=['Return on Equity %'],
                        inline=True,
                        style={'overflowY': 'scroll', 'height': '50px'}
                    ),
                ], width={'size':3, 'offset':1})
            ]),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure={}, id='ratios')
                ], width={'size': 10, 'offset': 1})
            ])
             
        ]),

        competitor_analysis_tab
    ])
], style={"height": "100vh"}, fluid=True)


@app.callback(
    Output(component_id='latest_close_price', component_property='children'),
    Output(component_id='close_price_date', component_property='children'),
    Input(component_id='select_company', component_property= 'value')
)
def update_close_price(company_chosen):
    # Filter the merged_df dataframe for the selected company and get the latest close price
    latest_data = merged_df[merged_df['symbol'] == company_chosen].sort_values(by='Datetime', ascending=False).iloc[0]
    
    # Get the latest close price and the corresponding date
    latest_close = latest_data['Close']
    latest_date = latest_data['Datetime'].strftime('%d %B')  # Format date as "19 August"

    # Format the price and date for display
    close_price_text = f"INR {latest_close:,.2f}"
    date_text = f"{latest_date} - Close Price"

    return close_price_text, date_text

@callback(
    Output(component_id='earning_analysis', component_property="figure"),
    Input(component_id='select_company', component_property="value"),
    Input(component_id='is_list', component_property="value")
)
def update_graph(company_chosen, metrics_chosen):
    # Filter data based on selected company
    if isinstance(metrics_chosen, str):
        metrics_chosen = [metrics_chosen]

    company_data = is_data[is_data['Company Symbol'] == company_chosen]
    
    # Filter data based on the selected metrics
    filtered_data = company_data[company_data['Particulars'].isin(metrics_chosen)]
    filtered_data = filtered_data.drop(columns=['Company Symbol'])
    
    # Reshape the DataFrame for plotting
    melted_df = filtered_data.melt(id_vars='Particulars', var_name='Year', value_name='Amount')
    melted_df['Year'] = melted_df['Year'].astype(int)
    
    # Create the bar chart
    fig = px.bar(melted_df, x='Year', y='Amount', color='Particulars',
                 title=f'IS Metrics for {company_chosen}',
                 labels={'Amount': 'Amount', 'Year': 'Year'},
                 barmode='group')

    # Update layout to match your desired aesthetics
    fig.update_layout(xaxis_title='Year', yaxis_title='Amount', legend_title='Metric', plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      xaxis=dict(showgrid=False, tickfont=dict(color='black'), titlefont=dict(color='black')),
                      yaxis=dict(showgrid=False, tickfont=dict(color='black'), titlefont=dict(color='black')),
                      title=dict(font=dict(color='black'), x=0.5),
                      legend=dict(font=dict(color='black')))

    return fig

@callback(
    Output(component_id='bs_earning_analysis', component_property="figure"),
    Input(component_id='select_company', component_property="value"),
    Input(component_id='bs_list', component_property="value")
)
def update_graph(company_chosen, metrics_chosen):
    # Filter data based on selected company
    if isinstance(metrics_chosen, str):
        metrics_chosen = [metrics_chosen]

    company_data = bs_data[bs_data['Company Symbol'] == company_chosen]
    
    # Filter data based on the selected metrics
    filtered_data = company_data[company_data['Particulars'].isin(metrics_chosen)]
    filtered_data = filtered_data.drop(columns=['Company Symbol'])
    
    # Reshape the DataFrame for plotting
    melted_df = filtered_data.melt(id_vars='Particulars', var_name='Year', value_name='Amount')
    melted_df['Year'] = melted_df['Year'].astype(int)
    
    # Create the bar chart
    fig = px.bar(melted_df, x='Year', y='Amount', color='Particulars',
                 title=f'BS Metrics for {company_chosen}',
                 labels={'Amount': 'Amount', 'Year': 'Year'},
                 barmode='group')

    # Update layout to match your desired aesthetics
    fig.update_layout(xaxis_title='Year', yaxis_title='Amount', legend_title='Metric', plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      xaxis=dict(showgrid=False, tickfont=dict(color='black'), titlefont=dict(color='black')),
                      yaxis=dict(showgrid=False, tickfont=dict(color='black'), titlefont=dict(color='black')),
                      title=dict(font=dict(color='black'), x=0.5),
                      legend=dict(font=dict(color='black')))
    
    fig.update_traces(marker_color='#90EE90', selector=dict(type='bar', name=fig.data[0].name))

    return fig

@callback(
    Output(component_id='cf_earning_analysis', component_property="figure"),
    Input(component_id='select_company', component_property="value"),
    Input(component_id='cf_list', component_property="value")
)
def update_graph(company_chosen, metrics_chosen):
    # Filter data based on selected company
    if isinstance(metrics_chosen, str):
        metrics_chosen = [metrics_chosen]

    company_data = cf_data[cf_data['Company Symbol'] == company_chosen]
    
    # Filter data based on the selected metrics
    filtered_data = company_data[company_data['Particulars'].isin(metrics_chosen)]
    filtered_data = filtered_data.drop(columns=['Company Symbol'])
    
    # Reshape the DataFrame for plotting
    melted_df = filtered_data.melt(id_vars='Particulars', var_name='Year', value_name='Amount')
    melted_df['Year'] = melted_df['Year'].astype(int)
    
    # Create the bar chart
    fig = px.bar(melted_df, x='Year', y='Amount', color='Particulars',
                 title=f'CF Metrics for {company_chosen}',
                 labels={'Amount': 'Amount', 'Year': 'Year'},
                 barmode='group')

    # Update layout to match your desired aesthetics
    fig.update_layout(xaxis_title='Year', yaxis_title='Amount', legend_title='Metric', plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      xaxis=dict(showgrid=False, tickfont=dict(color='black'), titlefont=dict(color='black')),
                      yaxis=dict(showgrid=False, tickfont=dict(color='black'), titlefont=dict(color='black')),
                      title=dict(font=dict(color='black'), x=0.5),
                      legend=dict(font=dict(color='black')))

    return fig

@callback(
    Output(component_id='stock_price_chart', component_property="figure"),
    Input(component_id='select_company', component_property="value"),
    Input(component_id='graph_metric', component_property='value'),
    Input(component_id='n1m', component_property='n_clicks'),
    Input(component_id='n3m', component_property='n_clicks'),
    Input(component_id='n6m', component_property='n_clicks'),
    Input(component_id='n1Y', component_property='n_clicks'),
    Input(component_id='n3Y', component_property='n_clicks'),
    Input(component_id='n5Y', component_property='n_clicks'),
    Input(component_id='n10Y', component_property='n_clicks')
)
def update_graph(company_chosen, metric, n1m, n3m, n6m, n1Y, n3Y, n5Y, n10Y):
    # Define the end date and default start date (last 30 days)
    end_date = datetime(2024, 8, 20)
    start_date = end_date - timedelta(days=30)

    # Identify which button was clicked to set the appropriate date range
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'n1m':
            start_date = end_date - timedelta(days=30)
        elif button_id == 'n3m':
            start_date = end_date - timedelta(days=90)
        elif button_id == 'n6m':
            start_date = end_date - timedelta(days=180)
        elif button_id == 'n1Y':
            start_date = end_date - timedelta(days=365)
        elif button_id == 'n3Y':
            start_date = end_date - timedelta(days=3*365)
        elif button_id == 'n5Y':
            start_date = end_date - timedelta(days=5*365)
        elif button_id == 'n10Y':
            start_date = end_date - timedelta(days=10*365)

    # Filter the merged_df dataframe for the selected company and date range
    company_data = merged_df[(merged_df['symbol'] == company_chosen) &
                             (merged_df['Datetime'] >= start_date) &
                             (merged_df['Datetime'] <= end_date)]

    # Check if the selected metric exists in the merged_df dataframe
    if metric not in merged_df.columns:
        return dash.no_update

    # Generate the line chart using Plotly Express for the selected metric
    fig = px.line(
        company_data,
        x='Datetime',
        y=metric,
        title=f'Daily {metric} for {company_chosen}'
    )

    # Add volume as a bar chart on the secondary y-axis
    fig.add_bar(
        x=company_data['Datetime'],
        y=company_data['Volume'],
        name='Volume',
        yaxis='y2',
        marker=dict(color='rgba(0, 128, 0, 0.4)'),  # Very light blue color with transparency
    )

    # Update the layout to include the secondary y-axis
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            tickfont=dict(color='black'),
            titlefont=dict(color='black'),
            showline=True,
            linecolor='black',
            linewidth=2,
            showgrid=False,
            nticks=11
        ),
        yaxis=dict(
            tickfont=dict(color='black'),
            titlefont=dict(color='black'),
            showline=True,
            linecolor='black',
            linewidth=2,
            showgrid=False,
            title=metric
        ),
        yaxis2=dict(
            title='Volume',
            overlaying='y',
            side='right',
            showgrid=False,
            tickfont=dict(color='lightblue'),
            titlefont=dict(color='lightblue')
        ),
        title=dict(font=dict(color='black'), x=0.5),
        legend=dict(font=dict(color='black')),
        bargap=0,  # No gap between bars for a continuous look
    )

    return fig

@callback(
    Output(component_id='ratios', component_property="figure"),
    Input(component_id='select_company', component_property="value"),
    Input(component_id='ratios_checklist', component_property='value')
)
def update_graph(selected_company, selected_ratios):
    if not selected_ratios:
        return {}

    company_data = ratios[ratios['Company Symbol'] == selected_company]
    filtered_data = company_data[company_data['Particulars'].isin(selected_ratios)]
    melted_df = filtered_data.melt(id_vars=['Particulars'],
                                   var_name='Year',
                                   value_name='Value',
                                   value_vars=[str(year) for year in range(2014, 2025)])

    melted_df['Value'] = pd.to_numeric(melted_df['Value'], errors='coerce')
    fig = px.line(melted_df, x='Year', y='Value', color='Particulars',
                  title=f'{selected_company} Financial Ratios')
    fig.update_layout(xaxis_title='Year', yaxis_title='Value',
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      title=dict(font=dict(color='black'), x=0.5))
    return fig


# Callback to update the table with columns based on selected criteria
@callback(
    Output('dynamic-table-container', 'children'),
    Input('criteria-dropdown-1', 'value'),
    Input('min-value-input-1', 'value'),
    Input('max-value-input-1', 'value'),
    Input('criteria-dropdown-2', 'value'),
    Input('min-value-input-2', 'value'),
    Input('max-value-input-2', 'value'),
    Input('criteria-dropdown-3', 'value'),
    Input('min-value-input-3', 'value'),
    Input('max-value-input-3', 'value'),
    Input('criteria-dropdown-4', 'value'),
    Input('min-value-input-4', 'value'),
    Input('max-value-input-4', 'value'),
    Input('criteria-dropdown-5', 'value'),
    Input('min-value-input-5', 'value'),
    Input('max-value-input-5', 'value')
)
def update_table(criteria1, min1, max1, criteria2, min2, max2, criteria3, min3, max3, criteria4, min4, max4, criteria5, min5, max5):
    # List of selected criteria with their min and max values
    criteria_list = [
        {'criteria': criteria1, 'min': min1, 'max': max1},
        {'criteria': criteria2, 'min': min2, 'max': max2},
        {'criteria': criteria3, 'min': min3, 'max': max3},
        {'criteria': criteria4, 'min': min4, 'max': max4},
        {'criteria': criteria5, 'min': min5, 'max': max5},
    ]

    # Filter out criteria that are not selected
    selected_criteria = [c for c in criteria_list if c['criteria']]

    # If no criteria are selected, return an empty table
    if not selected_criteria:
        return dbc.Table([
            html.Thead(html.Tr([html.Th("Symbol"), html.Th("Close")])),
            html.Tbody([])  # Empty body
        ], bordered=True, dark=False, hover=True, responsive=True, striped=True)

    # Step 1: Sort and get the latest available data for each symbol in val_ratios
    val_ratios_latest = val_ratios.sort_values(by=['symbol', 'Datetime'], ascending=[True, False]).groupby('symbol').first().reset_index()

    # Step 2: Apply filtering to val_ratios_latest based on the selected criteria
    for criterion in selected_criteria:
        criteria_name = criterion['criteria']
        min_value = criterion['min']
        max_value = criterion['max']

        if criteria_name in val_ratios_latest.columns:
            # Ensure the column is numeric
            val_ratios_latest[criteria_name] = pd.to_numeric(val_ratios_latest[criteria_name], errors='coerce')

            # Apply filtering
            if min_value is not None:
                val_ratios_latest = val_ratios_latest[val_ratios_latest[criteria_name] >= min_value]
            if max_value is not None:
                val_ratios_latest = val_ratios_latest[val_ratios_latest[criteria_name] <= max_value]

    # Step 3: Prepare the header row with dynamic columns
    header_row = [html.Th("Symbol"), html.Th("Close")] + [html.Th(criterion['criteria']) for criterion in selected_criteria]

    # Step 4: Populate the table rows
    table_rows = []
    for _, row_data in val_ratios_latest.iterrows():
        row = [html.Td(row_data['symbol'])]

        # Get the close value
        symbol = row_data['symbol']
        close_value = data.loc[data['symbol'] == symbol, 'Close'].values[-1] if not data.loc[data['symbol'] == symbol, 'Close'].empty else None
        row.append(html.Td(close_value))

        # Add the criteria values
        for criterion in selected_criteria:
            criteria_name = criterion['criteria']
            criteria_value = row_data.get(criteria_name, None)
            row.append(html.Td(criteria_value))

        table_rows.append(html.Tr(row))

    # Step 5: Return the populated table
    return dbc.Table([
        html.Thead(html.Tr(header_row)),
        html.Tbody(table_rows)
    ], bordered=True, dark=False, hover=True, responsive=True, striped=True)

@app.callback(
    Output(component_id='company_name',component_property= 'children'),
    Output(component_id='industry', component_property='children'),
    Output(component_id='isin_code', component_property='children'),
    Input(component_id='select_company', component_property='value')
)
def update_card(selected_company):
    # Filter the DataFrame for the selected company
    company_data = company_basic_data[company_basic_data['symbol'] == selected_company].iloc[0]

    # Extract values
    company_name = company_data['Company Name']
    industry = company_data['Industry']
    isin_code = company_data['ISIN Code']

    return company_name, industry, isin_code

if __name__ == '__main__':
    app.run(debug=True)
