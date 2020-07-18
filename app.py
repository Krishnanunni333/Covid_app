import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date
import datetime
import plotly.graph_objects as go
from covid import Covid
from PIL import Image
import requests
from io import BytesIO
import pycountry
covid = Covid()
covid_2 = Covid(source="worldometers")
st.header(':earth_asia:')
st.title(" **COVID-19 WEB APP** ")
st.header("This application is a Streamlit dashboard that can be used "
            "to analyze COVID-19 data across the world :mask:.")
st.markdown('This app uses daily cases, deaths, and testing (limited) statistics related to the COVID-19 virus for 207 countries provided by <a href="https://ourworldindata.org/" target="_blank">\
            Our World in Data</a>, <a href="https://pypi.org/project/covid/" target="_blank">\
            Covid python package</a>, <a href="https://www.worldometers.info/" target="_blank">\
            worldometers</a> and <a href="https://www.who.int/" target="_blank">\
            WHO.</a>',unsafe_allow_html=True)
@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    return data
data=load_data()
def total_cases_total_deaths(d):
    y_2=np.sqrt(d['total_cases'])
    y_3=np.sqrt(d['total_deaths'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d['ndate'], y=y_2,
                    mode='lines',
                    name='Total cases',fill='tonexty'))
    fig.add_trace(go.Scatter(x=d['ndate'], y=y_3,
                    mode='lines', name='Total Deaths',fill='tozeroy'))
    st.plotly_chart(fig)
def new_cases_new_deaths(d):
    y_2=np.sqrt(d['new_cases'])
    y_3=np.sqrt(d['new_deaths'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d['ndate'], y=y_2,
                    mode='lines',
                    name='New cases',fill='tonexty'))
    fig.add_trace(go.Scatter(x=d['ndate'], y=y_3,
                    mode='lines', name='New Deaths',fill='tozeroy'))
    st.plotly_chart(fig)
def new_test(d):
    html='''#### <span style="color:red">Why is data on testing important?</span>
No country knows the total number of people infected with COVID-19. All we know is the infection status of those who have been tested. All those who have a lab-confirmed infection are counted as confirmed cases.

This means that the counts of confirmed cases depend on how much a country actually tests. Without testing there is no data.

Testing is our window onto the pandemic and how it is spreading. Without data on who is infected by the virus we have no way of understanding the pandemic. Without this data we can not know which countries are doing well, and which are just underreporting cases and deaths.

To interpret any data on confirmed cases we need to know how much testing for COVID-19 the country actually does.'''
    y_3=np.log(d['new_tests'])
    if y_3.isnull().sum()==len(y_3):
        st.markdown('<i>No data is available on new testing for {} .</i>'.format(countrys),unsafe_allow_html=True)
    else:
        fig = px.bar(d, x='date', y='new_tests')
        st.plotly_chart(fig)
    st.markdown(html, unsafe_allow_html=True)
def country_details(d,countrys):
    a3=str(d['iso_code'].values).strip('[]').strip("''").lower()
    ind = pycountry.countries.get(alpha_3=a3).alpha_2.lower()
    if ind =='au':
        ind='at'
    elif ind=='at':
        ind='au'
    response = requests.get('https://www.worldometers.info/img/flags/{}-flag.gif'.format(ind))
    img = Image.open(BytesIO(response.content))
    img=img.convert('RGB')
    newsize = (300, 200) 
    img = img.resize(newsize)
    st.image(img)
    d.fillna('Not Available',inplace=True)
    st.markdown('**_All data as of_** : {}'.format(recent_date.strftime('%Y-%m-%d')))
    st.markdown('**Covid-19 Death rate** : {}'.format(str(d['cvd_death_rate'].values).strip('[]')))
    st.markdown('**Total cases** : {}'.format(covid.get_status_by_country_name(countrys)['confirmed']))
    st.markdown('**Active cases** : {}'.format(covid.get_status_by_country_name(countrys)['active']))
    st.markdown('**Deaths** : {}'.format(covid.get_status_by_country_name(countrys)['deaths']))
    st.markdown('**Recovered** : {}'.format(covid.get_status_by_country_name(countrys)['recovered']))
    st.markdown('**Total Tests** : {}'.format(covid_2.get_status_by_country_name(countrys)['total_tests']))
    st.markdown('**Critical** : {}'.format(covid_2.get_status_by_country_name(countrys)['critical']))
    st.markdown('**GDP per Capita** : {}'.format(str(d['gdp_per_capita'].values).strip('[]')))
    st.markdown('**Population** : {}'.format(str(d['population'].values).strip('[]')))
    st.markdown('**Population density** : {}'.format(str(d['population_density'].values).strip('[]')))
    st.markdown('**Median Age** : {}'.format(str(d['median_age'].values).strip('[]')))
    st.markdown('**Aged 65 older** : {}'.format(str(d['aged_65_older'].values).strip('[]')))
    st.markdown('**Aged 70 older** : {}'.format(str(d['aged_70_older'].values).strip('[]')))
