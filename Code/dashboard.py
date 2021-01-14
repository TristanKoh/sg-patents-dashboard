PATH = "C:\\Users\\Tristan\\Desktop\\Computational_Law\\IP_Dashboard\\Data"

import streamlit as st

import pandas as pd
import sqlite3

# Connect and pull everything from the db
con = sqlite3.connect(PATH+"\\patents.db")
df = pd.read_sql_query("SELECT * FROM summary", con)
con.close()

# Create df for count by lodgement date
df_dates = df["lodgementDate"].value_counts().rename_axis("lodgementDate").reset_index(name = "counts")

# For count by application status
df_appstatus = df["applicationStatus"].value_counts().rename_axis("applicationStatus").reset_index(name = "counts")

# Dashboard elements
st.title("Singapore Patent Dashboard")

# Plot timeseries for number of patents filed per day
st.text("Time series of number of patents filed from 10 September 2018 to 1 September 2020")
st.vega_lite_chart(df_dates, {
    "mark" : {"type" : "line", "tooltip" : True},
    "encoding" : {
        "x" : {"field" : "lodgementDate", "type" : "temporal", "title" : "Date of lodgement", "timeUnit" : "yearmonthdate"},
        "y" : {"field" : "counts", "type" : "quantitative", "title" : "Number of filings"},
    },
    "width" : 1200,
    "height" : 200,
})


st.text("Barchart of the different types of application status")
st.vega_lite_chart(df_appstatus, {
    "mark" : {"type" : "bar", "tooltip" : True},
    "encoding" : {
        "x" : {"field" : "applicationStatus", "title" : "Application Status", "sort" : {"op" : "sum", "field" : "counts", "order" : "descending"}},
        "y" : {"field" : "counts", "aggregate" : "sum"}
    },
    "width" : 600,
    "height" : 600,
})