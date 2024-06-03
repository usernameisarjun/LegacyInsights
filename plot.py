#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Function to display correlation matrix heatmap
def display_heatmap(data):
    numeric_data = data.select_dtypes(include=['int64', 'float64'])
    corr_matrix = numeric_data.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title('Correlation Matrix Heatmap')
    st.pyplot(fig)

# Function to display scatter plot
def display_scatter_plot(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='Location', y='Quantity', data=data, ax=ax)
    ax.set_title('Location vs. Quantity')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Function to classify artifact type as gold, silver, or other
def classify_artifact_type(artifact):
    if "gold" in artifact.lower():
        return "Gold"
    elif "silver" in artifact.lower():
        return "Silver"
    else:
        return "Other"

# Function to handle data analysis
def analyze_data(country_data, selected_country, selected_artifact_type):
    data = country_data[selected_country]
    artifact_data = data[data['Artifact'].apply(classify_artifact_type) == selected_artifact_type]
    if not artifact_data.empty:
        st.write("Data loaded for '{}' artifact type in '{}' country.".format(selected_artifact_type, selected_country))
        display_heatmap(artifact_data)
        display_scatter_plot(artifact_data)
    else:
        st.write("No data found for '{}' artifact type in '{}' country.".format(selected_artifact_type, selected_country))

# Load data from the Excel file
excel_data = pd.read_excel('antique_data.xlsx', sheet_name=None)

# Prompt user to select a country
available_countries = list(excel_data.keys())
selected_country = st.selectbox("Select a country from:", available_countries)

# Check if selected country is valid
if selected_country not in available_countries:
    st.write("Invalid country selected.")
else:
    # Select artifact type
    selected_artifact_type = st.selectbox("Select an artifact type:", ["Gold", "Silver", "Other"])

    # Perform analysis
    analyze_data(excel_data, selected_country, selected_artifact_type)
