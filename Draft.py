from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import pyodbc
import datetime
import config

# noinspection DuplicatedCode




INTERVAL = 25  # how many seconds between each layout
UPDATE_INTERVAL = 60  # how many seconds before updating the data

colors = {'background': '#4f81bd', 'text': 'white'}
borders = {'border': '2px #073763 solid', 'border-radius': '15px'}
headerstyle = {'height': 100,
               'textAlign': 'center',
               'color': colors['text'],
               'backgroundColor': colors['background'],
               'fontSize': 24,
               'border': '2px #073763 solid',
               'border-radius': '4px'}
app = dash.Dash(__name__)

# app.config.suppress_callback_exceptions = True
app.layout = html.Div(children=[
    html.Div(id='app-container'),
    dcc.Interval(
        id='interval1',
        interval=INTERVAL * 1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div(id='out', style={'display': 'none'}),
    dcc.Interval(id='interval2',
                 interval=UPDATE_INTERVAL * 1000,
                 n_intervals=0)
], )


@app.callback(Output('out', 'children'),
              [Input('interval2', 'n_intervals')])
def UPDATE_DATA(n_intervals):
    conn = pyodbc.connect('DSN=keyvanTest;'
                          'Database=Digitalization;'
                          'TrustedConnection=yes;'
                          'MARS_Connection=yes;'
                          'UID=PyUsrDashRdr;'
                          'PWD=dash*reader')
    global DashboardValues
    DashboardValues = pd.read_sql(config.HM_SQL_Data['Dashboard_Values'], conn)
    global tab5_figure_df
    tab5_figure_df = pd.read_sql(config.HM_SQL_Data['tab5_df'], conn)
    global tab4_figure_df
    tab4_figure_df = pd.read_sql(config.HM_SQL_Data['tab4_df'], conn)
    global complianceData
    complianceData = pd.read_sql(config.HM_SQL_Data['compliance_Data'], conn)
    global dates1
    # converts the date from int to a date in year/month format
    dates1 = [datetime.datetime.strptime(str(dt_int), "%Y%m") for dt_int in tab4_figure_df['YYYYMM']]
    global dates2
    dates2 = [datetime.datetime.strptime(str(dt_int), "%Y%m") for dt_int in tab5_figure_df['YYYYMM']]
    global fig1
    fig1 = px.bar(tab4_figure_df, x=dates1, y='MeanTime',
                  text='MeanTime',
                  labels=dict(x='Month'),
                  template='simple_white',
                  height=800
                  )
    fig1.update_xaxes(
        tickvals=dates1,
        tickformat='%b %Y'
    )
    fig1.update_yaxes(
        title_text='Mean Time (hours)'
    )
    global fig2
    fig2 = px.bar(tab5_figure_df, x=dates2, y='MeanTime',
                  text='MeanTime',
                  labels=dict(x='Month'),
                  template='simple_white',
                  height=800
                  )
    fig2.update_xaxes(
        tickvals=dates2,
        tickformat='%b %Y'
    )
    fig2.update_yaxes(
        title_text='Mean Time (hours)'
    )
    global fig3
    fig3 = px.bar(complianceData, x='weeknames', y='count',
                  template='simple_white',
                  height=800,
                  labels='count'

                  )
    fig3.update_xaxes(
        title_text='Weeks'
    )
    fig3.update_yaxes(
        title_text='Compliance Percentage',
        tickformat='1%',
    )
    # fig3.add_trace(go.Scatter(name='line of best fit', x='Weeks', y=complianceData['bestfit'], mode='lines'))
    return n_intervals


@app.callback(Output('app-container', 'children'),
              [Input('interval1', 'n_intervals')])
def CHANGE_PAGE(n_intervals):
    # references to the dataframes that are displayed in the dashboard
    Total_Time_Scheduled = DashboardValues.iloc[0, 0]
    Total_Time_Unscheduled = DashboardValues.iloc[0, 1]
    Total_Time_ScheduledP = DashboardValues.iloc[0, 2]
    Total_Time_UnscheduledP = DashboardValues.iloc[0, 3]
    Leading_Scheduled = DashboardValues.iloc[0, 4]
    Leading_Unscheduled = DashboardValues.iloc[0, 5]
    MTTR = tab4_figure_df.iloc[0, 2]
    MTBF = tab5_figure_df.iloc[0, 2]
    MTTR_Definition = "The average time needed to restore an asset to its full operational capabilities " \
                      "after a loss of function "
    MTBF_Definition = "The average length of operating time between failures for an asset or " \
                      "component"

    # noinspection DuplicatedCode
    # layouts the app will roll through are contained in this list
    PAGES = [
        dcc.Tab(label='Tab one', children=[
            dbc.Row(html.H1(config.HM_SQL_Data['dashboard_Header']), style=headerstyle),
            dbc.Row(children=[
                html.Span("Leading Indicators",
                          style={'textAlign': 'left',
                                 'color': colors['text'],
                                 'background': colors['background'],
                                 'fontSize': 60,
                                 'display': 'inline-block',
                                 'margin-left': 150,
                                 'margin-top': 10,
                                 'border': '4px #073763 solid',
                                 'border-radius': '4px'
                                 }),
                html.Span("Lagging Indicators",
                          style={'textAlign': 'right',
                                 'color': colors['text'],
                                 'background': colors['background'],
                                 'fontSize': 60,
                                 'display': 'inline-block',
                                 'margin-left': 670,
                                 'margin-top': 10,
                                 'border': '4px #073763 solid',
                                 'border-radius': '4px'
                                 }),

            ]),
            dbc.Row(children=[

                html.Span("% Scheduled", style={'textAlign': 'center',
                                                'color': colors['text'],
                                                'background': colors['background'],
                                                'fontSize': 50,
                                                'display': 'inline-block',
                                                'margin-left': 10,
                                                'margin-top': 10,
                                                'border': '4px #073763 solid',
                                                'border-radius': '4px',
                                                'width': 350
                                                }, ),
                html.Span("% Unscheduled", style={'textAlign': 'center',
                                                  'color': colors['text'],
                                                  'background': colors['background'],
                                                  'fontSize': 50,
                                                  'display': 'inline-block',
                                                  'margin-left': 10,
                                                  'margin-top': 10,
                                                  'border': '4px #073763 solid',
                                                  'border-radius': '4px',
                                                  'width': 350
                                                  }, ),
                html.Span("% Scheduled", style={'textAlign': 'center',
                                                'color': colors['text'],
                                                'background': colors['background'],
                                                'fontSize': 50,
                                                'display': 'inline-block',
                                                'margin-left': 400,
                                                'border': '4px #073763 solid',
                                                'border-radius': '4px',
                                                'width': 350
                                                }, ),
                html.Span("% Unscheduled", style={'textAlign': 'center',
                                                  'color': colors['text'],
                                                  'background': colors['background'],
                                                  'fontSize': 50,
                                                  'display': 'inline-block',
                                                  'margin-left': 10,
                                                  'border': '4px #073763 solid',
                                                  'border-radius': '4px',
                                                  'width': 350
                                                  }, ),
            ]),
            dbc.Row(children=[
                html.Span(Leading_Scheduled, style={'textAlign': 'center',
                                                    'color': colors['text'],
                                                    'background': colors['background'],
                                                    'fontSize': 50,
                                                    'display': 'inline-block',
                                                    'margin-left': 10,
                                                    'margin-top': 10,
                                                    'border': '4px #073763 solid',
                                                    'border-radius': '4px',
                                                    'width': 350
                                                    }),
                html.Span(Leading_Unscheduled, style={'textAlign': 'center',
                                                      'color': colors['text'],
                                                      'background': colors['background'],
                                                      'fontSize': 50,
                                                      'display': 'inline-block',
                                                      'margin-left': 10,
                                                      'border': '4px #073763 solid',
                                                      'border-radius': '4px',
                                                      'width': 350
                                                      }, ),
                html.Span(MTTR, style={'textAlign': 'center',
                                       'color': colors['text'],
                                       'background': colors['background'],
                                       'fontSize': 50,
                                       'display': 'inline-block',
                                       'margin-left': 400,
                                       'border': '4px #073763 solid',
                                       'border-radius': '4px',
                                       'width': 350
                                       }, ),
                html.Span(MTBF, style={'textAlign': 'center',
                                       'color': colors['text'],
                                       'background': colors['background'],
                                       'fontSize': 50,
                                       'display': 'inline-block',
                                       'margin-left': 10,
                                       'margin-top': 10,
                                       'border': '4px #073763 solid',
                                       'border-radius': '4px',
                                       'width': 350
                                       }, )
            ]),
            html.Div(html.Img(src=app.get_asset_url("NASLogo.jpg"),
                              style={'height': '25%',
                                     'width': '25%',
                                     }),
                     style={
                         'textAlign': 'center'
                     }
                     ),
        ]),
        dcc.Tab(label='Tab two', children=[
            html.Div(children=[
                dbc.Row(html.H1('Past Month: Scheduled vs Unscheduled Maintenance'), style=headerstyle),
                dbc.Row(children=[
                    dbc.Col(html.Span("Total Time Hours"),
                            style={'textAlign': 'left',
                                   'color': colors['text'],
                                   'background': colors['background'],
                                   'fontSize': 60,
                                   'display': 'inline-block',
                                   'margin-left': 175,
                                   'margin-top': 10,
                                   'border': '4px #073763 solid',
                                   'border-radius': '4px'
                                   }),
                    dbc.Col(html.Span("Total Time %"),
                            style={'textAlign': 'right',
                                   'color': colors['text'],
                                   'background': colors['background'],
                                   'fontSize': 60,
                                   'display': 'inline-block',
                                   'margin-left': 725,
                                   'margin-top': 10,
                                   'border': '4px #073763 solid',
                                   'border-radius': '4px'
                                   }),
                ], ),
                dbc.Row(children=[

                    html.Span("Scheduled", style={'textAlign': 'center',
                                                  'color': colors['text'],
                                                  'background': colors['background'],
                                                  'fontSize': 50,
                                                  'display': 'inline-block',
                                                  'margin-left': 10,
                                                  'margin-top': 10,
                                                  'border': '4px #073763 solid',
                                                  'border-radius': '4px',
                                                  'width': 350
                                                  }),
                    html.Span("Unscheduled", style={'textAlign': 'center',
                                                    'color': colors['text'],
                                                    'background': colors['background'],
                                                    'fontSize': 50,
                                                    'display': 'inline-block',
                                                    'margin-left': 10,
                                                    'margin-top': 10,
                                                    'border': '4px #073763 solid',
                                                    'border-radius': '4px',
                                                    'width': 350
                                                    }, ),
                    html.Span("% Scheduled", style={'textAlign': 'center',
                                                    'color': colors['text'],
                                                    'background': colors['background'],
                                                    'fontSize': 50,
                                                    'display': 'inline-block',
                                                    'margin-left': 400,
                                                    'border': '4px #073763 solid',
                                                    'border-radius': '4px',
                                                    'width': 350
                                                    }, ),
                    html.Span("% Unscheduled", style={'textAlign': 'center',
                                                      'color': colors['text'],
                                                      'background': colors['background'],
                                                      'fontSize': 50,
                                                      'display': 'inline-block',
                                                      'margin-left': 10,
                                                      'border': '4px #073763 solid',
                                                      'border-radius': '4px',
                                                      'width': 350
                                                      }, ),
                ]),
                dbc.Row(id='row4', children=[
                    html.Span(Total_Time_Scheduled, style={'textAlign': 'center',
                                                           'color': colors['text'],
                                                           'background': colors['background'],
                                                           'fontSize': 50,
                                                           'display': 'inline-block',
                                                           'margin-left': 10,
                                                           'margin-top': 10,
                                                           'border': '4px #073763 solid',
                                                           'border-radius': '4px',
                                                           'width': 350
                                                           }),
                    html.Span(Total_Time_Unscheduled, style={'textAlign': 'center',
                                                             'color': colors['text'],
                                                             'background': colors['background'],
                                                             'fontSize': 50,
                                                             'display': 'inline-block',
                                                             'margin-left': 10,
                                                             'border': '4px #073763 solid',
                                                             'border-radius': '4px',
                                                             'width': 350
                                                             }, ),
                    html.Span(Total_Time_ScheduledP, style={'textAlign': 'center',
                                                            'color': colors['text'],
                                                            'background': colors['background'],
                                                            'fontSize': 50,
                                                            'display': 'inline-block',
                                                            'margin-left': 400,
                                                            'border': '4px #073763 solid',
                                                            'border-radius': '4px',
                                                            'width': 350
                                                            }, ),
                    html.Span(Total_Time_UnscheduledP, style={'textAlign': 'center',
                                                              'color': colors['text'],
                                                              'background': colors['background'],
                                                              'fontSize': 50,
                                                              'display': 'inline-block',
                                                              'margin-left': 10,
                                                              'margin-top': 10,
                                                              'border': '4px #073763 solid',
                                                              'border-radius': '4px',
                                                              'width': 350
                                                              }, )
                ]),
                html.Div(html.Img(src=app.get_asset_url("NASLogo.jpg"),
                                  style={'height': '25%',
                                         'width': '25%',
                                         }),
                         style={
                             'textAlign': 'center'
                         }
                         ),
            ])
        ]),
        dcc.Tab(label='Tab Three', children=[
            dbc.Row(html.H1('HM Daytech Compliance: Labor vs Scheduled - Breaks'), style=headerstyle),
            dbc.Row(dcc.Graph(
                id='ComplianceGraph',
                figure=fig3,
            ),
            )
        ]),
        dcc.Tab(label='Tab Four', children=[
            html.Div(children=
                     [dbc.Row(html.H1('Defining MTTR and MTBF', ), style=headerstyle),
                      html.Div("MTTR-Mean Time to Repair:",
                               style={
                                   'textAlign': 'center',
                                   'color': colors['text'],
                                   'backgroundColor': colors['background'],
                                   'fontSize': 60,
                                   'border': borders['border'],
                                   'border-radius': borders['border-radius'],
                                   'width': 800,
                                   'margin-bottom': 3,
                                   'margin-top': 5}),
                      dcc.Textarea(value=MTTR_Definition,
                                   style={
                                       'fontSize': 50,
                                       'color': colors['text'],
                                       'backgroundColor': colors['background'],
                                       'border': borders['border'],
                                       'border-radius': borders['border-radius'],
                                       'width': '100%', 'height': 150
                                   }),
                      html.Div("MTBF- Mean Time Between Failure:",
                               style={
                                   'margin-top': 50,
                                   'textAlign': 'center',
                                   'color': colors['text'],
                                   'backgroundColor': colors['background'],
                                   'fontSize': 60,
                                   'border': borders['border'],
                                   'border-radius': borders['border-radius'],
                                   'width': 1000,
                                   'margin-bottom': 3
                               }),
                      dcc.Textarea(
                          value=MTBF_Definition,
                          style={
                              'fontSize': 50,
                              'color': colors['text'],
                              'backgroundColor': colors['background'],
                              'border': borders['border'],
                              'border-radius': borders['border-radius'],
                              'width': '100%', 'height': 150
                          }),
                      ],

                     )
        ]),
        dcc.Tab(label='Tab Five', children=[
            html.Div(html.Img(src=app.get_asset_url("mtbfmttr_graphic.jpg"),
                              style={
                                  'height': '85%',
                                  'width': '85%',
                              }),
                     style={
                         'textAlign': 'center'
                     })
        ]),
        dcc.Tab(label='Tab Six', children=[
            html.Div(children=[
                dbc.Row(dbc.Col(html.H1('Mean Time to Repair(MTTR): Mechanical Only'), style=headerstyle), ),
                dbc.Row(dbc.Col(dcc.Graph(
                    id='MTTRGraph',
                    figure=fig1,
                )
                ),
                )
            ])
        ]),
        dcc.Tab(label='Tab Seven', children=[
            dbc.Row(dbc.Col(html.H1('Mean Time Between Failure(MTBF): Mechanical Only')), style=headerstyle, ),
            dcc.Graph(
                figure=fig2
            )
        ])
    ]
    return PAGES[n_intervals % len(PAGES)]


if __name__ == '__main__':
    app.run_server(debug=True)
