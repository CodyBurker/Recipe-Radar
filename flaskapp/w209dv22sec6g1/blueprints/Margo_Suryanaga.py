from flask import Blueprint
import altair as alt
import pandas as pd
import numpy as np

Margo_Suryanaga = Blueprint('Margo_Suryanaga', __name__)

###########################
###### Data Sources #######
###########################
path = 'taste.csv'
# taste = pd.read_csv(path)  #TODO:// Error 500 issues 
    
# flavor_grouped_byCuisine = taste.groupby("cuisine", as_index=False).agg(
#     sweetness = ("sweetness", np.mean),
#     saltiness = ("saltiness", np.mean),
#     sourness = ("sourness", np.mean),
#     bitterness = ("bitterness", np.mean),
#     savoriness = ("savoriness", np.mean),
#     fattiness = ("fattiness", np.mean),
#     spiciness = ("spiciness", np.mean)
# )
    
# ## Create bar chart with flavor profiling
# ## NEED TO UPDATE TO DYNAMICALLY SPIT OUT MULTIPLE CHARTS
# input_dropdown_cuisine = alt.binding_select(options=taste.cuisine.unique(), name='Cuisines')
# selection = alt.selection_multi(fields=['cuisine'], empty='none')

# alt.data_transformers.enable('default', max_rows=None)

# color = alt.condition(selection, alt.Color('cuisine:N', legend=None), alt.value('lightgray'))
# make_selector = alt.Chart(flavor_grouped_byCuisine).mark_rect().encode(y='cuisine', color=color).add_selection(selection)

###########################
##### flavorprofiles ######
###########################

@Margo_Suryanaga.route("/data/flavorprofiles/MSSweet")
def Sweet():
    
    # Layering and configuring the components
    chart_sweet = alt.Chart(flavor_grouped_byCuisine).mark_bar().encode(
            x=alt.X('sweetness:Q'),
            y = 'cuisine',
            color = color
        ).properties(width=300, height=300, title='Sweetness'
    ).transform_filter(selection)
                     
    return chart_sweet.to_json()

@Margo_Suryanaga.route("/data/flavorprofiles/MSSpicy")
def Spicy():
    chart_spicy = alt.Chart(flavor_grouped_byCuisine).mark_bar(
        ).encode(
            x=alt.X('spiciness:Q'),
        y = 'cuisine',
        color = color
        ).properties(width=300, height=300, title='Spiciness'
    ).transform_filter(
        selection
    )
    return chart_spicy.to_json()

@Margo_Suryanaga.route("/data/flavorprofiles/MSSalty")
def Salty():        
    chart_salty = alt.Chart(flavor_grouped_byCuisine).mark_bar(
        ).encode(
            x=alt.X('saltiness:Q'),
        y = 'cuisine',
        color = color
        ).properties(width=300, height=300, title='Saltiness'
    ).transform_filter(
        selection
    )
    return chart_salty.to_json()

@Margo_Suryanaga.route("/data/flavorprofiles/MSSour")
def Sour():    
    chart_sour = alt.Chart(flavor_grouped_byCuisine).mark_bar(
        ).encode(
            x=alt.X('sourness:Q'),
        y = 'cuisine',
        color = color
        ).properties(width=300, height=300, title='Sourness'
    ).transform_filter(
        selection
    )
    return chart_sour.to_json()
    
@Margo_Suryanaga.route("/data/flavorprofiles/MSBitter")
def Bitter():
    chart_bitter = alt.Chart(flavor_grouped_byCuisine).mark_bar(
        ).encode(
            x=alt.X('bitterness:Q'),
        y = 'cuisine',
        color = color
        ).properties(width=300, height=300, title='Bitterness'
    ).transform_filter(
        selection
    )
    return chart_bitter.to_json()

@Margo_Suryanaga.route("/data/flavorprofiles/MSSavory")
def Savory():    
    chart_savory = alt.Chart(flavor_grouped_byCuisine).mark_bar(
        ).encode(
            x=alt.X('savoriness:Q'),
        y = 'cuisine',
        color = color
        ).properties(width=300, height=300, title='Savoriness'
    ).transform_filter(
        selection
    )
    return chart_savory.to_json()

@Margo_Suryanaga.route("/data/flavorprofiles/MSFatty")
def Fatty():    
    chart_fatty = alt.Chart(flavor_grouped_byCuisine).mark_bar(
        ).encode(
            x=alt.X('fattiness:Q'),
        y = 'cuisine',
        color = color
        ).properties(width=300, height=300, title='Fattiness'
    ).transform_filter(
        selection
    )

    return chart_fatty.to_json()
    