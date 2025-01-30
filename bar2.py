#This will create a graph that has a bar for the male totals and a bar for the female totals

#This version didnt have a copy so description so I have now included one


import os
import pandas as pd
import requests
import yaml
import seaborn as sns
import matplotlib.pyplot as plt

BASE_URL = "https://eu.kobotoolbox.org/api/v2"
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# read in secrets.yaml
with open("secrets.yml") as file:
    secrets = yaml.safe_load(file)
token = secrets["personal_api_token"]
form_id = "a8uCNcYY8At6dDfkqP88oW"  # in the URL in a browser

headers = {"Authorization": f"Token {token}"}
data_url = f"{BASE_URL}/assets/{form_id}/data.json"
response = requests.get(data_url, headers=headers)
if response.status_code == 200:
    data = response.json()
    bird_df = pd.DataFrame(data["results"])
else:
    print(f"Failed to fetch data from form {form_id}, check the form id and token.")


#   dropping the columns that the form has created that I will not be using in the graphs
bird_df = bird_df.drop(columns=['_id', 'formhub/uuid','start', 'end','_xform_id_string', '_uuid','_attachments', '_status','_geolocation', '_submission_time','_tags', '_notes','__version__','meta/instanceID','_validation_status','_submitted_by'])
bird_df = bird_df.drop(columns=['table/Total_Owls','table/Total_Parrots','table/Total_Penguins','table/Total_Toucans','table/Total_Chickens','table/Total_Cranes','table/Overall_Totals','table/Male_Totals','table/Female_Totals'])


#   Renaming the columns so they are more usable
bird_df = bird_df.rename(columns={'table/Total_Owls':'Total Owls','table/Total_Parrots':'Total Parrots','table/Total_Penguins':'Total Penguins','table/Total_Toucans':'Total Toucans','table/Total_Chickens':'Total Chickens','table/Total_Cranes':'Total Cranes'})
bird_df = bird_df.rename(columns={'table/Female_Owls':'Female Owls','table/Female_Parrots':'Female Parrots','table/Female_Penguins':'Female Penguins','table/Female_Toucans':'Female Toucans','table/Female_Chickens':'Female Chickens','table/Female_Cranes':'Female Cranes'})
bird_df = bird_df.rename(columns={'table/Male_Owls':'Male Owls','table/Male_Parrots':'Male Parrots','table/Male_Penguins':'Male Penguins','table/Male_Toucans':'Male Toucans','table/Male_Chickens':'Male Chickens','table/Male_Cranes':'Male Cranes'})
bird_df = bird_df.rename(columns={'table/Male_Totals':'Male Totals','table/Female_Totals':'Female Totals','table/Overall_Totals':'Overall Totals'})

#   Here I have used the .melt() method to turn each one of the column titles into
#   a value in the column I named "Bird_Gender" next I have turn the values for each
#   of these into another column called "Count".
#   These two together have formed a new dataframe called bird_melted which is closer 
#   to the format that I need to use the .lmplot() method
bird_melted = bird_df.melt(var_name='Bird_Gender', value_name='Count')

#   This next piece of code is used to create a new column called "Gender" this is done by 
#   using a lambda function that will interate tho the Bird_Gender column and if it 
#   contains the String "Male" it will add the new value "Male" to a new column "'Gender' if
#   it doesnt then it will add the value "Female"
bird_melted['Gender'] = bird_melted['Bird_Gender'].apply(lambda x: 'Male' if 'Male' in x else 'Female')
#   This next will create a new column that will record the type of bird  in a new column named "type of bird"
#   it does this using a .str.replace() method to replace the redundant parts of "Bird_Gender" 
bird_melted['Type of Bird'] = bird_melted['Bird_Gender'].str.replace('Male ', '').str.replace('Female ', '')
#   next we get ride of the "Bird_Gender" column as this is now redundant 
bird_melted = bird_melted.drop(columns=['Bird_Gender'])

# This is to make sure the data type is correct and can be used to make a chart
bird_melted['Count'] = pd.to_numeric(bird_melted['Count'], errors='coerce')


#  creates a time stamp that can be added to file name
current_date = pd.Timestamp.now().strftime("%Y-%m-%d")

# Group the data by Gender and Type of Bird, and sum the counts
grouped = bird_melted.groupby(['Gender', 'Type of Bird'])['Count'].sum().reset_index()

# Pivot the data to get one row per Gender, and columns for each Type of Bird
pivot_df = grouped.pivot(index='Gender', columns='Type of Bird', values='Count').fillna(0)

# Plotting
ax = pivot_df.plot(kind='bar', stacked=True, figsize=(10, 6), cmap='Dark2')

# Add labels and title
plt.xlabel('Gender')
plt.ylabel('Count')
plt.title('Totals of Gender')

# Show the plot
plt.xticks(rotation=0)
plt.show()
#

plt.savefig(f"{OUTPUT_DIR}/bird__total__bar{current_date}.png")# This OUTPUT_DIR was made for use with .gitingore 
