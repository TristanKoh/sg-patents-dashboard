PATH = "Data"

import streamlit as st
from streamlit_plotly_events import plotly_events

import pandas as pd
import numpy as np
import sqlite3
import plotly as py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import datetime as dt

# Connect and pull everything from the db
con = sqlite3.connect(PATH+"/patents.db")
df = pd.read_sql_query("SELECT * FROM summary", con)
df_ipc = pd.read_sql_query("SELECT * FROM app_ipc", con)
df_documents = pd.read_sql_query("SELECT * FROM supporting_documents", con)
df_inventors = pd.read_sql_query("SELECT * FROM inventors", con)
df_pct = pd.read_sql_query("SELECT * FROM pct_app", con)
con.close()

##st.dataframe(df.head())
##st.dataframe(df_ipc.head())

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

#######################
### Sidebar Filters ###
#######################

st.sidebar.markdown("<a href='#link_to_top'>Back to top</a>", unsafe_allow_html=True)

# Start and end date
st.sidebar.title("Date Range")
df['lodgementDate'] = pd.to_datetime(df['lodgementDate'])

earliest_date = min(df['lodgementDate']).to_pydatetime()
latest_date = max(df['lodgementDate']).to_pydatetime()
start_date = st.sidebar.date_input('Start date', earliest_date)
end_date = st.sidebar.date_input('End date', latest_date)

filtered_df = df[(df['lodgementDate'].dt.date>= start_date) & (df['lodgementDate'].dt.date<=end_date)]

# Application status
st.sidebar.title("Application Status")
statuses = filtered_df["applicationStatus"].unique().tolist()
status_chosen = st.sidebar.multiselect('Select application status', statuses, statuses)

filtered_df = filtered_df[filtered_df['applicationStatus'].isin(status_chosen)]
filtered_df_ipc = df_ipc[df_ipc['applicationNum'].isin(filtered_df['applicationNum'])]
filtered_df_documents = df_documents[df_documents['applicationNum'].isin(filtered_df['applicationNum'])]
filtered_df_inventors = df_inventors[df_inventors['applicationNum'].isin(filtered_df['applicationNum'])]
filtered_df_pct = df_pct[df_pct['applicationNum'].isin(filtered_df['applicationNum'])]

# IPC section and class
st.sidebar.title("IPC components")
ipc_sections = sorted(filtered_df_ipc['section'].unique().tolist())
section_chosen = st.sidebar.multiselect('Select IPC section', ipc_sections, ipc_sections)
ipc_classes = sorted(filtered_df_ipc[filtered_df_ipc['section'].isin(section_chosen)]['class'].unique().tolist())
class_chosen = st.sidebar.multiselect('Select IPC class', ipc_classes, ipc_classes)

filtered_df_ipc = filtered_df_ipc[filtered_df_ipc['class'].isin(ipc_classes)]
filtered_df = filtered_df[filtered_df['applicationNum'].isin(filtered_df_ipc['applicationNum'])]
filtered_df_documents = filtered_df_documents[filtered_df_documents['applicationNum'].isin(filtered_df_ipc['applicationNum'])]
filtered_df_inventors = filtered_df_inventors[filtered_df_inventors['applicationNum'].isin(filtered_df_ipc['applicationNum'])]
filtered_df_pct = filtered_df_pct[filtered_df_pct['applicationNum'].isin(filtered_df_ipc['applicationNum'])]

###################################
### Prep Data for Visualisation ###
###################################

# Create df for count by lodgement date
#df_dates = filtered_df["lodgementDate"].value_counts().rename_axis("lodgementDate").reset_index(name = "counts")
#df_dates = df_dates.sort_values('lodgementDate')
df_dates = filtered_df["lodgementDate"].value_counts()
df_dates_bymonth = df_dates.resample("MS").sum()
df_dates_bymonth = df_dates_bymonth.rename_axis("lodgementDate").reset_index(name = "counts")
df_dates_bymonth['year-month'] = df_dates_bymonth['lodgementDate'].dt.strftime('%Y-%m')
df_dates_bymonth = df_dates_bymonth.sort_values('lodgementDate')

