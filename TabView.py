import csv
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sqlConn import DataUtility

query = '''

select * from PdMEng.kjpDashboardValues

'''
sql = DataUtility()
conn = #replace with odbc string
df = pd.DataFrame(sql.min_query(query))
df.to_csv("assets/bs.csv", index=False)


with open("assets/bs.csv", 'r') as csvfile:
    so = csv.reader(csvfile, delimiter=',', quotechar='"')
    so_data = []
    for row in so:
        so_data.append(row)

Total_Time_Scheduled = so_data[1]
Total_Time_Unscheduled = so_data[2]
Total_Time_ScheduledP = so_data[3]
Total_Time_UnscheduledP = so_data[4]
Leading_Scheduled = so_data[5]
Leading_Unscheduled = so_data[6]
MTTR = so_data[7]
MTBF = so_data[8]
MTTR_Definition = "This metric is the average time needed to restore an asset to its full operational capabilities " \
                  "after a loss of function "
MTBF_Definition = "This metric is the average length of operating time between failures for an asset or " \
                  "component"

colors = {'background': '#4f81bd', 'text': 'white'}
borders = {'border': '2px #073763 solid', 'border-radius': '15px'}

app = dash.Dash(__name__)
# app.config.suppress_callback_exceptions = True
# noinspection DuplicatedCode

app.layout = html.Div(
    dcc.Tabs(children=[
        dcc.Tab(label='Tab one', children=[
            dbc.Row(html.H1('Hot Mill Maintenance KPI Dashboard (Total Score)'), style={
                'height': 100,
                'textAlign': 'center',
                'color': colors['text'],
                'backgroundColor': colors['background'],
                'fontSize': 24,
                'border': '2px #073763 solid',
                'border-radius': '4px'
            }, ),
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
                html.Span(MTTR, style={'textAlign': 'right',
                                       'color': colors['text'],
                                       'background': colors['background'],
                                       'fontSize': 50,
                                       'display': 'inline-block',
                                       'margin-left': 550,
                                       'border': '4px #073763 solid',
                                       'border-radius': '4px'
                                       }, ),
                html.Span(MTBF, style={'textAlign': 'right',
                                       'color': colors['text'],
                                       'background': colors['background'],
                                       'fontSize': 50,
                                       'display': 'inline-block',
                                       'margin-left': 250,
                                       'margin-top': 10,
                                       'border': '4px #073763 solid',
                                       'border-radius': '4px'
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
                dbc.Row(html.H1('May 2021: Scheduled vs Unscheduled Maintenance'),
                        style={
                            'height': 100,
                            'textAlign': 'center',
                            'color': colors['text'],
                            'backgroundColor': colors['background'],
                            'fontSize': 24,
                            'border': '2px #073763 solid',
                            'border-radius': '4px'
                        }, ),
                dbc.Row(children=[
                    dbc.Col(html.Span("Total Time Hours"),
                            style={'textAlign': 'left',
                                   'color': colors['text'],
                                   'background': colors['background'],
                                   'fontSize': 60,
                                   'display': 'inline-block',
                                   'margin-left': 200,
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
                                   'margin-left': 700,
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
                    html.Span(Total_Time_ScheduledP, style={'textAlign': 'right',
                                                            'color': colors['text'],
                                                            'background': colors['background'],
                                                            'fontSize': 50,
                                                            'display': 'inline-block',
                                                            'margin-left': 550,
                                                            'border': '4px #073763 solid',
                                                            'border-radius': '4px'
                                                            }, ),
                    html.Span(Total_Time_UnscheduledP, style={'textAlign': 'right',
                                                              'color': colors['text'],
                                                              'background': colors['background'],
                                                              'fontSize': 50,
                                                              'display': 'inline-block',
                                                              'margin-left': 225,
                                                              'margin-top': 10,
                                                              'border': '4px #073763 solid',
                                                              'border-radius': '4px'
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
        dcc.Tab(label='Tab three', children=[
            html.Div(children=

                     [html.H1('Defining MTTR and MTBF',
                              style={
                                  'height': 100,
                                  'textAlign': 'center',
                                  'color': colors['text'],
                                  'backgroundColor': colors['background'],
                                  'fontSize': 65,
                                  'border': borders['border'],
                                  'border-radius': borders['border-radius']}),
                      html.Div("MTTR-Mean Time to Repair:",
                               style={
                                   'textAlign': 'center',
                                   'color': colors['text'],
                                   'backgroundColor': colors['background'],
                                   'fontSize': 60,
                                   'border': borders['border'],
                                   'border-radius': borders['border-radius'],
                                   'width': 800,
                                   'margin-bottom': 3}),
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
        dcc.Tab(label='Tab Four', children=[
            html.Div(children=[
                dbc.Row(dbc.Col(html.H1('Mean Time to Repair(MTTR): Mechanical Only May 2021')),
                        style={
                            'height': 100,
                            'textAlign': 'center',
                            'color': colors['text'],
                            'backgroundColor': colors['background'],
                            'fontSize': 24,
                            'border': '2px #073763 solid',
                            'border-radius': '4px'
                        }, ),
                dbc.Row(dbc.Col(dcc.Graph(
                    id='Graph',
                    figure={
                        'data': [
                            {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                            {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                        ],
                        'layout': {
                            'title': 'Dash Data Visualization'
                        }
                    }
                )
                ))
            ])
        ]),
        dcc.Tab(label='Tab Five', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 4, 3],
                         'type': 'line', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [5, 4, 3],
                         'type': 'line', 'name': u'Montréal'},
                    ]
                }
            )
        ]), ], ),
)

if __name__ == '__main__':
    app.run_server(debug=True)
