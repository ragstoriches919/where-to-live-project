import cfg
import pandas as pd
import requests
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PICKLE_K12_SCHOOL_DATA = os.path.join(cfg.ROOT_DIR, "raw_data/dept_of_education/pickled_files/k12_school_data.pkl")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_nces_k_12_data(fields):

    """
    Returns K-12 data from NCES API
    :param fields: List of strings Ex.) ['OBJECTID', 'NCESSCH', 'SURVYEAR', 'STABR']
    :return: DataFrame
    """

    url_header = r"https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/School_Characteristics_Current/FeatureServer/2/query"
    fields_str = "*" if fields == [] else ",".join(fields)

    total_records = 120000
    offset = 2000

    # Loop through the pages of the URL and return specified data
    for i in range(total_records//offset + 1):
        url = f"{url_header}?outFields={fields_str}&where=1%3D1&f=geojson&resultOffset={str(offset * i)}"
        response = requests.get(url).json()
        print(url)

        if i==0:
            df_schools = pd.json_normalize(response["features"])
            df_schools.to_pickle(PICKLE_K12_SCHOOL_DATA)
        else:
            df_schools_temp = pd.json_normalize(response["features"])
            df_schools = pd.concat([df_schools, df_schools_temp])
            df_schools.to_pickle(PICKLE_K12_SCHOOL_DATA)

        print(df_schools[df_schools.columns[:4]].tail())

    return df_schools


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    # fields = ['OBJECTID', 'NCESSCH', 'SURVYEAR', 'STABR', 'SCH_NAME', 'LSTREET1', 'LSTREET2', 'LCITY', 'LSTATE', 'LZIP',
    #         'GSLO', 'GSHI', 'TOTAL', 'LATCOD', 'LONCOD', 'NMCNTY', 'STUTERATIO', 'SCHOOL_TYPE_TEXT']

    # get_df_nces_k_12_data(fields)

    df = pd.read_pickle(PICKLE_K12_SCHOOL_DATA)
    print(df)
