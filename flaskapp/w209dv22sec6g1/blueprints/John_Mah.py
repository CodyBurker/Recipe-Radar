from flask import Blueprint
import altair as alt
import pandas as pd
import numpy as np

John_Mah = Blueprint('John_Mah', __name__)

###########################
###### Data Sources #######
###########################
def nutrition_data():

    path = '/w209dv22sec6g1/data/flavorprofiles.csv'
    df = pd.read_csv(path)
    return df

###########################
##### flavorprofiles ######
###########################

@John_Mah.route("/flavorprofiles/JMChart")
def chart():

    x = np.arange(100)
    source = pd.DataFrame({
      'x': x,
      'f(x)': np.sin(x / 5)
    })

    chart = alt.Chart(source).mark_line().encode(
        x='x',
        y='f(x)'
    )

    return chart.to_json()
