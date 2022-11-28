import streamlit as st
import numpy as np
import pandas as pd
#import cufflinks

st.set_page_config(layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown(f"# Differential Expression Data Plot")

int_data = pd.read_csv("./data/merged-int-data-nauger-2022-23-v2.csv")
len_int_data = len(int_data.index)

st.markdown(f"The current data frame contains **{len_int_data}** transcripts.")
st.markdown(f"For exploratory purposes the expression data shown here is filtered by using a FDR < 0.05. Please check the FDR of the transcript of interest to assess significance.")

trinitys = int_data.Trinity.unique().tolist()

sidebar = st.sidebar
trinity_selector = st.multiselect(
    "Select Transcript",
    trinitys
)

selected_data = int_data.query(f"Trinity in {trinity_selector}")

if len(selected_data)>0:
    st.markdown(f"Current selected transcripts: {trinity_selector}")
else:
    st.markdown('No transcripts selected.')

show_data = st.checkbox("Show Data", False)

int12hpe = sidebar.checkbox("12 HPE")
int1dpe = sidebar.checkbox("1 DPE")
int3dpe = sidebar.checkbox("3 DPE")
int7dpe = sidebar.checkbox("7 DPE")
int14dpe = sidebar.checkbox("14 DPE")
int14dpea = sidebar.checkbox("14 DPEA")
int14dpep = sidebar.checkbox("14 DPEP")
int21dpe = sidebar.checkbox("21 DPE")

lines = [int12hpe, int1dpe, int3dpe, int7dpe, int14dpe, int14dpea, int14dpep, int21dpe]
line_cols = ['log2FC_12hpe', 'log2FC_1dpe', 'log2FC_3dpe', 'log2FC_7dpe', 'log2FC_14dpe', 'log2FC_14dpea', 'log2FC_14dpep', 'log2FC_21dpe']
stages = [c[1] for c in zip(lines,line_cols) if c[0]==True]

if show_data:
    if len(selected_data)>0:
        st.dataframe(selected_data)
    else:
        st.markdown("Empty Dataframe")
    
plot=st.checkbox("Show Barplot", False)

if len(stages)>0:
    fig = selected_data.iplot(kind="bar", asFigure=True, xTitle="Trinity ID", yTitle="log2FC", x="Trinity", y=stages)
    st.plotly_chart(fig, use_container_width=False)
else:
    st.markdown("No stages selected. Please select stages in the sidebar menu.")