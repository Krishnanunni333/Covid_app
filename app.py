import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date, timedelta
from datetime import datetime
import time
import plotly.graph_objects as go
from covid import Covid
from PIL import Image
import requests
from io import BytesIO
import pycountry
covid = Covid()
covid_2 = Covid(source="worldometers")
response = requests.get('https://phil.cdc.gov//PHIL_Images/23312/23312_lores.jpg')
img = Image.open(BytesIO(response.content))
img=img.convert('RGB')
newsize = (300, 200) 
img = img.resize(newsize)
st.image(img)
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
    data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')
    return data
data=load_data()
def total_cases_total_deaths(d):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d['ndate'], y=np.log(d['total_cases']),
                    mode='lines',
                    name='Total cases',fill='tonexty'))
    fig.add_trace(go.Scatter(x=d['ndate'], y=np.log(d['total_deaths']),
                    mode='lines', name='Total Deaths',fill='tozeroy'))
    st.plotly_chart(fig)
def new_cases_new_deaths(d):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d['ndate'], y=np.log(d['new_cases']),
                    mode='lines',
                    name='New cases',fill='tonexty'))
    fig.add_trace(go.Scatter(x=d['ndate'], y=np.log(d['new_deaths']),
                    mode='lines', name='New Deaths',fill='tozeroy'))
    st.plotly_chart(fig)
def new_test(d):
    y_3=d['new_tests']
    if np.sum(y_3)==0:
        st.markdown('<i>No data is available on new testing for {} .</i>'.format(countrys),unsafe_allow_html=True)
    else:
        fig = px.bar(d, x='date', y='new_tests')
        st.plotly_chart(fig)
def country_details(t):
    ind=t['iso_code'].values[1].strip("''").lower()
    response = requests.get('https://raw.githubusercontent.com/adamoliver/Country-Flags-ISO-3/master/gif/{}.gif'.format(ind))
    img = Image.open(BytesIO(response.content))
    img=img.convert('RGB')
    newsize = (40, 20) 
    img = img.resize(newsize)
    st.image(img)
    st.markdown('**_All data as of_** : {}'.format(recent_date.strftime('%Y-%m-%d')))
    st.markdown('**Covid-19 Death rate** : {}'.format('Information not available or the country has no deaths yet.' if np.max(t['cvd_death_rate'].dropna()) is np.nan else np.max(t['cvd_death_rate'].dropna())))
    st.markdown('**Cumilative cases** : {}'.format('Information not available or the country has no cases yet.' if np.max(t['total_cases'].dropna()) is np.nan else np.max(t['total_cases'].dropna())))
    st.markdown('**Cumilative deaths** : {}'.format('Information not available or the country has no deaths yet.' if np.max(t['total_deaths'].dropna()) is np.nan else np.max(t['total_deaths'].dropna())))
    st.markdown('**Cumilative Tests** : {}'.format('Information not available.' if np.max(t['total_tests'].dropna()) is np.nan else np.max(t['total_tests'].dropna())))
    st.markdown('**New Cases** : {}'.format('Information not available.' if np.sum(t['new_cases'].dropna()) is np.nan else np.array(t['new_cases'].dropna())[-1]))
    st.markdown('**New Deaths** : {}'.format('Information not available.' if np.sum(t['new_deaths'].dropna()) is np.nan else np.array(t['new_deaths'].dropna())[-1]))
    st.markdown('**Total test Units** : {}'.format('Information not available.' if np.max(t['tests_units'].dropna()) is np.nan else np.max(t['tests_units'].dropna())))
    st.markdown('**Stringency index** : {}'.format('Information not available.' if np.max(t['stringency_index'].dropna()) is np.nan else np.max(t['stringency_index'].dropna())))
    st.markdown('**Handwashing facilities** : {}'.format('Information not available.' if np.max(t['handwashing_facilities'].dropna()) is np.nan else np.max(t['handwashing_facilities'].dropna())))
    st.markdown('**Hospital beds per thousand** : {}'.format('Information not available.' if np.max(t['hospital_beds_per_thousand'].dropna()) is np.nan else np.max(t['hospital_beds_per_thousand'].dropna())))
    st.markdown('**Life expectancy** : {}'.format('Information not available.' if np.max(t['life_expectancy'].dropna()) is np.nan else np.max(t['life_expectancy'].dropna())))
    st.markdown('**GDP per Capita** : {}'.format('Information not available.' if np.max(t['gdp_per_capita'].dropna()) is np.nan else np.max(t['gdp_per_capita'].dropna())))
    st.markdown('**Population** : {}'.format('Information not available.' if np.max(t['population'].dropna()) is np.nan else np.max(t['population'].dropna())))
    st.markdown('**Population density** : {}'.format('Information not available.' if np.max(t['population_density'].dropna()) is np.nan else np.max(t['population_density'].dropna())))
    st.markdown('**Median Age** : {}'.format('Information not available.' if np.max(t['median_age'].dropna()) is np.nan else np.max(t['median_age'].dropna())))
    st.markdown('**Diabetes prevalence** : {}'.format('Information not available.' if np.max(t['diabetes_prevalence'].dropna()) is np.nan else np.max(t['diabetes_prevalence'].dropna())))
    st.markdown('**Female smokers** : {}'.format('Information not available.' if np.max(t['female_smokers'].dropna()) is np.nan else np.max(t['female_smokers'].dropna())))
    st.markdown('**Male smokers** : {}'.format('Information not available.' if np.max(t['male_smokers'].dropna()) is np.nan else np.max(t['male_smokers'].dropna())))
    st.markdown('**Aged 65 older** : {}'.format('Information not available.' if np.max(t['aged_65_older'].dropna()) is np.nan else np.max(t['aged_65_older'].dropna())))
    st.markdown('**Aged 70 older** : {}'.format('Information not available.' if np.max(t['aged_70_older'].dropna()) is np.nan else np.max(t['aged_70_older'].dropna())))
    st.markdown('**Extreme poverty** : {}'.format('Information not available.' if np.max(t['extreme_poverty'].dropna()) is np.nan else np.max(t['extreme_poverty'].dropna())))
