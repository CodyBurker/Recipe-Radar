from flask import  Blueprint, render_template
import altair as alt
import pandas as pd
from pandasql import sqldf

Robert_Turnage = Blueprint('Robert_Turnage', __name__)
    
###########################
###### Data Sources #######
###########################

def bar_data():
    
    ingredients = pd.read_csv('ingredients.csv')
    
    # From here we can shape the flattened data to flow directly into data visuals
    df = ingredients[['name', 'cuisine']]
    df.rename(columns = {'name': 'Name', 'cuisine': 'Cuisine'}, inplace=True)
    df['Count'] = df.groupby(['Name', 'Cuisine'])['Name'].transform('count')
    df.sort_values(by=['Count'], inplace=True, ascending=False, ignore_index=True)
    df.drop_duplicates(subset=None, keep='first', inplace=True, ignore_index=True)
    df = df[df['Name'].isin(df['Name'].unique()[0:10])]
    
    return df

###########################
####### Ingredients #######
###########################
@Robert_Turnage.route("/data/ingredients/RTChart")
def chart():
    chart = alt.Chart(bar_data()).mark_bar().encode(    
                x='sum(Count):Q',
                y=alt.Y('Name:N', sort='-x'), 
                color='Cuisine:N'
            ).properties(title="Top 10 Count of Ingredients for by Cuisines")
    
    return chart.to_json()

@Robert_Turnage.route("/data/ingredients/Bottom")
def bottom():
    # Least complex dishes by Cuisine
    df = sqldf("""
    WITH Top AS (
        SELECT id
             , cuisine AS `Cuisine` 
             , COUNT(name) AS `Count`  
          FROM ingredients  
          GROUP BY cuisine, id
    ), Bottom AS (
        SELECT id
             , cuisine AS `Cuisine` 
             , COUNT(name) AS `Count`
          FROM ingredients  
          GROUP BY cuisine, id
    )
    SELECT *
      FROM Bottom
     ORDER BY cuisine, count 

    """)

    bottomdf = pd.DataFrame(columns = ['Cuisine', 'Count'])
    for idx, Cuisine in enumerate(df['Cuisine'].unique()):
      bottomdf.loc[idx] = [Cuisine, df[df['Cuisine'] == Cuisine]['Count'].min()]
    bottomdf.sort_values(by=['Count'], inplace=True, ascending=False, ignore_index=True)

    chart = alt.Chart(bottomdf).mark_bar().encode(
        x='Count:Q',
        y=alt.Y('Cuisine:N', sort='-x')
    ).properties(title="Most complexity as a Top Count of Ingredients by Cuisines")
    
    return chart.to_json()


        