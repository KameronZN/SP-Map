import streamlit as st
import pandas as pd
import folium
from folium import Marker
from streamlit_folium import st_folium

# Load the data
data = pd.read_excel('service providers oct24 cleaned.xlsx')

# Centered and styled main title using inline styles
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #013220;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #013220;
        color: white;
    }
    .main-title {
        color: #e66c37; /* Title color */
        text-align: center; /* Center align the title */
        font-size: 3rem; /* Title font size */
        font-weight: bold; /* Title font weight */
        margin-bottom: .5rem; /* Space below the title */
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Subtle text shadow */
    }
    div.block-container {
        padding-top: 2rem; /* Padding for main content */
    }
    .subheader {
        color: #e66c37;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        padding: 10px;
        border-radius: 5px;
        display: inline-block;
    }
    .section-title {
        font-size: 1.75rem;
        color: #004d99;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }
    .text {
        font-size: 1.1rem;
        color: #333;
        padding: 10px;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .nav-item {
        font-size: 1.2rem;
        color: #004d99;
        margin-bottom: 0.5rem;
    }
    .separator {
        margin: 2rem 0;
        border-bottom: 2px solid #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">RWANDA SERVICE PROVIDER DASHBOARD</h1>', unsafe_allow_html=True)
st.image("servprov.jpg", caption='Eden Care Service Providers', use_column_width=True)

# User Instructions
st.markdown('<h2 class="subheader">User Instructions</h2>', unsafe_allow_html=True)
st.markdown('<div class="text">1. <strong>Map Navigation:</strong> Zoom in, out, or pan across the map to view service providers. Click on a pin to see detailed information, including account number, registration number, and license number.</div>', unsafe_allow_html=True)
st.markdown('<div class="text">2. <strong>Filters:</strong> Use the filters on the left to narrow down results by various criteria. The map and table will update based on your selection.</div>', unsafe_allow_html=True)
st.markdown('<div class="text">3. <strong>Data Table:</strong> The table below the map shows the filtered service providers with all key details.</div>', unsafe_allow_html=True)    
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Introduction
st.markdown('<h1 class="main-title">Map of Service Providers in Rwanda</h1>', unsafe_allow_html=True)
st.markdown('<div class="text"> This interactive dashboard is designed to provide stakeholders with a comprehensive overview of all service providers affiliated with Eden Care in Rwanda. With an intuitive map interface, users can easily visualize the locations of various service providers across different districts and provinces. The dashboard includes filters that allow for quick searches based on various criteria, ensuring that stakeholders can find the information they need with ease. By clicking on a service providers pin on the map, users can access detailed information, including the account number, registration number, and license number. This feature facilitates informed decision-making and enhances understanding of the service provider landscape. Overall, the Eden Care Service Provider Dashboard empowers stakeholders to gain valuable insights, streamline communication, and optimize service delivery throughout the organization..</div>', unsafe_allow_html=True)


# Create filters in the sidebar
logo_url = 'EC_logo (2).png'  
st.sidebar.image(logo_url, use_column_width=True)

st.sidebar.header("Filters")
types = st.sidebar.multiselect("Select Serive Provider Type", options=data['Type'].unique())
names = st.sidebar.multiselect("Select Service Prover Name", options=data['Name'].unique())
statuses = st.sidebar.multiselect("Select Status", options=data['Status'].unique())
provinces = st.sidebar.multiselect("Select Province", options=data['Province'].unique())
districts = st.sidebar.multiselect("Select District", options=data['District'].unique())
citys = st.sidebar.multiselect("Select City", options=data['City'].unique())

# Apply filters
filtered_data = data.copy()
if types:
    filtered_data = filtered_data[filtered_data['Type'].isin(types)]
if names:
    filtered_data = filtered_data[filtered_data['Name'].isin(names)]
if statuses:
    filtered_data = filtered_data[filtered_data['Status'].isin(statuses)]
if provinces:
    filtered_data = filtered_data[filtered_data['Province'].isin(provinces)]
if districts:
    filtered_data = filtered_data[filtered_data['District'].isin(districts)]
if citys:
    filtered_data = filtered_data[filtered_data['City'].isin(citys)]

# Create a Folium map centered on Rwanda
m = folium.Map(location=[-1.9632, 29.8739], zoom_start=8)

# Add markers to the map
for _, row in filtered_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
         popup=folium.Popup(f"""
    <b>Name:</b> {row['Name']}<br>
    <b>Type:</b> {row['Type']}<br>
    <b>Status:</b> {row['Status']}<br>
    <b>Account Id:</b> {row['Account Id']}<br>
    <b>Registration Number:</b> {row['Registration Number']}<br>
    <b>MOH License Number:</b> {row['Moh License Number']}<br>
""", max_width=300),
        icon=folium.Icon(icon='info-sign', color='#e66c37') 
    ).add_to(m)

# Render the map in Streamlit
st_folium(m, width=725, height=500)
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

# Display filtered data below the map
if not filtered_data.empty:
    st.subheader("Service Providers Data")
    st.dataframe(filtered_data.drop(columns=['Latitude', 'Longitude', 'Country Of Operation', 'Full Address'], errors='ignore'))

else:
    st.write("No service providers found for the selected filters.")
