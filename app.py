
from google.protobuf.symbol_database import Default
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from streamlit.type_util import data_frame_to_bytes
from similarity_index import similarity_index



st.set_page_config(page_title="Renesas Cross-reference Guide",
                   page_icon= ":dash:",
                   layout = "wide")




#@st.cache(allow_output_mutation=True)
@st.cache_data
def get_data_from_excel():

    Combined_cleaned = pd.read_excel(r"Cross_referece_guide_Referral.xlsx",sheet_name= "Combined_cleaned_all_parts")
    Frequency_scaling = pd.read_excel(r"Cross_referece_guide_Referral.xlsx",sheet_name= "Frequency")
    Package_info_ST = pd.read_excel(r"Cross_referece_guide_Referral.xlsx",sheet_name= "Packaging_ST",index_col=0)
    Package_info_NXP = pd.read_excel(r"Cross_referece_guide_Referral.xlsx",sheet_name= "Packaging_NXP",index_col=0)
    Core_comparison=pd.read_excel(r"Cross_referece_guide_Referral.xlsx",sheet_name= "Core_comparison",index_col=0)
    mapping_df = pd.read_excel(r"Cross_referece_guide_Referral.xlsx", sheet_name="Hyperlink")
  


    Renesas_combined_cores= Combined_cleaned[Combined_cleaned["Company"] == "Renesas"]
    Processor= Frequency_scaling["Processor"].tolist()
    Processor_multiplier = Frequency_scaling["Scaled to M4"].tolist()
    Processor_multiplier = [round(num, 2) for num in Processor_multiplier]
    
    
    for i in range (len(Processor)):    
        index = list(Combined_cleaned[Combined_cleaned["Core"] == Processor[i]].index)
        Combined_cleaned.loc[index,"Frequency Scaled"] = Combined_cleaned.loc[index,"Operating Frequency (MHz)"]*Processor_multiplier[i]


    Renesas_combined_cores= Combined_cleaned[Combined_cleaned["Company"] == "Renesas"]
    return Combined_cleaned,Renesas_combined_cores,Package_info_ST,Package_info_NXP,Core_comparison,mapping_df

Combined_cleaned,Renesas_combined_cores,Package_info_ST,Package_info_NXP,Core_comparison,mapping_df = get_data_from_excel()



#------------- Algorithm -------------------#





# Function to hyperlink Group names based on mapping
def hyperlink_group_name(group):
    link = group_link_mapping.get(group)
    if link:
        return f'<a href="{link}" target="_blank">{group}</a>'
    return group
#------- SIDEBAR    --------#
st.sidebar.header("Choose Part Number:")

# Using object notation
company = st.sidebar.selectbox(
    "Company",
    ("STM", "NXP"),
    index = None
)
device = st.sidebar.selectbox(
    "Group",
    (Combined_cleaned[Combined_cleaned["Company"] == company]["Group"].unique()),
    index = None
)
alpha = list(Combined_cleaned[(Combined_cleaned["Company"] == company) &
                      (Combined_cleaned["Group"] == device)]["Pkg. Type"].unique())

pkg_type = st.sidebar.multiselect(
    'Package Type',
    alpha,alpha)
if len(pkg_type) == 0: 
    st.error('Please make your selection from the sidebar to view results', icon="🚨")
    st.stop()

part_number = st.sidebar.selectbox(
    "Part Number",
    (Combined_cleaned[(Combined_cleaned["Company"] == company) & 
                      (Combined_cleaned["Group"] == device) &
                     (Combined_cleaned["Pkg. Type"].isin(pkg_type))]["Part Number"].unique())
)


def create_slider(label, feature_name, dataframe, step=1):
    if feature_name not in dataframe.columns:
        raise ValueError(f"Column '{feature_name}' not found in dataframe.")
    return st.slider(label, 0, int(dataframe[feature_name].max()), 
                     (0, int(dataframe[feature_name].max())), step=step)

def filter_dataframe(dataframe, feature_name, slider_values):
    return dataframe[(dataframe[feature_name] >= slider_values[0]) & (dataframe[feature_name] <= slider_values[1])]

with st.sidebar.expander("Filter Renesas Parts:"):
    features = {
        'Operating Frequency (MHz)': {'label': 'Operating Frequency (MHz)', 'step': 5},
        'RAM Size (kB)': {'label': 'RAM Size (kB)', 'step': 5},
        'Flash Size (kB) (Prog)': {'label': 'Flash Size (kB)', 'step': 5},
        'Lead Count (#)': {'label': 'Lead Count (#)', 'step': 5},
        'CAN (ch)': {'label': 'CAN (ch)'},
        'CAN-FD (ch)': {'label': 'CAN-FD (ch)'},
        'I2C (ch)': {'label': 'I2C (ch)'},
        'I3C (ch)': {'label': 'I3C (ch)'},
        'Audio I/F': {'label': 'Audio I/F'},
        'USBHS (ch)': {'label': 'USBHS (ch)'},
        'USBFS (ch)': {'label': 'USBFS (ch)'},
        'Ethernet (ch)': {'label': 'Ethernet (ch)'},
        'Graphic LCD': {'label': 'Graphic LCD'},
        'Segment LCD': {'label': 'Segment LCD'},
        'Camera I/F': {'label': 'Camera I/F'},
        'SCI (ch)': {'label': 'SCI (ch)'}
    }
   
    
    sliders = {feature: create_slider(details['label'], feature, Renesas_combined_cores, details.get('step', 1)) for feature, details in features.items()}
    
