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
    return px.line(data_frame=sorted_df ,x="Date",y=radio_value,title=title, connectgaps=False)



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