def country(countrys):
    d=data[data['location']==countrys]
    st.subheader('Country wise analysis')
    st.markdown('## <span style="color:#782612  ">{}</span> '.format(countrys),unsafe_allow_html=True)
    start_date = st.sidebar.date_input('Start date',datetime.datetime(2019,12,31))
    end_date= st.sidebar.date_input('End date',recent_date)
    d['ndate'] = pd.to_datetime(d['date'])
    d=d[d['ndate'] >= pd.to_datetime(start_date)]
    d=d[d['ndate'] <= pd.to_datetime(end_date)]
    country_details(d[d['date']==date],countrys)
    st.markdown(' #### Comparison between total cases and total deaths of {} from {} to {}  '.format(countrys,start_date,end_date))
    total_cases_total_deaths(d)
    st.markdown(' #### Comparison between new cases and new deaths of {} from {} to {}  '.format(countrys,start_date,end_date))
    new_cases_new_deaths(d)
    st.markdown(' #### Trend of new tests performed in {}  from {} to {}'.format(countrys,start_date,end_date))
    new_test(d)
    
    if st.checkbox("Show raw data", False):
        st.subheader("Raw data of {} from {} to {}".format(countrys,start_date,end_date))
        st.dataframe(d.fillna('Not available'))
def map(s,t,by,on):
    k=np.log(s[t])
    options = ("orthographic","equirectangular")
    a = st.empty()
    value = a.radio("Select view", options, 1)
    fig = go.Figure(data=go.Choropleth(
    locations = s['iso_code'],
    z = k,
    text = s['location'],
    colorscale = 'Reds',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = by,
    ))
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C',
         landcolor='rgba(51,17,0,0.2)',
         subunitcolor='grey'),font = {"size": 9, "color":"White"},
         titlefont = {"size": 15, "color":"White"},
         margin={"r":0,"t":40,"l":0,"b":0},
         paper_bgcolor='#4E5D6C',
         plot_bgcolor='#4E5D6C',
                                  )
    fig.update_layout(
    title_text='Map of {}'.format(on),
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type=value,),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://ourworldindata.org/" target="_blank">\
            ourworldindata</a>',
        showarrow = False
    )],)
    st.plotly_chart(fig)
def find_case(s,on,k):
    by=st.selectbox('Based on',('Total cases', 'New cases','Total deaths','New Deaths','Total tests'))
    if k==1:
        if by=='Total cases':
            s=s[['location','total_cases','iso_code','continent']]
            map(s,'total_cases',by,on)
        elif by=='New cases':
            s=s[['location','new_cases','iso_code','continent']]
            map(s,'new_cases',by,on)
        elif by=='Total deaths':
            s=s[['location','total_deaths','iso_code','continent']]
            map(s,'total_deaths',by,on)
        elif by=='New Deaths':
            s=s[['location','new_deaths','iso_code','continent']]
            map(s,'new_deaths',by,on)
        elif by=='Total tests':
            s=s[['location','total_tests','iso_code','continent']]
            map(s,'total_tests',by,on)
    else:
        bar_continent(s,by)
        if by=='Total cases':
            s=s[['location','total_cases','iso_code','continent']]
            map(s,'total_cases',by,on)
        elif by=='New cases':
            s=s[['location','new_cases','iso_code','continent']]
            map(s,'new_cases',by,on)
        elif by=='Total deaths':
            s=s[['location','total_deaths','iso_code','continent']]
            map(s,'total_deaths',by,on)
        elif by=='New Deaths':
            s=s[['location','new_deaths','iso_code','continent']]
            map(s,'new_deaths',by,on)
        elif by=='Total tests':
            s=s[['location','total_tests','iso_code','continent']]
            map(s,'total_tests',by,on)
