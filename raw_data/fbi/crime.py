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

    """
    Grabs crime stats from every ORI (originating agency identifiers) in the US.  There are 18,000+ ORIs, so this takes a while...
    :param year_start: Integer
    :param year_end: Integer
    :return: None ... maybe change this to return something?
    """

    header_url = r"https://api.usa.gov/crime/fbi/sapi/"

    df_oris = get_df_fbi_originating_agency_identifiers()

    states_completed = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "GM", "HI", "IA", "ID", "IL",
                        "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH",
                        "NJ", "NM", "NV", "NY", "OH", "OK", "OR"]

    # Loop through states and ORIs in each state and grab all crime stats in the given year range
    for state in df_oris["state_abbr"].unique():
        if state not in states_completed:
            data = []
            for ori in df_oris.loc[df_oris["state_abbr"] == state]["ori"].unique():

                full_url = f"{header_url}/api/summarized/agencies/{ori}/offenses/{year_start}/{year_end}?API_KEY={cfg.API_KEY_FBI}"
                print(full_url)
                response = requests.get(full_url).json()
                print(response)

                # Grab all dictionaries for given ori and add to data list
                for ori_dict in response["results"]:
                    data.append(ori_dict)

            # Create a state-specific pickle file
            df_crime = pd.DataFrame(data)
            state_specific_pickle = PICKLE_CRIME_IN_THE_US.replace("crime_in_the_us", "crime_in_the_us_{}".format(state) )
            df_crime.to_pickle(state_specific_pickle)


def test(state):
    state_specific_pickle = PICKLE_CRIME_IN_THE_US.replace("crime_in_the_us", "crime_in_the_us_{}".format(state))
    df = pd.read_pickle(state_specific_pickle)

    df_oris = get_df_fbi_originating_agency_identifiers()

    df = pd.merge(df, df_oris, on=["ori", "state_abbr"])

    return df

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    df = get_df_crime(2019, 2020)
    # print(df)

    # test("MI")