import cfg
import pandas as pd
import numpy as np
import json
import os
import requests

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API_KEY_NATIONAL_PARK_SERVICE = cfg.API_KEY_NATIONAL_PARK_SERVICE
# PICKLE_CRIME_IN_THE_US = os.path.join(cfg.ROOT_DIR, "raw_data/fbi/pickled_files/crime_in_the_us.pkl")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_park_data():
    # endpoint = "https://developer.nps.gov/api/v1/parks?stateCode=" + state

    url_header = r"https://developer.nps.gov/api/v1/parks"
    url = f"{url_header}?&limit=1000&api_key={API_KEY_NATIONAL_PARK_SERVICE}"

    print(url)
    response = requests.get(url).json()

    # Loop through and clean up certain columns that have too many dictionaries
    for park in response["data"]:
        park["activities_list"] = ", ".join([i['name'] for i in park["activities"]])
        park["topics_list"] = ", ".join([i['name'] for i in park["topics"]])
        park["entrance_fee"] = ", ".join([i['cost'] for i in park["entranceFees"]])
        park["entrance_fee_desc"] = ", ".join([i['description'] for i in park["entranceFees"]])
        park["zip_code"] = ", ".join([i['postalCode'][:5] for i in park["addresses"]])

    # Clean up results of dataFrame
    df_parks = pd.json_normalize(response["data"])
    df_parks = df_parks.drop(columns=["activities", "topics", "entranceFees", "entrancePasses", "fees", "operatingHours", "addresses",
                 "images", "contacts.phoneNumbers", "contacts.emailAddresses"])

    return df_parks


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    df = get_df_park_data()
    print(df)