def country(countrys):
    d=data[data['location']==countrys]
    st.subheader('Country wise analysis')
    st.markdown('## <span style="color:#782612  ">{}</span> '.format(countrys),unsafe_allow_html=True)
    #recent_date =pd.to_datetime(d['date']).max()
    start_date = st.date_input('Start date',datetime.strptime('2019-12-31', '%Y-%m-%d').date())
    end_date= st.date_input('End date',recent_date)
    d['ndate'] = pd.to_datetime(d['date'])
    d=d[d['ndate'] >= pd.to_datetime(start_date)]
    d=d[d['ndate'] <= pd.to_datetime(end_date)]
    country_details(d)
    st.markdown(' #### Comparison between total cases and total deaths of {} from {} to {}  '.format(countrys,start_date,end_date))
    total_cases_total_deaths(d)
    st.markdown(' #### Comparison between new cases and new deaths of {} from {} to {}  '.format(countrys,start_date,end_date))
    new_cases_new_deaths(d)
    st.markdown(' #### Trend of new tests performed in {}  from {} to {}'.format(countrys,start_date,end_date))
    new_test(d)
    
    if st.checkbox("Show raw data", False):
        st.subheader("Raw data of {} from {} to {}".format(countrys,start_date,end_date))
        st.dataframe(d.fillna('Not available'))
