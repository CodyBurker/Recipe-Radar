from flask import Blueprint
import altair as alt
import pandas as pd
import numpy as np

Rishika_Pulvender = Blueprint('Rishika_Pulvender', __name__)

###########################
###### Data Sources #######
###########################
path = './data/nutrition.csv'

#data = pd.read_csv(path) #TODO:// Error 500 issues 

# df = data.filter(['id', 'cuisine', 'name', 'title', 'percentOfDailyNeeds'])
# out = df.pivot_table(index='id', columns='title', values=['percentOfDailyNeeds'])
# out.columns = out.swaplevel(axis='columns').columns.to_flat_index().map('_'.join)
# df1 = out.filter(['Carbohydrates_percentOfDailyNeeds', 'Fat_percentOfDailyNeeds', 'Protein_percentOfDailyNeeds'])
# df = df.filter(['id', 'cuisine', 'name'])
# nutrition = pd.concat([df, df1], axis=1)
# nutrition = nutrition[nutrition['id'].notna()]
# nutrition = nutrition[nutrition['cuisine'].notna()]
# nutrition[nutrition['id']==580502.0]
# nutrition['Carbohydrates_percentOfDailyNeeds'] = nutrition['Carbohydrates_percentOfDailyNeeds'].fillna(0)
# nutrition['Fat_percentOfDailyNeeds'] = nutrition['Fat_percentOfDailyNeeds'].fillna(0)
# nutrition['Protein_percentOfDailyNeeds'] = nutrition['Protein_percentOfDailyNeeds'].fillna(0)
# nutritionFinal = nutrition.groupby("cuisine", as_index=False).agg(
#     Carbs = ("Carbohydrates_percentOfDailyNeeds", np.mean),
#     Fats = ("Fat_percentOfDailyNeeds", np.mean),
#     Protein = ("Protein_percentOfDailyNeeds", np.mean)
# )
# df = data[data['title'].isin (["Fat", "Carbohydrates","Protein"])]
# df = df[['cuisine','title','amount']]

# # Adding in selector for first cuisine
# input_dropdown_cuisine = alt.binding_select(options=data.cuisine.unique(), name='Cuisines')
# selection = alt.selection_single(fields=['cuisine'], empty='none')

# alt.data_transformers.enable('default', max_rows=None)


###########################
####### nutrition #########
###########################

@Rishika_Pulvender.route("/data/nutrition/RPChart")
def chart():
    
    source = pd.DataFrame({
    'a': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'],
    'b': [28, 55, 43, 91, 81, 53, 19, 87, 52]
    })

    chart = alt.Chart(source).mark_bar().encode(
        x='a',
        y='b'
    )
    
    return chart.to_json()

@Rishika_Pulvender.route("/data/nutrition/pie1")
def pie1():
    
    color = alt.condition(selection, alt.Color('cuisine:N', legend=None), alt.value('lightgray'))
    make_selector = alt.Chart(df).mark_rect().encode(y='cuisine', color=color).add_selection(selection)

    # Pie chart for first cuisine
    pie1 = alt.Chart(df).mark_arc().encode(
        theta=alt.Theta(field="amount", type="quantitative"),
        color=alt.Color(field="title"),
    ).properties(width=300, height=300
    ).add_selection(selection
    ).transform_filter(selection)                
                    
    #### NEED TO FIX - TEXT AROUND PIE CHART DOES NOT WORK
    #text = pie.mark_text().encode(text="title:N")
    
    return pie1.to_json()


@Rishika_Pulvender.route("/data/nutrition/pie2")
def pie2():
    #pie_legend = alt.Chart(df).mark_rect().encode(y='title', color='title')

    # Selector for second cuisine
    selection_cuisine2 = alt.selection_single(fields=['cuisine'], empty='none')
    color2 = alt.condition(selection_cuisine2, alt.Color('cuisine:N', legend=None), alt.value('lightgray'))
    make_selector2 = alt.Chart(df).mark_rect().encode(y='cuisine', color=color2).add_selection(selection_cuisine2)

    # Pie chart for second cuisine
    pie2 = alt.Chart(df).mark_arc().encode(
        theta=alt.Theta(field="amount", type="quantitative"),
        color=alt.Color(field="title"),
    ).properties(width=300, height=300
    ).add_selection(selection_cuisine2
    ).transform_filter(selection_cuisine2)
    
    return pie2.to_json()
