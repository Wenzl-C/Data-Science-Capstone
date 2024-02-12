# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px








# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()




# Site dropdown menu options
site_dropdown = [
    {'label':'ALL', 'value':'ALL'},
    {'label':'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label':'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
    {'label':'KSC LC-39A', 'value': 'KSC LC-39A'},
    {'label':'VAFB LC-4E', 'value': 'VAFB LC-4E'}
                ]




# Create a dash application
app = dash.Dash(__name__)




# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Br(),
                                html.Div([html.Label('Select Launch Site:'),
                                        dcc.Dropdown(
                                            id= 'site-dropdown',
                                            options= site_dropdown,
                                            value='ALL',
                                            placeholder='All Sites',
                                            searchable=True)]),








                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart',style={'display':'flex'})),
                                html.Br(),




                                # TASK 3: Add a slider to select payload range
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=10,
                                                    marks={i: str(i) for i in range(0,10001,500)},
                                                    value=[min_payload,max_payload]
                                                ),




                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])




# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site',
                    title='Success Rates at Different Launch Sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        class_counts = filtered_df['class'].value_counts()
        fig = px.pie(values=class_counts.values, names=class_counts.index,
                    title=f'Success Rate of Launches at {entered_site}')
        return fig






# TASK 4:a
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(entered_site, payload_range):
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', color='Booster Version',
                         title='Scatter Plot of Payload Mass (kg) vs. Launch Success')
        return fig
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) &
                                (spacex_df['Payload Mass (kg)'].between(payload_range[0], payload_range[1]))]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version', title=f'Scatter Plot of Payload Mass vs. Launch Success at {entered_site}')
        return fig








# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)