def map(s,t,by,on,p):
    st.markdown(' * The value while hovering over the countries are log values of actual numbers. This is to get an accurate and understandable separation from all the countries.')
    if pd.isnull(s[t]).all():
        st.write('No data updated now on it, you can try with previous dates.')
    else:
        k=np.log(s[t])
        options = ("orthographic","equirectangular")
        a = st.empty()
        value = a.radio("Select view", options, 1)
        fig = go.Figure(data=go.Choropleth(
        locations = s['iso_code'],
        z = k,
        text = s['location'],
        colorscale = 'Picnic',
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
        if p==0:
            bar_continent(s,by)
def find_case(s,on,k):
    by=st.selectbox('Based on',('Total cases', 'New cases','Total deaths','New Deaths','Total tests'))
    if by=='Total cases':
        s=s[['location','total_cases','iso_code','continent']]
        map(s,'total_cases',by,on,k)
    elif by=='New cases':
        s=s[['location','new_cases','iso_code','continent']]
        map(s,'new_cases',by,on,k)
    elif by=='Total deaths':
        s=s[['location','total_deaths','iso_code','continent']]
        map(s,'total_deaths',by,on,k)
    elif by=='New Deaths':
        s=s[['location','new_deaths','iso_code','continent']]
        map(s,'new_deaths',by,on,k)
    elif by=='Total tests':
        s=s[['location','total_tests','iso_code','continent']]
        map(s,'total_tests',by,on,k)
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
    fig.update_layout(title_text='Based on {}'.format(by.replace('_',' ')))
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
yesterday = date.today() - timedelta(days=1)
current_time = time.localtime()
current_time = time.strftime("%H:%M:%S", current_time)
if datetime.strptime(current_time, '%H:%M:%S').time()>=datetime.strptime('15:00:00', '%H:%M:%S').time():
    recent_date =pd.to_datetime(data['date']).max()
else:
    recent_date =date.today() - timedelta(days=1)
def daily():
    st.markdown('# <span style="color:#3D3B15 "><b>World Today</b></span>',unsafe_allow_html=True)
    st.markdown('## <span style="color:#022F84 "><b> {} </b> total cases</span>'.format(covid.get_total_confirmed_cases()),unsafe_allow_html=True)
    st.markdown('## <span style="color:#B10618 "><b> {} </b> total deaths</span>'.format(covid.get_total_deaths()),unsafe_allow_html=True)
    st.markdown('## <span style="color:#07860E"><b> {} </b> total recovered</span>'.format(covid.get_total_recovered()),unsafe_allow_html=True)
    st.markdown('## <span style="color:#73257A "><b> {} </b> total active cases</span>'.format(covid.get_total_active_cases()),unsafe_allow_html=True)
    st.sidebar.markdown('# <span style="color:#3D3B15 "><b>Top 5 Countries</b></span>',unsafe_allow_html=True)
    present=data[data['date']==recent_date.strftime('%Y-%m-%d')].sort_values('total_cases',ascending = False)
    present=present.iloc[1:6]
    present=present[['location','total_cases']]
    fig = go.Figure(data=[go.Table(
    header=dict(
    values=["<b>Country</b>", "<b>Total cases</b>"],
    line_color='darkslategray', fill_color='royalblue',
    align='center', font=dict(color='white', size=15)
    ),
    cells=dict(
    values=[present.location, present.total_cases],
    line_color='darkslategray', fill_color='lightcyan',
    align='center', font=dict(color='black', size=14)
    ))
    ])
    fig.update_layout(width=350, height=400,title="On total cases")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    st.sidebar.plotly_chart(fig)
    
    present=data[data['date']==recent_date.strftime('%Y-%m-%d')].sort_values('total_deaths',ascending = False)
    present=present.iloc[1:6]
    present=present[['location','total_deaths']]
    fig = go.Figure(data=[go.Table(
    header=dict(
    values=["<b>Country</b>", "<b>Total deaths</b>"],
    line_color='darkslategray', fill_color='royalblue',
    align='center', font=dict(color='white', size=15)
    ),
    cells=dict(
    values=[present.location, present.total_deaths],
    line_color='darkslategray', fill_color='lightcyan',
    align='center', font=dict(color='black', size=14)
    ))
    ])
    fig.update_layout(width=350, height=400,title="On total deaths")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    st.sidebar.plotly_chart(fig)
daily()
def compare_country(country_1,country_2):
    st.markdown("## Comparison between {} and {}".format(country_1,country_2))
    d1=data.loc[data['location'] == country_1]
    d2=data.loc[data['location'] == country_2]
    d1['ndate'] = pd.to_datetime(d1['date'])
    d2['ndate'] = pd.to_datetime(d2['date'])
    y1=[np.max(d1['total_cases'].dropna()),np.max(d1['total_deaths'].dropna()),np.max(d1['total_tests'].dropna())]
    y2=[np.max(d2['total_cases'].dropna()),np.max(d2['total_deaths'].dropna()),np.max(d2['total_tests'].dropna())]
    y1=np.log(y1)
    y2=np.log(y2)
    fig_l = go.Figure(data=[
    go.Bar(name=country_1, x=['Total cases','Total deaths','Total tests'], y=y1),
    go.Bar(name=country_2, x=['Total cases','Total deaths','Total tests'], y=y2)
     ])
    fig_l.update_layout(barmode='group')
    st.plotly_chart(fig_l)
    st.markdown('### Trend of New Cases')
    y_2=d1['new_cases']
    y_3=d2['new_cases']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d1['ndate'], y=np.log(y_2),
                    mode='lines',
                    name=country_1,fill='tonexty'))
    fig.add_trace(go.Scatter(x=d2['ndate'], y=np.log(y_3),
                    mode='lines', name=country_2,fill='tozeroy'))
    st.plotly_chart(fig)
    st.markdown('### Trend of New Deaths')
    y_2=d1['new_deaths']
    y_3=d2['new_deaths']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d1['ndate'], y=np.log(y_2),
                    mode='lines',
                    name=country_1,fill='tonexty'))
    fig.add_trace(go.Scatter(x=d2['ndate'], y=np.log(y_3),
                    mode='lines', name=country_2,fill='tozeroy'))
    st.plotly_chart(fig)
    st.markdown('### Trend of New Tests')
    y_2=d1['new_tests']
    y_3=d2['new_tests']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d1['ndate'], y=np.log(y_2),
                    mode='lines',
                    name=country_1,fill='tonexty'))
    fig.add_trace(go.Scatter(x=d2['ndate'], y=np.log(y_3),
                    mode='lines', name=country_2,fill='tozeroy'))
    st.plotly_chart(fig)
    st.markdown('### Trend of Total Cases per million')
    y_2=d1['total_cases_per_million']
    y_3=d2['total_cases_per_million']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d1['ndate'], y=np.log(y_2),
                    mode='lines',
                    name=country_1,fill='tonexty'))
    fig.add_trace(go.Scatter(x=d2['ndate'], y=np.log(y_3),
                    mode='lines', name=country_2,fill='tozeroy'))
    st.plotly_chart(fig)
    st.markdown('### Trend of Total Deaths per million')
    y_2=d1['total_deaths_per_million']
    y_3=d2['total_deaths_per_million']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d1['ndate'], y=np.log(y_2),
                    mode='lines',
                    name=country_1,fill='tonexty'))
    fig.add_trace(go.Scatter(x=d2['ndate'], y=np.log(y_3),
                    mode='lines', name=country_2,fill='tozeroy'))
    st.plotly_chart(fig)
    st.markdown('### Trend of Total Tests per thousand')
    y_2=d1['total_tests_per_thousand']
    y_3=d2['total_tests_per_thousand']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d1['ndate'], y=np.log(y_2),
                    mode='lines',
                    name=country_1,fill='tonexty'))
    fig.add_trace(go.Scatter(x=d2['ndate'], y=np.log(y_3),
                    mode='lines', name=country_2,fill='tozeroy'))
    st.plotly_chart(fig)
