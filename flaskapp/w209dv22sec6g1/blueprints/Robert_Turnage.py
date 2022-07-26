from flask import  Blueprint
import altair as alt
import pandas as pd
from pandasql import sqldf

Robert_Turnage = Blueprint('Robert_Turnage', __name__)

colorpalette = ["#ff0000","#b00000","#870000","#550000","#e4e400","#baba00","#878700","#545400","#00ff00","#00b000","#008700","#005500","#00ffff","#00b0b0","#008787","#005555","#b0b0ff","#8484ff","#4949ff","#0000ff","#ff00ff","#b000b0","#870087","#550055","#e4e4e4","#bababa","#878787","#545454"]
colorpalette = [x.lower() for x in colorpalette]
    
###########################
###### Data Sources #######
###########################

# Transform Top 10 Ingredient Data
def TopIngredients_data():
    # From here we can shape the flattened data to flow directly into data visuals
    df = sqldf("""
      WITH Clean AS (--TODO:\\ Take to pre-flatten step to remove from BI
        SELECT CASE WHEN name LIKE '%garlic%' THEN 'garlic' 
                    WHEN name LIKE '%salt%'   THEN 'salt' 
                    WHEN name LIKE '%ginger%' THEN 'ginger' 
                    WHEN name LIKE '%cumin%'  THEN 'cumin' 
                    ELSE name END             AS `Name`
                , cuisine                     AS `Cuisine`
          FROM ingredients
          WHERE Name <> 'salt and pepper'
      ) 
      , T1 AS (
        SELECT Name
              , Cuisine
              , COUNT(Name) AS `Count`
        FROM Clean
        GROUP BY Name, Cuisine    
      )
      , T2 AS (
        SELECT Name
              , SUM(Count) AS `SumOfCount`
          FROM T1
          GROUP BY Name
      )
      SELECT A.Name
           , A.Cuisine
           , A.Count
           , B.SumOfCount
        FROM T1 AS A
        JOIN T2 AS B ON B.Name = A.Name
        ORDER BY B.SumOfCount DESC, A.Name    
    """)
    
    return df

# Pull data for Pie Data
def pie_data():
      
    df = sqldf("""
    WITH A AS (
        SELECT id
             , cuisine AS `Cuisine` 
             , COUNT(title) AS `Count`  
          FROM ingredients  
          GROUP BY cuisine, id
    ),
      B AS (
        SELECT cuisine AS `Cuisine` 
             , COUNT(cuisine) AS `CountOfRecipes`  
             , SUM(Count)     AS `SumOfIngredients`  
          FROM A  
          GROUP BY Cuisine
    ),
      C AS (
        SELECT Cuisine
             , CAST (SumOfIngredients AS FLOAT)  / CAST (CountOfRecipes AS FLOAT)  AS `AvgIngredientPerRecipe`
          FROM B  
          GROUP BY Cuisine
    )
    , D AS (
      SELECT B.*
           , C.AvgIngredientPerRecipe
        FROM B 
        JOIN C ON C.Cuisine = B.Cuisine
    
    )
    , E AS (
      SELECT *
           , SUM(CountOfRecipes) AS `TotalRecipes`
           , SUM(SumOfIngredients) AS `TotalIngredients`
        FROM D 
    )
    , F AS (
      SELECT D.*
           , CAST (D.CountOfRecipes AS FLOAT) / CAST (E.TotalRecipes AS FLOAT) AS `PercentOfRecipes`
           , CAST (D.SumOfIngredients AS FLOAT) / CAST (E.TotalIngredients AS FLOAT) AS `PercentOfIngredients`
        FROM D,E 
    )
    SELECT *
      FROM F
      ORDER BY AvgIngredientPerRecipe
    
    """)
    dfLength = len(df['Cuisine'])
    df['NormalizationFactor'] = (df['PercentOfRecipes'] - 1/dfLength)
    df['NormalizedAvgIngredient'] = df['AvgIngredientPerRecipe'] * df['NormalizationFactor']

    df1 = pd.DataFrame([df[['Cuisine','AvgIngredientPerRecipe']].max(), df[['Cuisine','AvgIngredientPerRecipe']].min()])
    df1 = df1.append({'Cuisine': 'Mean(All)', 'AvgIngredientPerRecipe': df[['AvgIngredientPerRecipe']].mean()[0]}, ignore_index=True)
    df1['AvgIngredientPerRecipe'] = df1['AvgIngredientPerRecipe'].round(2)
    
    return df1

###########################
####### Ingredients #######
###########################
Ingredients = pd.read_csv('/groups/w209dv22sec6g1/flaskapp/data/TopIngredients.csv')


@Robert_Turnage.route("/data/ingredients/TopIngredients")
def TopIngredients():
    
    df = Ingredients
    
    df1 = df[df['Name'].isin(df['Name'].unique()[0:10])].sort_values(by=['SumOfCount', 'Name'], ignore_index=True, ascending=False)
    chart = alt.Chart(df1).mark_bar().encode(    
        x=alt.X('Count:Q', title='Count', sort=None)
      , y=alt.Y('Name:N', title='Ingredients', sort=None)
      , color=alt.Color('Cuisine:N', scale=alt.Scale(range=colorpalette))
      , tooltip=alt.Tooltip(["Cuisine", "Count", "Name"])
    ).properties(
        title="Top 10 Count of Ingredients for by Cuisines"
      , height = 300
      , width = 400 
    ).interactive()
       
    return chart.to_json()


