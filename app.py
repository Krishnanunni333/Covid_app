import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from datetime import date
import datetime
import geopandas as gpd
import plotly.graph_objects as go
st.title(" **COVID-19 WEB APP** ")
st.markdown("This application is a Streamlit dashboard that can be used "
            "to analyze COVID-19 data across the world :earth_asia::mask:")
data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
def country(countrys):
    d=data[data['location']==countrys]
    start_date = st.sidebar.date_input('Start date',datetime.datetime(2019,12,31))
    end_date= st.sidebar.date_input('End date',recent_date)
    d['ndate'] = pd.to_datetime(d['date'])
    d=d[d['ndate'] >= pd.to_datetime(start_date)]
    d=d[d['ndate'] <= pd.to_datetime(end_date)]
    y_2=np.sqrt(d['new_cases'])
    y_3=np.sqrt(d['new_deaths'])
    st.markdown(' #### Graph of {} from {} to {}  '.format(countrys,start_date,end_date))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d['ndate'], y=y_2,
                    mode='lines',
                    name='New cases'))
    fig.add_trace(go.Scatter(x=d['ndate'], y=y_3,
                    mode='lines', name='New Deaths'))
    st.plotly_chart(fig)
    if st.checkbox("Show raw data", False):
        st.subheader("Raw data of {} from {} to {}".format(countrys,start_date,end_date))
        st.dataframe(d.fillna('Not available'))
def map(s,t,by):
    k=np.log(s[t])
    fig = go.Figure(data=go.Choropleth(
    locations = s['iso_code'],
    z = k,
    text = s['location'],
    colorscale = 'Rainbow',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = by,
    ))

    fig.update_layout(
    title_text='Latest',
    geo=dict(
        showframe=True,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://ourworldindata.org/">\
            ourworldindata</a>',
        showarrow = False
    )])
    st.plotly_chart(fig)
p= pd.to_datetime(data['date'])
recent_date =p.max()
st.markdown('## WORLD MAP')
date = st.date_input('Select date for the map',recent_date)
date=date.strftime('%Y-%m-%d')
s=data[data['date']==date]
k=s[data['location']=='World']
st.markdown('### On this date  ({})  , glboally, there are  {}  new cases,  {}  new deaths. There are  {}  total cases and  {}  total deaths also.'.format(date,k.iloc[0]['new_cases'],k.iloc[0]['new_deaths'],
              k.iloc[0]['total_cases'],k.iloc[0]['total_deaths']))
by=st.selectbox('Based on',('Total cases', 'New cases','Total deaths','New Deaths','GDP per capita'))
if by=='Total cases':
    s=s[['location','total_cases','iso_code']]
    map(s,'total_cases',by)
elif by=='New cases':
    s=s[['location','new_cases','iso_code']]
    map(s,'new_cases',by)
elif by=='Total deaths':
    s=s[['location','total_deaths','iso_code']]
    map(s,'total_deaths',by)
elif by=='New Deaths':
    s=s[['location','new_deaths','iso_code']]
    map(s,'new_deaths',by)
elif by=='GDP per capita':
    s=s[['location','gdp_per_capita','iso_code']]
    map(s,'gdp_per_capita',by)
option=list(data.location.unique())
option=option[:len(option)-2]
countrys = st.sidebar.selectbox(
        'Select Country ',(option))
country(countrys)