##st.dataframe(df_dates.head())
##st.dataframe(df_dates_bymonth.head())

# For count by application status
df_appstatus = filtered_df["applicationStatus"].value_counts().rename_axis("applicationStatus").reset_index(name = "count")
df_appstatus['percentage'] = df_appstatus['count']/df_appstatus['count'].sum()
df_appstatus['x'] = 'placeholder'
#st.dataframe(df_appstatus.head())

# For count by IPC section symbol
df_ipc_section = filtered_df_ipc["section"].value_counts().rename_axis("ipcSection").reset_index(name = "counts")
##st.dataframe(df_ipc_section)

# For count by IPC class symbol
df_ipc_class = filtered_df_ipc["class"].value_counts().rename_axis("ipcClass").reset_index(name = "counts")

############################
### Chart Visualisations ###
############################

st.markdown("<div id='link_to_top'></div>", unsafe_allow_html=True)

# Dashboard elements
st.title("Singapore Patent Dashboard")

# Summary section
# ------------------------------------------------------
with st.beta_expander("Summary"):
    
    ### ROW 1 - Big number tiles for app status breakdown ###        
    st.markdown("*Barchart of the different types of application status*")
    barh = px.bar(df_appstatus, x='percentage', y='x', color='applicationStatus',
                  orientation='h', custom_data=['count'],
                  color_discrete_sequence=px.colors.qualitative.G10
                   )
    barh.update_layout(barmode='stack', xaxis_tickformat = '%',
                       xaxis_title="",
                       yaxis={'visible': False, 'showticklabels': False})
    
    barh.update_traces(hovertemplate = 'Percentage: %{x:.2%}<br>' + 'Count: %{customdata[0]}')
    st.plotly_chart(barh, use_container_width=True)

    ### ROW 2 - Time series of patent filed & percentage of pct apps ###
    col1, col2 = st.beta_columns(2)

    # Plot timeseries for number of patents filed per day
    with col1:
        st.markdown("*Time series of number of patents filed from 10 September 2018 to 1 September 2020*")
        fig1 = px.bar(df_dates_bymonth, x="lodgementDate", y="counts",
                      labels={"lodgementDate": "Date of Lodgement",
                              "counts": "Application Count"},
                      hover_name="year-month",
                      hover_data={"lodgementDate": False,
                                  "counts": True},
                      color_discrete_sequence=px.colors.qualitative.G10
                      )
        st.plotly_chart(fig1, use_container_width=True)

    # Plot bar chart for type of application status
    with col2:
        st.markdown("*Proportion of Apps with PCT Application*")
        pct_app_num = filtered_df_pct['applicationNum'].nunique()
        non_pct_app_num = filtered_df["applicationNum"].nunique() - pct_app_num
        fig2 = px.bar(x=['PCT Apps', 'Non-PCT Apps'],
                      y=[pct_app_num, non_pct_app_num],
                      color_discrete_sequence=px.colors.qualitative.G10)
        fig2.update_traces(hovertemplate = 'Count: %{y}')
        fig2.update_layout(xaxis_title="", yaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)

    ### ROW 3 - IPC analysis ###
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.markdown("*Proportion of IPC sections*")
        fig3 = px.pie(df_ipc_section, names='ipcSection', values='counts',
                       labels={
                           "ipcSection": "IPC Section",
                           "counts": "Section Count",
                        }, color_discrete_sequence=px.colors.qualitative.G10
                       )
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.markdown("*Distribution of IPC classes*")
        fig4 = px.bar(df_ipc_class, x="ipcClass", y="counts",
                      labels={
                           "ipcClass": "IPC Class",
                           "counts": "Class Count",
                        }, color_discrete_sequence=px.colors.qualitative.G10
                       )
        st.plotly_chart(fig4, use_container_width=True)

    with col3:
        st.markdown("*List of applications with selected class*")
        user_input = st.text_input("Enter IPC class in textbox e.g. H6").upper()
        selected_appNum = filtered_df_ipc[filtered_df_ipc['class'].str.contains(user_input)]['applicationNum']
        if user_input!="":
            st.dataframe(filtered_df[filtered_df['applicationNum'].isin(selected_appNum)])


