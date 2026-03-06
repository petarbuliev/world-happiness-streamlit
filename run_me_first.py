#  Imports section start
import streamlit as st
import pandas as pd
import os
import plotly.express as px
#  Imports section end

#  Function section start

@st.cache_data
def load_combined_data(data_folder="data"):
    combined_df = pd.DataFrame()

    columns_to_keep = [
        'Country or region', 'Year', 'Overall rank', 'Score',
        'GDP per capita', 'Social support', 'Healthy life expectancy',
        'Freedom to make life choices', 'Generosity', 'Perceptions of corruption'
    ]

    for file in sorted(os.listdir(data_folder)):
        if file.endswith(".csv"):
            print(f"==== {file} ====")  # I've added this to make sure the cache is sticking and we aren't runing throught the csv files more than once
            year = int(file[:4])
            file_path = os.path.join(data_folder, file)
            df = pd.read_csv(file_path)

            col_renames = {
                'Country': 'Country or region',
                'Country or region': 'Country or region',
                'Happiness Score': 'Score',
                'Happiness.Rank': 'Overall rank',
                'Happiness Rank': 'Overall rank',
                'Score': 'Score',
                'Economy (GDP per Capita)': 'GDP per capita',
                'Economy..GDP.per.Capita.': 'GDP per capita',
                'Family': 'Social support',
                'Social support': 'Social support',
                'Health (Life Expectancy)': 'Healthy life expectancy',
                'Health..Life.Expectancy.': 'Healthy life expectancy',
                'Freedom': 'Freedom to make life choices',
                'Freedom to make life choices': 'Freedom to make life choices',
                'Trust (Government Corruption)': 'Perceptions of corruption',
                'Trust..Government.Corruption.': 'Perceptions of corruption'
            }
            df.rename(columns=col_renames, inplace=True)

            df["Year"] = year
            df = df[[col for col in columns_to_keep if col in df.columns]]

            combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_df.to_csv("combined_happiness_data.csv", index=False)
    print("✅ Data combined and saved to combined_happiness_data.csv")
    
    return combined_df


#  Function section end

df = load_combined_data()

# Load the cleaned data
df = pd.read_csv("combined_happiness_data.csv")

st.title("🌍 World Happiness Report Explorer")

# # Sidebar: Select a year
# years = sorted(df["Year"].unique())
# selected_year = st.sidebar.selectbox("Select Year", years)

# # Filter the data
# filtered_df = df[df["Year"] == selected_year]

# st.subheader(f"Happiness Data for {selected_year}")
# st.dataframe(filtered_df)