st.markdown('# Global Analysis')
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
st.markdown('# Country Analysis')
st.markdown('#### Check below for analysing a country')
c=st.checkbox('Country wise analysis')
if c:
    option=list(data.location.unique())
    option=option[:len(option)-2]
    countrys = st.selectbox('Select Country',option)
    country(countrys)
st.markdown('#### Check below for comparing two countries')
k=st.checkbox('Compare Two Countries')
if k:
    option=list(data.location.unique())
    option=option[:len(option)-2]
    country_1 = st.selectbox('Select 1st Country',option)
    country_2 = st.selectbox('Select 2nd Country',option)
    if country_1==country_2:
        st.markdown("Select 2 different countries!!!")
    else:
        compare_country(country_1,country_2)
def clinics():
    return pd.read_csv('SearchResults (1).csv')
clinic=clinics()
st.markdown("# Recent top 10 details of clinical trials and medicines.")
st.text("This data is updated once in a week")
fig = go.Figure(data=[go.Table(
    header=dict(
    values=["<b>Rank</b>", "<b>Title</b>","<b>Status</b>", "<b>Study Results</b>","<b>Conditions</b>", "<b>Interventions</b>","<b>Locations</b>",],
    line_color='darkslategray', fill_color='royalblue',
    align='center', font=dict(color='white', size=11)
    ),
    cells=dict(
    values=[clinic.Rank, clinic.Title,clinic.Status, clinic['Study Results'],clinic.Conditions, clinic.Interventions,clinic.Locations, ],
    line_color='darkslategray', fill_color='lightcyan',
    align='center', font=dict(color='black', size=10)
    ))
    ])
