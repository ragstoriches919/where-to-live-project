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
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_crime_pickle_files():
    """
    Gets list of all files in path fbi/pickled_files
    :return: List of strings
    """

    list_files = os.listdir("pickled_files")
    return list_files


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Database Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def create_database(db_location, dict_columns):

    """
    Can create a database with given parameters
    :param db_location: String.  Filepath.
    :param dict_columns: Dictionary Ex.) {"ori": "text"}
    :return: None
    """

    column_type_pairs = []
    for key, val in dict_columns.items():
        column_type_pairs.append(key + " " + val)
    sql_column_type_strings = (",".join(column_type_pairs))

    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute(f"CREATE TABLE {db_location[:-3]}({sql_column_type_strings})")

    conn.commit()
    conn.close()


def insert_dataframe_into_database(df, database_path):

    conn = sqlite3.connect(database_path)
    c = conn.cursor()

    row_str = ""
    for index, row in df.iterrows():
        for row_index, row_value in row.items():
            row_str += '"' + str(row_value) + '", '
        # print(row_str[:-2])
        c.execute(f"INSERT INTO {database_path[:-3]} VALUES ({row_str[:-2].strip()})")

        row_str = ""

    conn.commit()
    conn.close()


def insert_all_states_into_crime_database():

    """
    Insert crime data for ALL states into sqlite database.
    :return: None
    """

    states_pickles = get_crime_pickle_files()

    for file in states_pickles:
        print("Working on {}".format(file))
        start_time = time.time()
        file_path = "pickled_files/" + file
        df = pd.read_pickle(file_path)
        insert_dataframe_into_database(df, "crime.db")

        total_time = time.time() - start_time
        print(total_time)
        print("\n")


def insert_all_states_into_ori_database():

    """
    Insert crime data for ALL states into sqlite database.
    :return: None
    """

    df_oris = get_df_fbi_originating_agency_identifiers()
    insert_dataframe_into_database(df_oris, "oris.db")


def query_crime_db(state):

    """
    Queries crime.db and returns a dataframe of results
    :param state: String Ex.) "CT"
    :return: DataFrame
    """

    # Read sqlite query results into a pandas DataFrame
    conn = sqlite3.connect("crime.db")
    df = pd.read_sql_query("SELECT * from crime where state_abbr = '{}'".format(state), conn)
    conn.close()

    return df


def query_oris_db():

    conn = sqlite3.connect("oris.db")
    df_oris = pd.read_sql_query("SELECT * from oris", conn)
    conn.close()

    return df_oris


def create_crime_database():
    file_path = "crime.db"
    dict_column_types = {"ori": "text", "data_year": "integer", "offense": "text", "state_abbr": "text",
                         "cleared": "integer", "actual": "integer", "data_range": "text"}

    create_database(file_path, dict_column_types )


def create_ori_database():
    file_path = "oris.db"

    dict_column_types = {"ori": "text", "agency_name": "text", "agency_type_name": "text", "state_name": "text",
                         "state_abbr": "text", "division_name": "text", "region_name": "text", "region_desc": "text",
                         "county_name": "text", 'nibrs': "text", "latitude": "real",
                         "longitude": "real", "nibrs_start_date": "text"}

    create_database(file_path, dict_column_types)


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


def get_df_crime_cached(state):

    df_crime = query_crime_db(state)
    df_oris = query_oris_db()
    common_columns = list(set(df_crime.columns).intersection(set(df_oris.columns)))

    df_crime = pd.merge(df_crime, df_oris, on=common_columns)

    return df_crime


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    print(get_df_crime_cached("CT"))

