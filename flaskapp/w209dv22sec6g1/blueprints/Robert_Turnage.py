from flask import  Blueprint
import altair as alt
import pandas as pd
import pandasql

Robert_Turnage = Blueprint('Robert_Turnage', __name__)
    
###########################
###### Data Sources #######
###########################
def bar_data():
    
    ingredients = pd.read_csv('ingredients.csv')
    
    # From here we can shape the flattened data to flow directly into data visuals
    df = pandasql.sqldf("""
      WITH Clean AS (--TODO:\\ Take to pre-flatten step to remove from BI
        SELECT CASE WHEN name LIKE '%garlic%' 
                    THEN 'garlic' 
                    WHEN name LIKE '%salt%' 
                    THEN 'salt' 
                    WHEN name LIKE '%ginger%' 
                    THEN 'ginger' 
                    WHEN name LIKE '%cumin%' 
                    THEN 'cumin' 
                    ELSE name
                END                             AS `Name`
                , cuisine                       AS `Cuisine`
          FROM ingredients
          WHERE Name <> 'salt and pepper'
      )  
      SELECT Name
            , Cuisine
            , COUNT(Name) AS `Count`
      FROM Clean
      GROUP BY Name, Cuisine
      ORDER BY Count DESC
      LIMIT 50          
    """)   
    
    return df

###########################
####### Ingredients #######
###########################
@Robert_Turnage.route("/data/ingredients/bar")
def bar():
    chart = alt.Chart(bar_data()).mark_bar().encode(    
                x='sum(Count):Q',
                y=alt.Y('Name:N', sort='-x'), 
                color='Cuisine:N'
            ).properties(title="Top 10 Count of Ingredients for by Cuisines")
    
    return chart.to_json()