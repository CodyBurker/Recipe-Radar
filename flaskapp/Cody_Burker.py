from flask import Blueprint
import altair as alt
import pandas as pd
import numpy as np
import pandasql

Cody_Burker = Blueprint('Cody_Burker', __name__)

###########################
###### Data Sources #######
###########################
def nutrition_data():
    
    path = '/data/flavorprofiles.csv'
    df = pd.read_csv(path)
    return df

###########################
##### flavorprofiles ######
###########################

@Cody_Burker.route("/data/flavorprofiles/CBChart")
def chart():
    
    # Compute x^2 + y^2 across a 2D grid
    x, y = np.meshgrid(range(-5, 5), range(-5, 5))
    z = x ** 2 + y ** 2
    
    # Convert this grid to columnar data expected by Altair
    source = pd.DataFrame({'x': x.ravel(),
                         'y': y.ravel(),
                         'z': z.ravel()})
    
    chart = alt.Chart(source).mark_rect().encode(
        x='x:O',
        y='y:O',
        color='z:Q'
    )
        
    return chart.to_json()