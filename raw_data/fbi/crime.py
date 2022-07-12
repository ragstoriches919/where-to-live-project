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


def get_df_crime():
    url = r"api.usa.gov/crime/fbi/sapi/"

    full_url = f"https://api.usa.gov/crime/fbi/sapi/api/summarized/state/CT/larceny/2015/2020?API_KEY={cfg.API_KEY_FBI}"
    response = requests.get(full_url).json()
    data = []

    df = pd.json_normalize(response["results"])
    print(df)
    return df

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    df = get_df_fbi_originating_agency_identifiers()