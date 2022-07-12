import cfg
import pandas as pd
import numpy as np
import json
import os
import requests

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API_KEY_FBI = cfg.API_KEY_FBI
PICKLE_CRIME_IN_THE_US = os.path.join(cfg.ROOT_DIR, "raw_data/fbi/pickled_files/crime_in_the_us.pkl")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_fbi_originating_agency_identifiers():
    """
    Retrurns ORIs (originating agency identifiers) for all police systems in the US by state
    :return: DataFrame
    """
    url = f"https://api.usa.gov/crime/fbi/sapi/api/agencies?api_key={API_KEY_FBI}"
    response = requests.get(url).json()

    data = []
    for state in response.keys():
        for ori in response[state].keys():
            data.append(response[state][ori])

    df_oris = pd.DataFrame(data)
    df_oris = df_oris.sort_values(by=["state_abbr", "ori"])

    return df_oris


def get_df_crime(year_start, year_end):
    header_url = r"https://api.usa.gov/crime/fbi/sapi/"

    df_oris = get_df_fbi_originating_agency_identifiers()

    data = []

    # Loop through ORIs and calculate all crime stats in the given year range
    # for ori in df_oris["ori"].unique():
    for ori in df_oris["state_abbr"].unique():

        full_url = f"{header_url}/api/summarized/agencies/{ori}/offenses/{year_start}/{year_end}?API_KEY={cfg.API_KEY_FBI}"
        print(full_url)
        response = requests.get(full_url).json()
        print(response)

        for ori_dict in response["results"]:
            data.append(ori_dict)

    df_crime = pd.DataFrame(data)
    df_crime.to_pickle(PICKLE_CRIME_IN_THE_US)

    return df_crime



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    # df = get_df_crime(2019, 2020)