Renesas_combined_cores_filtered = Renesas_combined_cores.copy()

for feature, slider_values in sliders.items():
    Renesas_combined_cores_filtered = filter_dataframe(Renesas_combined_cores_filtered, feature, slider_values)






if Renesas_combined_cores_filtered.empty:
    new_combined_cores = Renesas_combined_cores_filtered
    new_combined_cores["Similarity_Index"] = ""
    #st.write("The chosen filter resulted in empty Renesas dataframe")
 
else:
    new_combined_cores= similarity_index(Combined_cleaned,Package_info_ST,Package_info_NXP,Renesas_combined_cores_filtered,part_number,Core_comparison)




#------- MAINPAGE -----------------

col1, col2 = st.columns([4,1])

with col1:
    st.title("Renesas RA family Cross-Reference Guide")
    
with col2:
   st.image("RA_white.png")


#['CAN (ch)','CAN-FD (ch)','I2C (ch)','I3C (ch)','SSI (ch)','USBHS (ch)','USBFS (ch)','Ethernet (ch)','Graphic LCD','Segment LCD','Camera Interface','SCI (ch)']

cleaned_columns_Renesas = ["Part Number","Operating Frequency (MHz)","Flash Size (kB) (Prog)","RAM Size (kB)","Core","Lead Count (#)","Pkg. Type","Group",'CAN (ch)','CAN-FD (ch)','I2C (ch)','I3C (ch)','Audio I/F','USBHS (ch)','USBFS (ch)','Ethernet (ch)','Graphic LCD','Segment LCD','Camera I/F','SCI (ch)',"Similarity_Index"]
cleaned_columns_STM = ["Part Number","Operating Frequency (MHz)","Flash Size (kB) (Prog)","RAM Size (kB)","Core","Lead Count (#)","Pkg. Type","Group",'CAN (ch)','CAN-FD (ch)','I2C (ch)','I3C (ch)','Audio I/F','USBHS (ch)','USBFS (ch)','Ethernet (ch)','Graphic LCD','Segment LCD','Camera I/F','UART (ch)']
cleaned_columns_NXP = ["Part Number","Operating Frequency (MHz)","Flash Size (kB) (Prog)","RAM Size (kB)","Core","Lead Count (#)","Pkg. Type","Group",'CAN (ch)','CAN-FD (ch)','I2C (ch)','I3C (ch)','Audio I/F','USBHS (ch)','USBFS (ch)','Ethernet (ch)','Graphic LCD','Segment LCD','Camera I/F','Flex Comms.',"FlexIO"]

st.subheader("Selected competitor part")

if company== "STM":
    st.dataframe(Combined_cleaned[Combined_cleaned["Part Number"]== part_number ][cleaned_columns_STM],hide_index=1)
else:
    st.dataframe(Combined_cleaned[Combined_cleaned["Part Number"]== part_number ][cleaned_columns_NXP],hide_index=1)
    
col1, col2 = st.columns([4,1])
with col1:
    st.subheader("Renesas parts arranged from most similar to competitor part")
    
with col2:
   expand = st.checkbox('Expand table')

if expand:
    st.dataframe(new_combined_cores[cleaned_columns_Renesas].head(20),use_container_width=True,hide_index=1)
    #df = new_combined_cores[cleaned_columns_Renesas].head(20)
    #group_link_mapping = dict(zip(mapping_df['Group'], mapping_df['Links']))
    #df['Group'] = df['Group'].apply(hyperlink_group_name)
    #st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    #st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    #df = new_combined_cores[cleaned_columns_Renesas].head(5)
    #group_link_mapping = dict(zip(mapping_df['Group'], mapping_df['Links']))
    #df['Group'] = df['Group'].apply(hyperlink_group_name)
    #st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    
    
    #st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    st.dataframe(new_combined_cores[cleaned_columns_Renesas].head(5),use_container_width=True,hide_index=1)
    




st.subheader("Tool explanation")
st.markdown(':small_blue_diamond: The cross reference guide is a tool to quickly help you find a Renesas part that is the most similar to the chosen STM/NXP part.')
st.markdown(':small_blue_diamond: From the sidebar, you select the desired STM/NXP part number. The similarity index then compares the chosen competitor parts features (frequency, flash/RAM, pin count and package type) to all Renesas parts and then rearranges it in descending order i.e. the most similar Renesas part will be on top of the table.')
st.markdown(':small_blue_diamond: In the sidebar, you can expand the "Filter Renesas parts" to filter Renesas table according to user imposed constraints which include many different peripherals depending on your requirements.')
st.markdown(':small_blue_diamond: Do note, some peripherals have been simplified and bundled to similar functionality categories such as in Camera I/F and audio I/F, this is to ensure ease of comparison.')
st.markdown(':small_blue_diamond: The table offers an interactive experience with numerous features, including the ability to sort columns in ascending or descending order by clicking on them (an arrow is displayed), a scrollable interface to browse through Renesas parts, and the convenience of easily copying and pasting cells into Excel or Google Sheets.')

st.markdown(" :warning: :red[Disclaimer]: The selection for the tool has been done with great care, but data correctness is not always guaranteed." )


num_newlines = 18
for _ in range(num_newlines):
    st.markdown('  \n')

col1, col2 = st.columns([4,1])
with col2:
   st.markdown(":mailbox:**For any feedback, please contact:** eldar.sido.bx@renesas.com")


#---- HIDE STREAMLIT STYLE   -------#

hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)