fig.update_layout(width=800, height=600,title="Clinical details")
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig)
html='''#### <span style="color:red">Why is data on testing important?</span>
No country knows the total number of people infected with COVID-19. All we know is the infection status of those who have been tested. All those who have a lab-confirmed infection are counted as confirmed cases.

This means that the counts of confirmed cases depend on how much a country actually tests. Without testing there is no data.

Testing is our window onto the pandemic and how it is spreading. Without data on who is infected by the virus we have no way of understanding the pandemic. Without this data we can not know which countries are doing well, and which are just underreporting cases and deaths.

To interpret any data on confirmed cases we need to know how much testing for COVID-19 the country actually does.'''
About_text='''Coronaviruses (CoV) are a large family of viruses that cause illness ranging from the common cold to more severe diseases such as Middle East Respiratory Syndrome (MERS-CoV) and Severe Acute Respiratory Syndrome (SARS-CoV). A novel coronavirus (nCoV) is a new strain that has not been previously identified in humans.

Coronaviruses are zoonotic, meaning they are transmitted between animals and people. Detailed investigations found that SARS-CoV was transmitted from civet cats to humans and MERS-CoV from dromedary camels to humans. Several known coronaviruses are circulating in animals that have not yet infected humans.

Common signs of infection include respiratory symptoms, fever, cough, shortness of breath and breathing difficulties. In more severe cases, infection can cause pneumonia, severe acute respiratory syndrome, kidney failure and even death.

Standard recommendations to prevent infection spread include regular hand washing, covering mouth and nose when coughing and sneezing, thoroughly cooking meat and eggs. Avoid close contact with anyone showing symptoms of respiratory illness such as coughing and sneezing.'''
st.markdown(html, unsafe_allow_html=True)
About_video='''<iframe width="388" height="315" src="https://www.youtube.com/embed/mOV1aBVYKGA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'''
st.markdown('## About covid-19 by WHO')
st.markdown(About_text,unsafe_allow_html=True)
st.markdown('### Covid-19: video by WHO')
st.markdown(About_video,unsafe_allow_html=True)
st.markdown('Subscribe for newsletter from WHO')
st.markdown('<a href="https://confirmsubscription.com/h/d/18DFE0FD1CC9DA69" target="_blank">Subscribe to WHO newsletter</a>',unsafe_allow_html=True)
st.write('**As different countries are at different time zones, the data may not be upto date but it is made as accurate as possible')



