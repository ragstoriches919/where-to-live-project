import cfg
import pandas as pd
import requests
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_nces_k_12_data(fields):

    """
    """
    url_header = r"https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/School_Characteristics_Current/FeatureServer/2/query"
    fields_str = "*" if fields == [] else ",".join(fields)

    url = f"{url_header}?outFields={fields_str}&where=1%3D1&f=geojson"
    response = requests.get(url).json()
    df = pd.json_normalize(response["features"])
    print(response)
    print(df)
    # df.to_csv('test.csv')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    # get_df_nces_k_12_data()
    # cols = "OBJECTID,NCESSCH,SURVYEAR,STABR,SCH_NAME,LSTREET1,LSTREET2,LCITY,LSTATE,LZIP,GSLO,GSHI,TOTAL,LATCOD,LONCOD,NMCNTY,STUTERATIO,SCHOOL_TYPE_TEXT"
    cols = ['OBJECTID', 'NCESSCH', 'SURVYEAR', 'STABR', 'SCH_NAME', 'LSTREET1', 'LSTREET2', 'LCITY', 'LSTATE', 'LZIP',
            'GSLO', 'GSHI', 'TOTAL', 'LATCOD', 'LONCOD', 'NMCNTY', 'STUTERATIO', 'SCHOOL_TYPE_TEXT']

    get_df_nces_k_12_data(cols)