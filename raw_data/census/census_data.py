import pandas as pd
import requests
import cfg

import raw_data.fhfa.fhfa_data as fhfa

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API_KEY_CENSUS = cfg.API_KEY_CENSUS

CSV_CENSUS_CODES = cfg.CSV_CENSUS_CODES
CSV_STATE_CODES = cfg.CSV_STATE_CODES
CSV_ZCTA_TO_MSA = cfg.CSV_ZTCA_TO_MSA
EXCEL_ZIPCODE_TO_ZCTA = cfg.EXCEL_ZIPCODE_TO_ZCTA

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_census_state_code(state_abbrev):

    df_state_codes = pd.read_csv(CSV_STATE_CODES, dtype=str)
    state_code = df_state_codes.loc[df_state_codes["state_abbrev"]==state_abbrev]["state_code"].iloc[0]

    return state_code


def get_dict_new_census_column_names(list_old_col_names):

    dict_col_names = {}
    df_census_codes = pd.read_csv(CSV_CENSUS_CODES)

    for old_col in list_old_col_names:
        if old_col not in ["NAME", "GEO_ID", "state", "zip code tabulation area"]:

            if old_col == "B01001_001E":
                dict_col_names[old_col] = "population_total"
            elif old_col == "B25107_001E":
                dict_col_names[old_col] = "house_price_median"
            elif old_col == "B19013_001E":
                dict_col_names[old_col] = "household_income_median"
            else:
                dict_col_names[old_col] = df_census_codes.loc[df_census_codes["census_code"] == old_col]["label"].iloc[0]

    # More manual column name changes
    dict_col_names["zip code tabulation area"] = "zcta"
    dict_col_names["state"] = "state_code"

    return dict_col_names


def get_df_zip_codes():
    # https://udsmapper.org/zip-code-to-zcta-crosswalk/
    df_zip_codes = pd.read_excel(EXCEL_ZIPCODE_TO_ZCTA, dtype='str')
    df_zip_codes.columns = df_zip_codes.columns.str.lower()
    df_zip_codes = df_zip_codes.loc[df_zip_codes["zip_join_type"]=="Zip matches ZCTA"]

    return df_zip_codes


def get_df_zcta_to_msa():

    df_zips = pd.read_csv(CSV_ZCTA_TO_MSA)
    df_zips['zcta5'] = df_zips['zcta5'].astype(str).str.zfill(5)
    df_zips = df_zips.rename(columns={"zcta5": "zcta", "cbsaname15": "cbsa_name"})
    df_zips = df_zips[["zcta", "cbsa"]]

    return df_zips


def get_df_census_codes():

    data_url = r"https://api.census.gov/data/2019/acs/acs5/variables.json"
    response = requests.get(data_url).json()
    vars = response["variables"]

    data = []
    for key in vars:
        data.append([key, vars[key]["label"]])

    df_census_codes = pd.DataFrame(data=data, columns=["census_code", "label"])
    df_census_codes.to_csv(CSV_CENSUS_CODES)
    return df_census_codes


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_df_census_data(census_codes, year, state_abbrev, zcta=None ):

    """
    Retrieves census data from API based on contents of census_codes param
    :param census_codes: String Ex.) 'B01001_001E' or 'NAME,GEO_ID,B01001_001E,B25107_001E,B19013_001E'
    :param year: Integer
    :param state_abbrev: String Ex.) "CT"
    :param zcta: String Ex.) "06074"
    :return: DataFrame
    """

    dsource = 'acs/acs5'

    state_code = get_census_state_code(state_abbrev)
    base_url = f'https://api.census.gov/data/{year}/{dsource}'
    data_url = f'{base_url}?get={census_codes}&for=zip%20code%20tabulation%20area:*&in=state:{state_code}&key={API_KEY_CENSUS}'
    print(data_url)

    response = requests.get(data_url).json()
    column_names = response[0]
    data = response[1:]

    dict_new_cols = get_dict_new_census_column_names(column_names)

    df = pd.DataFrame(columns=column_names, data=data )
    df = df.rename(columns=dict_new_cols)
    df = df.sort_values(by=["zcta"])

    # Merge zip codes database
    df = pd.merge(df, get_df_zip_codes(), on="zcta")
    df = pd.merge(df, get_df_zcta_to_msa(), on="zcta", how='left')

    if zcta is not None:
        df = df.loc[df["zip code tabulation area"] == zcta]

    return df


def get_df_acs_5y_data_raw(year, state_abbrev, zcta=None):

    census_codes = 'NAME,GEO_ID,B01001_001E,B25107_001E,B19013_001E'
    df = get_df_census_data(census_codes, year, state_abbrev, zcta=zcta)
    df = pd.merge(df, fhfa.get_df_fhfa_data(), on="cbsa", how='left')

    # Drop negative values
    df = df.loc[ (df["house_price_median"].astype(int) > 0) & (df["household_income_median"].astype(int) > 0)]

    # Extra analytics
    df["home_price_to_median_income"] = df["house_price_median"].astype(int) / df["household_income_median"].astype(int)
    df["household_income_percentile"] = df["household_income_median"].astype(int).rank(pct=True)
    df["home_price_to_income_percentile"] = df["home_price_to_median_income"].astype(int).rank(pct=True, ascending=False)

    df.to_csv('test.csv')

    return df

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    df = get_df_census_data('NAME,GEO_ID,B01001_001E,B25107_001E,B19013_001E', 2019, "CT")