def bar_continent(s,by):
    Asia=s[s['continent']=='Asia']
    Oceania=s[s['continent']=='Oceania']
    South_America=s[s['continent']=='South America']
    North_America=s[s['continent']=='North America']
    Africa=s[s['continent']=='Africa']
    plot_bar(Asia,Oceania,South_America,North_America,Africa,by)
def plot_bar(Asia,Oceania,South_America,North_America,Africa,by):
    by=by.lower()
    by=by.strip()
    by=by.replace(' ','_')
    a=np.sum(Asia[by])
    b=np.sum(Oceania[by])
    c=np.sum(Africa[by])
    d=np.sum(South_America[by])
    e=np.sum(North_America[by])
    fig = go.Figure()
    fig.add_trace(go.Bar(
    y=['Asia', 'Oceania', 'South America','North America','Africa'],
    x=[a,b,c,d,e],
    name=by,
    orientation='h',
    marker=dict(
        color='rgba(50, 171, 96, 0.6)',
        line=dict(color='rgba(50, 171, 96, 1.0)', width=3))
    ))
    st.plotly_chart(fig)
def basis_case(s,on,date):
    if on=='World':
        t=s[s['location']=='World']
        st.markdown('On this date,  {}  , in  {}  , there is a total of  {}  total cases and {}  total deaths.'.format(date,on,t.iloc[0]['total_cases'],t.iloc[0]['total_deaths']))
        st.markdown('**New cases   :-  {}'.format(t.iloc[0]['new_cases']))
        st.markdown('**New deaths  :-  {}'.format(t.iloc[0]['new_deaths']))
        find_case(s,on,0)
    else:
        st.markdown('On this date,  {}  , in  {}  , there is a total of  {}  total cases and {}  total deaths.'.format(date,on,np.sum(s['total_cases']),np.sum(s['total_deaths'])))
        st.markdown('New cases   :- {}'.format(np.sum(s['new_cases'])))
        st.markdown('New deaths  :-{}'.format(np.sum(s['new_deaths'])))
        find_case(s,on,1)
recent_date =pd.to_datetime(data['date']).max()
present=data[data['date']==recent_date.strftime('%Y-%m-%d')]
st.markdown('# <span style="color:#3D3B15 "><b>World Today</b></span>',unsafe_allow_html=True)
st.markdown('## <span style="color:#022F84 "><b> {} </b> total cases</span>'.format(int(present[present['location']=='World'].values[0][4])),unsafe_allow_html=True)
st.markdown('## <span style="color:#B10618 "><b> {} </b> total deaths</span>'.format(int(present[present['location']=='World'].values[0][6])),unsafe_allow_html=True)
st.markdown('## <span style="color:#07860E"><b> {} </b> total recovered</span>'.format(covid.get_total_recovered()),unsafe_allow_html=True)
st.markdown('## <span style="color:#73257A "><b> {} </b> total active cases</span>'.format(covid.get_total_active_cases()),unsafe_allow_html=True)
st.sidebar.markdown('## **Top 5 countries based number of confirmed cases**')
st.sidebar.table((present.sort_values('total_cases',ascending = False)[['location','total_cases']]).set_index('location').iloc[1:6,:])
st.markdown('## <span style="color:#021868">Data Explorer</span>',unsafe_allow_html=True)
st.markdown('### Metric')
date = st.date_input('Select date for the map',recent_date)
date=date.strftime('%Y-%m-%d')
s=data[data['date']==date]
on=st.selectbox('',('World', 'Asia', 'Europe', 'Africa', 'North America', 'South America', 'Oceania',))
if on=='World':
    basis_case(s,on,date)
elif on=='Asia':
    s=s[s['continent']=='Asia']
    basis_case(s,on,date)
