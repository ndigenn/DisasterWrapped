import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files
from google.colab import drive
import pathlib
import spacy

drive.mount('/content/drive')

filepath = "FemaWebDisasterDeclarations.csv"
df = pd.read_csv(filepath)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

unique_incidents = df['incidentType'].unique().tolist()
lowercase_list = [x.lower() for x in unique_incidents]

# User input
user_input = input("Enter a question. (Ex. What natural disasters happend in Florida in 2003?) ")

# Process user input
doc = nlp(user_input)

# Extract state name, year, incident type, and declaration type from user input
state_name = None
year = None
incident_type = None
declaration_type = None
for token in doc:
    if token.ent_type_ == "GPE":  # GPE (Geopolitical Entity) is used by spaCy for locations
        state_name = token.text
    if token.like_num and len(token.text) == 4:  # Check if token resembles a 4-digit number (year)
        year = token.text
    if token.text.lower() in lowercase_list:  # Check for incident type keywords
        incident_type = token.text
    if token.text.lower() in ['dr', 'em', 'hm']:  # Check for declaration type keywords
        declaration_type = token.text

# Filter DataFrame based on extracted values, select relevant columns
filtered_df = df.copy()  # Start with a copy of the original DataFrame
if state_name:
    filtered_df = filtered_df[filtered_df['stateName'].str.contains(state_name, case=False, na=False)]
if year:
    filtered_df = filtered_df[filtered_df['incidentBeginDate'].str.contains(year)]
if incident_type:
    filtered_df = filtered_df[filtered_df['incidentType'].str.contains(incident_type, case=False)]
if declaration_type:
    filtered_df = filtered_df[filtered_df['declarationType'].str.contains(declaration_type, case=False)]

# Print selected columns
if not filtered_df.empty:
    userFilteredDf = filtered_df[['disasterName', 'declarationType', 'incidentBeginDate', 'stateName', 'incidentType']]
else:
    print("No matching data found.")

print(userFilteredDf)
