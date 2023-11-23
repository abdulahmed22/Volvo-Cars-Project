import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import random
import os 
import warnings
warnings.filterwarnings('ignore')

# Set page configuration and title
st.set_page_config(page_title="Volvo Cars Waste Management", page_icon=":recycle:",
                    layout="wide")

# Title and introduction
st.title(":recycle: Volvo Waste Generation Dashboard")
st.markdown(
    """<div style='background-color: #f0f0f0; padding: 10px;'>
    <p>This dashboard provides insights into Volvo Cars' waste generation.</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


with st.sidebar:
    uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is None:
    st.info(" Upload a file through config", icon="ℹ️")
    st.stop()
@st.cache_data
def load_data(path: str):
    df = pd.read_excel(path)
    return df


df = load_data(uploaded_file)


col1, col2 = st.columns((2)) 


filtered = df[df['RODkod'] != '-1']
filtered = filtered[filtered['Hämtställe Ort'] != 'Mölndal' ]
filtered = filtered[~filtered['Hämtställe Märkning'].str.contains('Rest.', case=False)]
filtered['Lev.YearMonth'] = pd.to_datetime(filtered['Lev.YearMonth'], format='%Y%m').dt.to_period('M').astype(str)

filtered.head(10)
# Create for Region
region = st.sidebar.multiselect("Region",filtered["Hämtställe Ort"].unique())
if not region:
    df2 = filtered.copy()
else:
    df2 = filtered[filtered["Hämtställe Ort"].isin(region)]


# Get unique facility types
facility_types = ['RA', 'RB', 'Lammhult', 'Others']

# Sidebar multiselect for selecting facility types
selected_facility_types = st.sidebar.multiselect(
    "Facility Type",
    facility_types,  # Provide options for facility types
)

# Create a dictionary to map facility types to respective buildings
facility_buildings = {
    'RA': df2[df2['Hämtställe Märkning'].str.contains('RA', case=True)]['Hämtställe Märkning'].unique(),
    'RB': df2[df2['Hämtställe Märkning'].str.contains('RB', case=True)]['Hämtställe Märkning'].unique(),
    'Lammhult': df2[df2['Hämtställe Märkning'].str.contains('Lammhult', case=False)]['Hämtställe Märkning'].unique(),
    'Others': df2[~df2['Hämtställe Märkning'].str.contains('RA|RB|Lammhult', case=True)]['Hämtställe Märkning'].unique()
}

# Sidebar multiselect for selecting buildings based on the selected facility types
# Filter buildings based on selected facility types
selected_buildings = []
for facility_type in selected_facility_types:
    selected_buildings.extend(facility_buildings.get(facility_type, []))

# Remove duplicates from selected buildings
selected_buildings = list(set(selected_buildings))

# Sidebar multiselect for selecting buildings based on the selected facility types
selected_building = st.sidebar.multiselect(
    "Building",
    selected_buildings,  # Display corresponding buildings
)
if not selected_facility_types:
    df3 = df2.copy()
else:
    df3 = df2[df2["Hämtställe Märkning"].isin(selected_building)]
category_df = df3.groupby(by = ["Lev.YearMonth"], as_index = False)["Kvantitet kg"].sum()



total_waste = df3["Kvantitet kg"].sum()

# Calculate recycled waste and rate (assuming 'Recycled waste' is a column in your DataFrame)
recycled_waste = df3[df3['RODkod'].isin(['R13', 'R3', 'R10', 'R11', 'R4','R5','R9'])]['Kvantitet kg'].sum()
landfill_waste =  df3[df3['RODkod'].isin(['D1', 'D9', 'D10'])]['Kvantitet kg'].sum()
recycled_rate = (recycled_waste / total_waste) * 100 if total_waste != 0 else 0  # Calculate the percentage



def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 24,
            },
            title={
                "text": label,
                "font": {"size": 22},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)

top_left_column, top_right_column = st.columns((2, 1))
bottom_left_column, bottom_right_column = st.columns(2)

with top_left_column:
    column_1, column_2, column_3, column_4 = st.columns(4)

    with column_1:
        plot_metric(
            "Total Waste (kg)",
            total_waste,
            prefix="",
            suffix="",
            show_graph=False,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
        plot_gauge(total_waste/total_waste, "#0068C9", "", "Current Ratio", 1)

    with column_2:
        plot_metric(
            "Recycled Waste(kg)",
            recycled_waste,
            prefix="",
            suffix="",
            show_graph=False,
            color_graph="rgba(255, 43, 43, 0.2)",
        )
        plot_gauge(recycled_waste/total_waste, "#FF8700", "", "", 1)

    with column_3:
        plot_metric("Recycled Rate", recycled_rate, prefix="", suffix=" %", show_graph=False)
        plot_gauge(recycled_rate, "#FF2B2B", "", "", 100)
        
    with column_4:
        plot_metric("Landfill Waste(kg)",landfill_waste , prefix="", suffix="", show_graph=False)
        plot_gauge(landfill_waste/total_waste, "#29B09D", "", "", 1)