elif on=='Europe':
    s=s[s['continent']=='Europe']
    basis_case(s,on,date)
elif on=='Africa':
    s=s[s['continent']=='Africa']
    basis_case(s,on,date)
elif on=='North America':
    s=s[s['continent']=='North America']
    basis_case(s,on,date)
elif on=='South America':
    s=s[s['continent']=='South America']
    basis_case(s,on,date)
elif on=='Oceania':
    s=s[s['continent']=='Oceania']
    basis_case(s,on,date)
c=st.sidebar.checkbox('Country wise analysis')
if c:
    option=list(data.location.unique())
    option=option[:len(option)-2]
    countrys = st.sidebar.selectbox('Select Country',option)
    country(countrys)
st.markdown("## Select below to compare two countries")
k=st.checkbox('Compare Two Countries')
if k:
    option=list(data.location.unique())
    option=option[:len(option)-2]
    country_1 = st.selectbox('Select 1st Country',option)
    country_2 = st.selectbox('Select 2nd Country',option)
    if country_1==country_2:
        st.markdown("Select 2 different countries")
    else:
        st.markdown("## Comparison between {} and {}".format(country_1,country_2))
        y1=[covid_2.get_status_by_country_name(country_1)['confirmed'],covid_2.get_status_by_country_name(country_1)  ['active'],covid_2.get_status_by_country_name(country_1)['deaths'],covid_2.get_status_by_country_name(country_1)['total_tests']]
        y2=[covid_2.get_status_by_country_name(country_1)['confirmed'],covid_2.get_status_by_country_name(country_2)['active'],covid_2.get_status_by_country_name(country_2)['deaths'],covid_2.get_status_by_country_name(country_2)['total_tests']]
        y1=np.log(y1)
        y2=np.log(y2)
        fig_l = go.Figure(data=[
        go.Bar(name=country_1, x=['confirmed','active','deaths','total tests'], y=y1),
        go.Bar(name=country_2, x=['confirmed','active','deaths','total tests'], y=y2)
        ])
        fig_l.update_layout(barmode='group')
        st.plotly_chart(fig_l)
        st.markdown('### Trend of Total Cases per million')
        d1=data.loc[data['location'] == country_1]
        d2=data.loc[data['location'] == country_2]
        y_2=d1['total_cases_per_million']
        y_3=d2['total_cases_per_million']
        d1['ndate'] = pd.to_datetime(d1['date'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d1['ndate'], y=y_2,
                    mode='lines',
                    name=country_1,fill='tonexty'))
        fig.add_trace(go.Scatter(x=d1['ndate'], y=y_3,
                    mode='lines', name=country_2,fill='tozeroy'))
        st.plotly_chart(fig)
        st.markdown('### Trend of Total Deaths per million')
        y_2=d1['total_deaths_per_million']
        y_3=d2['total_deaths_per_million']
        d1['ndate'] = pd.to_datetime(d1['date'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d1['ndate'], y=y_2,
                    mode='lines',
                    name=country_1,fill='tonexty'))
        fig.add_trace(go.Scatter(x=d1['ndate'], y=y_3,
                    mode='lines', name=country_2,fill='tozeroy'))
        st.plotly_chart(fig)
        st.markdown('### Trend of Total Tests per thousand')
        y_2=d1['total_tests_per_thousand']
        y_3=d2['total_tests_per_thousand']
        d1['ndate'] = pd.to_datetime(d1['date'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=d1['ndate'], y=y_2,
                    mode='lines',
                    name=country_1,fill='tonexty'))
        fig.add_trace(go.Scatter(x=d1['ndate'], y=y_3,
                    mode='lines', name=country_2,fill='tozeroy'))
        st.plotly_chart(fig)
About_video='''<iframe width="388" height="315" src="https://www.youtube.com/embed/mOV1aBVYKGA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'''
st.markdown('### About covid-19 by WHO')
st.markdown(About_video,unsafe_allow_html=True)
st.markdown('<a href="https://confirmsubscription.com/h/d/18DFE0FD1CC9DA69" target="_blank">Subscribe to WHO newsletter</a>',unsafe_allow_html=True)
st.write('**As different countries are at different time zones, the data may not be upto date but it is made as accurate as possible')


