from google.protobuf.symbol_database import Default
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import matplotlib as plt
from streamlit.type_util import data_frame_to_bytes
import xlrd
import math
import re
import seaborn as sns
import matplotlib.pyplot as plt



st.set_page_config(page_title="Deployment Test",
                   page_icon= ":dash:",
                   layout = "wide")
Renesas_combined_cleaned = pd.read_excel("RA_family_combined.xlsx")

st.dataframe(Renesas_combined_cleaned)



#---- HIDE STREAMLIT STYLE   -------#

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)