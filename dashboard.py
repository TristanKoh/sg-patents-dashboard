PATH = "Data"

import streamlit as st

import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import datetime as dt

# Connect and pull everything from the db
con = sqlite3.connect(PATH+"/patents.db")
df = pd.read_sql_query("SELECT * FROM summary", con)
df_ipc = pd.read_sql_query("SELECT * FROM app_ipc", con)
con.close()

##st.dataframe(df.head())
##st.dataframe(df_ipc.head())

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

#######################
### Sidebar Filters ###
#######################

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

# IPC section and class
st.sidebar.title("IPC components")
ipc_sections = sorted(filtered_df_ipc['section'].unique().tolist())
section_chosen = st.sidebar.multiselect('Select IPC section', ipc_sections, ipc_sections)
ipc_classes = sorted(filtered_df_ipc[filtered_df_ipc['section'].isin(section_chosen)]['class'].unique().tolist())
class_chosen = st.sidebar.multiselect('Select IPC class', ipc_classes, ipc_classes)

filtered_df_ipc = filtered_df_ipc[filtered_df_ipc['class'].isin(ipc_classes)]
filtered_df = filtered_df[filtered_df['applicationNum'].isin(filtered_df_ipc['applicationNum'])]

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
df_appstatus = filtered_df["applicationStatus"].value_counts().rename_axis("applicationStatus").reset_index(name = "counts")
##st.dataframe(df_appstatus.head())

# For count by IPC section symbol
df_ipc_section = filtered_df_ipc["section"].value_counts().rename_axis("ipcSection").reset_index(name = "counts")
##st.dataframe(df_ipc_section)

# For count by IPC class symbol
df_ipc_class = filtered_df_ipc["class"].value_counts().rename_axis("ipcClass").reset_index(name = "counts")


############################
### Chart Visualisations ###
############################

# Dashboard elements
st.title("Singapore Patent Dashboard")

# ROW 1
col1, col2 = st.beta_columns(2)

# Plot timeseries for number of patents filed per day
with col1:
    st.markdown("*Time series of number of patents filed from 10 September 2018 to 1 September 2020*")
    fig1 = px.bar(df_dates_bymonth, x="lodgementDate", y="counts",
                  labels={"lodgementDate": "Date of Lodgement",
                          "counts": "Application Count"},
                  hover_name="year-month",
                  hover_data={"lodgementDate": False,
                              "counts": True}
                  )
    st.plotly_chart(fig1, use_container_width=True)

# Plot bar chart for type of application status
with col2:
    st.markdown("*Barchart of the different types of application status*")
    fig2 = px.bar(df_appstatus, x="applicationStatus", y="counts",
                  labels={
                       "applicationStatus": "Application Status",
                       "counts": "Application Count",
                    }
                   )
    st.plotly_chart(fig2, use_container_width=True)

# ROW 2
col1, col2, col3 = st.beta_columns(3)

with col1:
    st.markdown("*Proportion of IPC sections*")
    fig3 = px.pie(df_ipc_section, names='ipcSection', values='counts',
                   labels={
                       "ipcSection": "IPC Section",
                       "counts": "Section Count",
                    }
                   )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("*Distribution of IPC classes*")
    fig4 = px.bar(df_ipc_class, x="ipcClass", y="counts",
                  labels={
                       "ipcClass": "IPC Class",
                       "counts": "Class Count",
                    }
                   )
    st.plotly_chart(fig4, use_container_width=True)

with col3:
    st.markdown("*List of applications with selected class*")
    user_input = st.text_input("Enter IPC class in textbox e.g. H6").upper()
    selected_appNum = filtered_df_ipc[filtered_df_ipc['class'].str.contains(user_input)]['applicationNum']
    if user_input!="":
        st.dataframe(filtered_df[filtered_df['applicationNum'].isin(selected_appNum)])

### Plot timeseries for number of patents filed per day
##st.text("Time series of number of patents filed from 10 September 2018 to 1 September 2020")
##st.vega_lite_chart(df_dates, {
##    "mark" : {"type" : "line", "tooltip" : True},
##    "encoding" : {
##        "x" : {"field" : "lodgementDate", "type" : "temporal", "title" : "Date of lodgement", "timeUnit" : "yearmonthdate"},
##        "y" : {"field" : "counts", "type" : "quantitative", "title" : "Number of filings"},
##    },
##    "width" : 1200,
##    "height" : 200,
##})
##
##
##st.text("Barchart of the different types of application status")
##st.vega_lite_chart(df_appstatus, {
##    "mark" : {"type" : "bar", "tooltip" : True},
##    "encoding" : {
##        "x" : {"field" : "applicationStatus", "title" : "Application Status", "sort" : {"op" : "sum", "field" : "counts", "order" : "descending"}},
##        "y" : {"field" : "counts", "aggregate" : "sum"}
##    },
##    "width" : 600,
##    "height" : 600,
##})
