#!/usr/bin/env python3
import pandas as pd
import streamlit as st
import folium
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import requests

# Function to read latitude and longitude data from the CSV file
def read_lat_long(country):
    df = pd.read_csv(f'{country}.csv')
    return df[['Latitude', 'Longitude', 'Location']]

# Get list of available countries
available_countries = ['India', 'America', 'UK', 'France', 'Russia']  # Update with your available countries

# Prompt user to select a country
selected_country = st.selectbox("Select a country:", available_countries)

# Read latitude and longitude data for the selected country
df = read_lat_long(selected_country)

# Create a map centered at the first location
mymap = folium.Map(location=[df['Latitude'].iloc[0], df['Longitude'].iloc[0]], zoom_start=5)

# Add markers for each location
for index, row in df.iterrows():
    folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['Location']).add_to(mymap)

# Save the map as an HTML file
mymap.save(f'{selected_country}_map.html')

st.write(f"Map of {selected_country} is saved as {selected_country}_map.html")


# Load data for all countries
excel_file = "antique_data.xlsx"
country_sheets = pd.read_excel(excel_file, sheet_name=None)

# Load data for the selected country
data = country_sheets[selected_country]

# Categorize artifacts into 'Gold', 'Silver', and 'Other' categories
def categorize_artifact(artifact):
    if 'Gold' in artifact:
        return 'Gold'
    elif 'Silver' in artifact:
        return 'Silver'
    else:
        return 'Other'

data['Artifact Category'] = data['Artifact'].apply(categorize_artifact)

# Get list of available artifact types
available_artifact_types = data['Artifact Category'].unique()

# Prompt user to select an artifact type
selected_artifact_type = st.selectbox("Select an artifact type:", available_artifact_types)

# Filter data for the selected artifact type
selected_data = data[data['Artifact Category'] == selected_artifact_type]

# Preprocess categorical features
encoder = LabelEncoder()
selected_data['Location'] = encoder.fit_transform(selected_data['Location'])
selected_data['Time Period'] = encoder.fit_transform(selected_data['Time Period'])

# Define features and target
X = selected_data[['Location', 'Quantity', 'Time Period']]
y = selected_data['Historical Period']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Decision Tree Visualization
if st.sidebar.selectbox("Select Model:", ["Decision Tree Visualization", "Naive Bayes Classifier"]) == "Decision Tree Visualization":
    # Train Decision Tree Classifier
    dt_classifier = DecisionTreeClassifier()
    dt_classifier.fit(X_train, y_train)

    # Visualize decision tree
    st.write("Decision Tree Visualization:")
    fig, ax = plt.subplots(figsize=(15, 10))
    plot_tree(dt_classifier, feature_names=X.columns, class_names=dt_classifier.classes_, filled=True, ax=ax)
    st.pyplot(fig)

# Naive Bayes Classifier
else:
    # Calculate probabilities for Naive Bayes Classifier
    st.sidebar.header("Naive Bayes Classifier")

    # Calculate the total number of artifacts
    total_artifacts = len(selected_data)

    # Calculate the number of artifacts for each type
    gold_artifacts = len(selected_data[selected_data['Artifact'].str.contains('gold', case=False)])
    silver_artifacts = len(selected_data[selected_data['Artifact'].str.contains('silver', case=False)])
    other_material_artifacts = total_artifacts - gold_artifacts - silver_artifacts

    # Calculate the probabilities
    probability_gold = gold_artifacts / total_artifacts
    probability_silver = silver_artifacts / total_artifacts
    probability_other_material = other_material_artifacts / total_artifacts

    # Display the probabilities
    st.subheader("Artifact Probabilities")
    st.write(f"Probability of finding a gold artifact: {probability_gold:.2%}")
    st.write(f"Probability of finding a silver artifact: {probability_silver:.2%}")
    st.write(f"Probability of finding an artifact made of other materials: {probability_other_material:.2%}")

    # Calculate conditional probabilities
    if silver_artifacts != 0:
        probability_gold_given_silver = gold_artifacts / silver_artifacts
    else:
        probability_gold_given_silver = 0

    if gold_artifacts != 0:
        probability_silver_given_gold = silver_artifacts / gold_artifacts
    else:
        probability_silver_given_gold = 0

    probability_other_material_given_gold_or_silver = 1 - ((gold_artifacts + silver_artifacts) / total_artifacts)

    # Display the conditional probabilities
    st.subheader("Naive Bayes Classifier")
    st.write(f"Probability of finding a gold artifact given the presence of a silver artifact: {probability_gold_given_silver:.2%}")
    st.write(f"Probability of finding a silver artifact given the presence of a gold artifact: {probability_silver_given_gold:.2%}")
    st.write(f"Probability of finding an artifact made of other materials given the presence of gold or silver artifacts: {probability_other_material_given_gold_or_silver:.2%}")

# Add "Next" button
if st.button("Next"):
    try:
        response = requests.get("http://localhost:8502")
        if response.status_code == 200:
            st.success("plot.py loaded successfully.")
            st.markdown("<a href='http://localhost:8502'>Click for More</a>", unsafe_allow_html=True)
        else:
            st.error("Error loading plot.py.")
    except requests.RequestException as e:
        st.error(f"Error loading plot.py: {e}")
if st.button("Generate Map"):
    try:
        response = requests.get("http://127.0.0.1:5500/India_map.html")
        if response.status_code == 200:
            st.success("plot.py loaded successfully.")
            st.markdown("<a href='http://127.0.0.1:5500/India_map.html'>Map</a>", unsafe_allow_html=True)
        else:
            st.error("Error loading plot.py.")
    except requests.RequestException as e:
        st.error(f"Error loading plot.py: {e}")
    
