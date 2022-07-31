from flask import  Blueprint
import altair as alt
import pandas as pd

Robert_Turnage = Blueprint('Robert_Turnage', __name__)

colorpalette = ["#ff0000","#b00000","#870000","#550000","#e4e400","#baba00","#878700","#545400","#00ff00","#00b000","#008700","#005500","#00ffff","#00b0b0","#008787","#005555","#b0b0ff","#8484ff","#4949ff","#0000ff","#ff00ff","#b000b0","#870087","#550055","#e4e4e4","#bababa","#878787","#545454"]
colorpalette = [x.lower() for x in colorpalette]
    
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
        #title="Top 10 Count of Ingredients for Recipes by Cuisines"
        height = 300
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

@Robert_Turnage.route("/data/ingredients/NumberOfRecipesVSCountOfIngredientByCuisine")
def NumberOfRecipesVSCountOfIngredientByCuisine(): 
    
    df = pd.read_csv('/groups/w209dv22sec6g1/flaskapp/data/NumberOfRecipesVSCountOfIngredientByCuisine.csv')
    
    source = df
    chart = alt.Chart(source).mark_circle().encode(
         x = alt.X('Ingredient Count:Q', scale=alt.Scale(zero=False), title='Count of Ingredients')
       , y = alt.Y('Number of Recipes:Q', scale=alt.Scale(zero=False, padding=1), title='Number of Recipes')
       , color=alt.Color("Cuisine:N"
            , scale=alt.Scale(range=colorpalette)
         ) 
       , size=alt.Size('Ingredient Count', scale=alt.Scale(domain=[0, 50]))
       , tooltip=alt.Tooltip(['Cuisine', 'Ingredient Count', 'Number of Recipes'], )
    ).properties(height = 800, width=500).interactive()
            
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

        