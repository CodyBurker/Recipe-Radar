from flask import Blueprint
import altair as alt
import pandas as pd
import pandasql

Margo_Suryanaga = Blueprint('Margo_Suryanaga', __name__)

###########################
###### Data Sources #######
###########################
def nutrition_data():
    
    path = '/data/flavorprofiles.csv'
    pd.read_csv(path)
    return df

###########################
##### flavorprofiles ######
###########################

@Margo_Suryanaga.route("/data/flavorprofiles/MSChart")
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