@Robert_Turnage.route("/data/ingredients/FirstIngredients")
def FirstIngredients():
    
    df = Ingredients
    
    dataframe = df[df['Name'].isin(df['Name'].unique()[0:1])]
    df1 = dataframe.sort_values(by=['Count'], ignore_index=True, ascending=False)
    chart = alt.Chart(df1).mark_bar().encode(  
        x=alt.X('Cuisine:N', axis=None, sort=None)  
      , y=alt.Y('Count', title = 'Count', sort=None)
      , tooltip=alt.Tooltip(["Cuisine", "Count", "Name"])
      , color=alt.Color('Cuisine:N'
            , title = 'Cuisine (Regionally Defined)'
            , legend=None
            , scale=alt.Scale(range=colorpalette)
        )
    ).properties(
        title = dataframe['Name'].unique()[0]
      , height = 300
      , width = 200 
    ).interactive()
        
    return chart.to_json()

@Robert_Turnage.route("/data/ingredients/SecondIngredients")
def SecondIngredients():
    
    df = Ingredients
    
    dataframe = df[df['Name'].isin(df['Name'].unique()[1:2])]
    df1 = dataframe.sort_values(by=['Count'], ignore_index=True, ascending=False)
    chart = alt.Chart(df1).mark_bar().encode(  
        x=alt.X('Cuisine:N', axis=None, sort=None)  
      , y=alt.Y('Count', title = 'Count', sort=None)
      , tooltip=alt.Tooltip(["Cuisine", "Count", "Name"])
      , color=alt.Color('Cuisine:N'
            , title = 'Cuisine (Regionally Defined)'
            , legend=None
            , scale=alt.Scale(range=colorpalette)
        )
    ).properties(
        title = dataframe['Name'].unique()[0]
      , height = 300
      , width = 200 
    ).interactive()
        
    return chart.to_json()

@Robert_Turnage.route("/data/ingredients/ThirdIngredients")
def ThirdIngredients():
    
    df = Ingredients
    
    dataframe = df[df['Name'].isin(df['Name'].unique()[2:3])]
    df1 = dataframe.sort_values(by=['Count'], ignore_index=True, ascending=False)
    chart = alt.Chart(df1).mark_bar().encode(  
        x=alt.X('Cuisine:N', axis=None, sort=None)  
      , y=alt.Y('Count', title = 'Count', sort=None)
      , tooltip=alt.Tooltip(["Cuisine", "Count", "Name"])
      , color=alt.Color('Cuisine:N'
            , title = 'Cuisine (Regionally Defined)'
            , legend=None
            , scale=alt.Scale(range=colorpalette)
        )
    ).properties(
        title = dataframe['Name'].unique()[0]
      , height = 300
      , width = 200 
    ).interactive()
        
    return chart.to_json()

@Robert_Turnage.route("/data/ingredients/IngredientPie")
def IngredientPie(): 
    
    df = pd.read_csv('/groups/w209dv22sec6g1/flaskapp/data/IngredientPie.csv')
    
    base = alt.Chart(df).encode(
    theta=alt.Theta("AvgIngredientPerRecipe:Q", stack=True)
      , color=alt.Color("Cuisine:N")
    )
    
    pie = base.mark_arc(outerRadius=120).properties(title="Most to Least Complex as an average of Ingredients used in Recipes by Cuisine")
    text = base.mark_text(radius=150, size=20).encode(text="AvgIngredientPerRecipe:N")
    
    chart = pie + text
        
    return chart.to_json()

###########################
######## Nutrition ########
###########################
NutritionData = pd.read_csv('/groups/w209dv22sec6g1/flaskapp/data/NutritionByCuisine.csv')
range_ = ['#F4D03F', 'steelblue']
@Robert_Turnage.route("/data/nutrition/AllHeat")
def AllHeat(): 
    
    chart = alt.Chart(NutritionData).mark_rect().encode(
    x='Name',
    y='Cuisine'
  , color=alt.Color('PODN:Q'
        , sort='x'
        , scale=alt.Scale(range=range_)
        , legend=alt.Legend(
            title = '% (U.S. FDA Recommended)'
          , orient='bottom'
          , columns=200
          , gradientLength=300
          , gradientThickness=30
          )
      )
    ).properties(
        title="Nutrition facts of Recipes by Cuisines"
        )

    
    return chart.to_json()


@Robert_Turnage.route("/data/nutrition/BadHeat")
def BadHeat(): 
    
    df = NutritionData
    bad = df[df['Type'] == 'bad']
    chart = alt.Chart(bad).mark_rect().encode(
        x='Name'
      , y='Cuisine'    
      , color=alt.Color('PODN:Q'
            , sort='x'
            , scale=alt.Scale(range=range_)
            , legend=alt.Legend(
                title = '% (U.S. FDA Recommended)'
              , orient='bottom'
              , columns=200
              , gradientThickness=30
              )
      ) # TODO//: Label what is PODN percentage of daily nutrion value based on 2k diet for avg human height. 
      , size='Type:N'
    ).properties(title="Bad Nutrition facts of Recipes by Cuisines")

    
    return chart.to_json()


@Robert_Turnage.route("/data/nutrition/GoodHeat")
def GoodHeat(): 

    df = NutritionData
    good = df[df['Type'] == 'good']
    chart = alt.Chart(good).mark_rect().encode(
        x='Name'
      , y='Cuisine'    
      , color=alt.Color('PODN:Q'
            , sort='x'
            , scale=alt.Scale(range=range_)
            , legend=alt.Legend(
                title = '% (U.S. FDA Recommended)'
              , orient='bottom'
              , columns=200
              , gradientLength=462
              , gradientThickness=30
              )
      ) # TODO//: Label what is PODN percentage of daily nutrion value based on 2k diet for avg human height. 
      , size='Type:N'
    ).properties(title="Good Nutrition facts of Recipes by Cuisines")

    
    return chart.to_json()

        