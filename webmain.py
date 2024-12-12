from dash import Dash,html,dcc,callback,Input,Output,dash_table,_dash_renderer
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
_dash_renderer._set_react_version("18.2.0")



df = pd.read_csv('NewTable_202412100949.csv')
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
else:
    raise ValueError("The Date column is missing")



df['Days'] = (df['Date']-df['Date'].min()).dt.days
df['Date_str'] = df['Date'].dt.strftime('%Y-%m-%d')

app= Dash(__name__)
"""
#radio資料
# radio_data=[['Close',"收盤價"],["Open","開盤價"],["High","最高價"],["Low","最低價"],['Volume',"成交量"]]



# rows = [
#     dmc.TableTr(
#         [
#             dmc.TableTd(df['Date_str']),
#             dmc.TableTd(df["Close"])
#         ]
#     )
#     for df in radio_data
# ]



# head = dmc.TableThead(
#     dmc.TableTr(
#         [
#             dmc.TableTh("日期"),
#             dmc.TableTh("收盤價")
#         ]
#     )
# )

# body = dmc.TableTbody(rows)
# caption = dmc.TableCaption("Taiwan NO.1")
"""



app.layout = html.Div(
    [
        html.H1("台積電股票分析",style={"textAlign":"center"}),
        dcc.RadioItems(['Close',"Open","High","Low","Volume"],value='Close',inline=True,id='radio_item'),
        dash_table.DataTable(
                            data = df.to_dict('records'),
                            page_size = 10,
                            id="datatable",
                            columns=[
                                    {"name": "Date", "id": "Date_str"},  # 顯示格式化後的 Date_str 欄位
                                    {"name": "Close", "id": "Close"},
                                    {"name": "Open", "id": "Open"},
                                    {"name": "High", "id": "High"},
                                    {"name": "Low", "id": "Low"},
                                    {"name": "Volume", "id": "Volume"},
                                    {"name": "Days", "id": "Days"}
                                ],
                            ),
        dcc.Graph(id='graph-content')


    ]
)

'''
# app.layout = dmc.MantineProvider(
#     [
#         dmc.Container(
#             dmc.Title(f'台積電股票分析',order=2),
#             fluid=True,
#             ta="center",
#             p=30
#         )
#     ,
#         dmc.Flex(
#             [
#                 dmc.RadioGroup(
#                     children = dmc.Group([dmc.Radio(l, value=k) for k,l in radio_data],my=10),
#                     id = "radio_item",
#                     value = "Close",
#                     label= "請選擇想了解的資料",
#                     size='md',
#                     mb=10
#                 )
#             ,
#                 dmc.ScrollArea(
#                     dmc.Table(
#                         [head,body,caption],
#                         w="100%"
#                     ),
#                     h=300,
#                     w="50%"
#                 )
#             ],
#             direction={"base":"column","sm":"row"},
#             gap={"base":"sm","sm":"lg"},
#             justify={"base":"center"}
#         )
#     ,
#         dmc.Container(
#             dcc.Graph(id="graph-content")
#         )
#     ]
# )
'''
#圖表事件
@callback(
    Output('graph-content','figure'),
    Input('radio_item','value')
)
def change_graph(radio_value):
    sorted_df = df.sort_values('Date')
    if radio_value =='Close':
        title = f'{radio_value}'
    elif radio_value =='Open':
        title = f'{radio_value}'
    elif radio_value =='High':
        title = f'{radio_value}'
    elif radio_value =='Low':
        title = f'{radio_value}'
    elif radio_value =='Volume':
        title = f'{radio_value}'
    return px.line(data_frame=sorted_df ,x="Date",y=radio_value,title=title)



@callback(
    Output('datatable','data'),
    Output('datatable','columns'),
    Input('radio_item','value')
)
def update_table(radio_value):
    columns=[{'id':"Date_str",'name':"Date"}
             ]
    if radio_value =='Close':
        columns.append ({'id':'Close','name':'Close'})
    elif radio_value =='Open':
        columns.append ({'id':'Open','name':'Open'})
    elif radio_value =='High':
        columns.append ({'id':'High','name':'High'})
    elif radio_value =='Low':
        columns.append ({'id':'Low','name':'Low'})
    elif radio_value =='Volume':
        columns.append ({'id':'Volume','name':'Volume'})
    return (df.to_dict('records')),columns



if __name__ =='__main__':
    app.run(debug=True)