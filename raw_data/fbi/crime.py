import time

import cfg
import pandas as pd
import os
import requests
import sqlite3

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
                        "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT"]

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


def get_crime_pickle_files():
    list_files = os.listdir("pickled_files")
    return list_files

def create_crime_database():

    conn = sqlite3.connect('crime.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE crime(
        ori text,
        data_year integer,
        offense text,
        state_abbr text,
        cleared integer,
        actual integer,
        data_range text
            
        )
    
    """)
    conn.commit()
    conn.close()


def insert_state_crime_data_into_database(state):

    pickle_name = "pickled_files/crime_in_the_us_{}.pkl".format(state)
    df = pd.read_pickle(pickle_name)

    conn = sqlite3.connect('crime.db')
    c = conn.cursor()

    for index, row in df.iterrows():
        # print(row)
        ori = row["ori"]
        year = row["data_year"]
        offense = row["offense"]
        state_abbr = row["state_abbr"]
        cleared = row["cleared"]
        actual = row["actual"]
        data_range = row["data_range"]

        c.execute(f"INSERT INTO crime VALUES ('{ori}', '{year}', '{offense}', '{state_abbr}', '{cleared}', '{actual}', '{data_range}')")

    conn.commit()
    conn.close()


def insert_all_states_into_crime_database():
    states = [state[-6:-4] for state in get_crime_pickle_files()]

    for state in states:
        print("Working on {}".format(state))
        start_time = time.time()
        insert_state_crime_data_into_database(state)
        total_time = time.time() - start_time
        print("{} took {} seconds".format(state, total_time))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    create_crime_database()
    insert_all_states_into_crime_database()