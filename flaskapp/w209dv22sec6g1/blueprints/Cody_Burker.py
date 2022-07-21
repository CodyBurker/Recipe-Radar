from flask import Blueprint
import altair as alt
import pandas as pd
import numpy as np
from vega_datasets import data 

Cody_Burker = Blueprint('Cody_Burker', __name__)

###########################
###### Data Sources #######
###########################
path = '/w209dv22sec6g1/data/flavorprofiles.csv'

# cuisine_mapping = pd.read_csv('./CuisinneMapping.csv')
# taste = pd.read_csv('./taste.csv')

###########################
##### flavorprofiles ######
###########################

@Cody_Burker.route("/flavorprofiles/CBChart")
def chart():

    # Merge with cuisine mapping
    mapping = taste.merge(cuisine_mapping, on='cuisine')
    # Filter out those with blank "ISO 31661 Numeric"
    mapping_filtered = mapping[mapping['ISO 31661 Numeric'].notnull()]
    mapping_filtered.loc[:,'id'] = mapping_filtered['ISO 31661 Numeric'].astype(int).astype(str)

    mapping_filtered_flavor = mapping_filtered[mapping_filtered.columns[0:8]]
    all_flavors = list(mapping_filtered_flavor.columns[1:8])

    source = alt.topo_feature(data.world_110m.url, 'countries')
    sphere = alt.sphere()
    graticule = alt.graticule()

    mapping_filtered_flavor = mapping_filtered[['id', 'sweetness', 'saltiness', 'sourness', 'bitterness', 'savoriness', 'fattiness', 'spiciness']]
    mapping_filtered_flavor_pivoted = pd.melt(mapping_filtered_flavor, id_vars=['id'], value_vars=mapping_filtered_flavor.columns[1:8])

    # Take average of value by id, variabl
    averaged = mapping_filtered_flavor_pivoted.groupby(['id','variable']).mean()
    # Reset hierarchical index
    averaged = averaged.reset_index()

    all_flavors = list(mapping_filtered_flavor.columns[0:7])
    charts = []
    for selected_flavor in all_flavors:
        # filter source where variable == selected_flavor
        selected_averaged = averaged[averaged['variable'] == selected_flavor]

        chart = alt.Chart(source).mark_geoshape(
            ).encode(
                color= 'value:Q',
                # opacity = 'variable:N'
            ).transform_lookup(
            lookup='id',
            from_=alt.LookupData(selected_averaged, 'id', ['value','variable'])
        ).project(
            'equirectangular'
        ).properties(width=600, height=400, title= selected_flavor
        )
        charts.append(chart)
    # Display a grid of charts
    return_chart = alt.vconcat((charts[1] | charts[2]),
    (charts[3]| charts[4]),
    (charts[5]| charts[6]),
    ).resolve_scale(
        color='independent'
    )
    return return_chart.to_json()