# Inventors' backgroun section
# ------------------------------------------------------

with st.beta_expander("Where are the Inventors from?"):
    # ROW 3
    # Create 2 dfs. Group apps by inventor, and inventors by country.
    inventor_apps = filtered_df_inventors.groupby(['country', 'name'])\
                           .agg({'applicationNum': lambda x: ', '.join(x)}).reset_index()
    inventor_apps.columns = ['Country', 'Inventor Name', 'Applications']
    inventor_per_country = inventor_apps['Country'].value_counts().reset_index()
    inventor_per_country.columns = ['Country', 'count']

    # Params for choropleth map
    data = dict (
        type = 'choropleth',
        locations = inventor_per_country['Country'],
        locationmode='country names',
        colorscale = 'PuBu',
        zmin = 0, zmax = inventor_per_country.quantile(0.95)[0], # 95th percentile, remove outlier USA ~14k
        # marker_line_color='darkgray',
        marker_line_width=0.5,
        z = inventor_per_country['count'])
    global_map = go.Figure(data=[data])
    global_map.update_geos(resolution=50, showcountries=True, countrycolor="#999999",
                           landcolor="#e3e3e3", showcoastlines=False)
    global_map.update_layout(margin={"r":0,"t":0,"l":0,"b":2})

    # plotly_events allow for callback from user input
    st.subheader("World Map by Inventor Count")
    selected_point = plotly_events(global_map, key="click", click_event=True, hover_event=False)
    placeholder_header = st.empty()
    placeholder_df = st.empty()

    if len(selected_point)>0:
        selected_country = inventor_per_country['Country'][selected_point[0]['pointIndex']]
        
        cols = ['Inventor Name', 'Applications']
        selected_inventors = inventor_apps[inventor_apps['Country']== selected_country][cols]
        placeholder_header.subheader(f"List of Inventors from {selected_country}")
        placeholder_df.dataframe(selected_inventors.sort_values('Inventor Name').reset_index(drop=True))



# Search feature section
# ------------------------------------------------------
with st.beta_expander("Search Application by Title"):
    # ROW 4
    user_input = st.text_input("Enter keyword e.g. Treatment")
    cols = ['applicationNum', 'titleOfInvention', 'lodgementDate']
    # Filter only abstract document type
    df_abstract = filtered_df_documents[filtered_df_documents['description'].str.lower()=="abstract"]
    # Select most updated abstract for each application
    df_abstract = df_abstract.sort_values('documentLodgementDate', ascending=False)
    df_abstract = df_abstract.groupby('applicationNum').agg({'titleOfInvention': "first",
                                                             'documentLodgementDate': "first",
                                                             'url' : "first"}).reset_index()
    # Obtain user search keyword
    df_abstract = df_abstract[df_abstract['titleOfInvention'].str.upper().str.contains(user_input.upper())]
    # Change url to clickable
    ## def make_clickable(url, text):
    ##     return f'<a target="_blank" href="{url}">{text}</a>'
    ## df_abstract['titleOfInvention'] = df_abstract.apply(lambda row: make_clickable(row['url'], row['titleOfInvention']), axis=1)

    # Join with summary to obtain lodgement date
    df_abstract = df_abstract.join(filtered_df[['applicationNum', 'lodgementDate']].set_index('applicationNum'),
                                   how='left', on='applicationNum')

    # Display
    if (user_input!=""):
        if len(df_abstract)>0:
            st.subheader("List of applications with selected keyword")
            st.write("<i>For more app details, search app number on\
                     <a href='https://ip2sg.ipos.gov.sg/RPS/WP/CM/SearchSimple/IP.aspx?SearchCategory=PT' target='_blank'>this website</a></i>",
                     unsafe_allow_html=True)
            ## st.write("*Click on title to view abstract.*")
            st.write(df_abstract[cols].to_html(escape=False), unsafe_allow_html=True)
        else:
            st.write("No application with keyword **", user_input, "** in title.")

st.markdown("<br><p style='text-align:right;'><a href='#link_to_top'>Back to top</a></p>", unsafe_allow_html=True)
