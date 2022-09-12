## This file is used to build geo tags for any zip code/state/msa

import cfg
import pandas as pd
import requests
import os
import numpy as np

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API_KEY_CENSUS = cfg.API_KEY_CENSUS

CSV_CENSUS_CODES = cfg.CSV_CENSUS_CODES
CSV_STATE_CODES = cfg.CSV_STATE_CODES
CSV_ZCTA_TO_MSA = cfg.CSV_ZTCA_TO_MSA
CSV_ZIPCODE_TO_ZCTA = cfg.CSV_ZIPCODE_TO_ZCTA
CSV_ZIPCODE_TO_COUNTY = cfg.CSV_ZIPCODE_TO_COUNTY
CSV_ZIPCODE_TO_SUB_COUNTY = cfg.CSV_ZIPCODE_TO_SUB_COUNTY
CSV_ZIPCODE_TO_CBSA = cfg.CSV_ZIPCODE_TO_CBSA
CSV_FIPS = cfg.CSV_FIP_CODES
CSV_CBSA_CODE_MAPPINGS_FROM_USPTO = cfg.CSV_CBSA_CODE_MAPPINGS_FROM_USPTO
CSV_CBSA_CODE_MAPPINGS_FROM_OMB = cfg.CSV_CBSA_CODE_MAPPINGS_FROM_OMB

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_zip_codes():

    """
    Get universe of zip codes
    :return: DataFrame
    """

    # https://udsmapper.org/zip-code-to-zcta-crosswalk/
    df_zip_codes = pd.read_csv(CSV_ZIPCODE_TO_ZCTA, encoding='latin-1')
    df_zip_codes.columns = df_zip_codes.columns.str.lower()
    df_zip_codes = df_zip_codes.loc[df_zip_codes["zip_join_type"] == "Zip matches ZCTA"]
    df_zip_codes.columns = ["zip", "town_name", "state", "zip_type", "zcta", "zip_join_type"]
    df_zip_codes['zip'] = df_zip_codes['zip'].astype(str).str.zfill(5)

    # Remove certain values
    df_zip_codes = df_zip_codes[~df_zip_codes["state"].isin(["PR", "VI", "GU"])]
    df_zip_codes = df_zip_codes[df_zip_codes["zip_type"] != "Post Office or large volume customer"]

    df_zip_codes = df_zip_codes.drop(columns = ["zcta", "zip_type", "zip_join_type"])

    return df_zip_codes


def get_df_zip_to_cbsa():

    """
    Get zip code to CBSA (core-based statistical area) data
    Source: https://www.huduser.gov/portal/datasets/usps_crosswalk.html#data
    :return:
    """

    df_cbsa = pd.read_csv(CSV_ZIPCODE_TO_CBSA)
    df_cbsa['zip'] = df_cbsa['zip'].astype(str).str.zfill(5)
    df_cbsa["tot_ratio"] = pd.to_numeric(df_cbsa["tot_ratio"])

    df_cbsa_grp = df_cbsa.groupby(["zip"])["tot_ratio"].max().reset_index()
    df_cbsa_best = pd.merge(df_cbsa_grp, df_cbsa, on=["zip", "tot_ratio"])
    df_cbsa_best["cbsa"] = df_cbsa_best["cbsa"].replace(99999, np.nan)

    df_cbsa_best = df_cbsa_best.rename(columns={"cbsa": "cbsa_code"})
    df_cbsa_best = df_cbsa_best.drop(columns = ["tot_ratio", "usps_zip_pref_city", "usps_zip_pref_state"])

    return df_cbsa_best


def get_df_zip_to_county():
    """
    Get zip code to county data
    Source: https://www.huduser.gov/portal/datasets/usps_crosswalk.html#data
    :return:
    """

    df_county = pd.read_csv(CSV_ZIPCODE_TO_COUNTY)
    df_county['zip'] = df_county['zip'].astype(str).str.zfill(5)
    df_county["tot_ratio"] = pd.to_numeric(df_county["tot_ratio"])

    df_county_grp = df_county.groupby(["zip"])["tot_ratio"].max().reset_index()
    df_county_best = pd.merge(df_county_grp, df_county, on=["zip", "tot_ratio"])

    # Get county names
    df_fips = pd.read_csv(CSV_FIPS)
    df_county_best = pd.merge(df_county_best, df_fips[["CountyName", "CountyFIPS"]], left_on = ["county"], right_on = ["CountyFIPS"], how="left" )
    df_county_best = df_county_best.rename(columns = {"CountyName": "county_name", "county": "county_code"})

    df_county_best = df_county_best.drop(columns = ["usps_zip_pref_city", "usps_zip_pref_state"])

    return df_county_best


def get_df_zip_to_sub_county():

    """
    Get zip code to sub-county data
    Source: https://www.huduser.gov/portal/datasets/usps_crosswalk.html#data
    :return: DataFrame
    """

    df_sub_county = pd.read_csv(CSV_ZIPCODE_TO_SUB_COUNTY)
    df_sub_county['zip'] = df_sub_county['zip'].astype(str).str.zfill(5)
    df_sub_county["tot_ratio"] = pd.to_numeric(df_sub_county["tot_ratio"])
    df_sub_county_grp = df_sub_county.groupby(["zip"])["tot_ratio"].max().reset_index()
    df_sub_county_best = pd.merge(df_sub_county_grp, df_sub_county, on=["zip", "tot_ratio"])

    df_sub_county_best = df_sub_county_best.drop(columns=["usps_zip_pref_city", "usps_zip_pref_state", "tot_ratio"])

    df_sub_county_best = df_sub_county_best.rename(columns = {"county_sub": "sub_county_code"})

    return df_sub_county_best


def get_df_cbsa_codes(missing_cbsa_codes=None):

    """
    Gets all CBSA codes that will be used in the geo-tagging process.
    Source (US Patent and Trade Office): https://www.uspto.gov/web/offices/ac/ido/oeip/taf/cls_cbsa/cbsa_countyassoc.htm
    Better source (OMB):  https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html
    :param missing_cbsa_codes: List of Integers Ex.) [33380, 42500, 19430, ...]
    :return: DataFrame
    """

    df_cbsa_omb = pd.read_csv(CSV_CBSA_CODE_MAPPINGS_FROM_OMB)
    df_cbsa_omb = df_cbsa_omb[["cbsa_code", "cbsa_name", "cbsa_category", "csa_title"]]
    df_cbsa_omb = df_cbsa_omb.drop_duplicates()

    # return df_cbsa_omb

    # Look for missing codes in df_geo
    if missing_cbsa_codes is not None:

        df_cbsa_uspto = pd.read_csv(CSV_CBSA_CODE_MAPPINGS_FROM_USPTO)
        df_cbsa_uspto_filtered = df_cbsa_uspto.loc[df_cbsa_uspto["cbsa_code"].isin(missing_cbsa_codes)]

        df_cbsa_uspto_filtered = df_cbsa_uspto_filtered[["cbsa_code", "cbsa_name", "cbsa_category"]]
        df_cbsa_uspto_filtered["csa_title"] = np.nan

        df_cbsa_omb = pd.concat([df_cbsa_omb, df_cbsa_uspto_filtered])

    return df_cbsa_omb

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Driver Function
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_zip_code_complete():

    """
    Driver function to retrieve complete zip code dataset.
    :return: DataFrame
    """

    df_zips = get_df_zip_codes()
    df_zip_to_cbsa = get_df_zip_to_cbsa()
    df_zip_to_county = get_df_zip_to_county()
    df_zip_to_sub_county = get_df_zip_to_sub_county() # May not have any real use case...

    # Prep CBSA codes...look at OMB and USPTO sources
    df_cbsa_codes_init = get_df_cbsa_codes()
    missing_cbsa_codes = list(set(df_zip_to_cbsa["cbsa_code"].unique()) - set(df_cbsa_codes_init["cbsa_code"]))
    df_cbsa_codes = get_df_cbsa_codes(missing_cbsa_codes)

    df_geo = pd.merge(df_zips, df_zip_to_cbsa, left_on="zip", right_on="zip", how="left")
    df_geo = df_geo.loc[~df_geo["cbsa_code"].isnull()]
    df_geo = pd.merge(df_geo, df_zip_to_county[["zip", "county_code", "county_name"]], left_on="zip", right_on="zip", how='left')
    df_geo = pd.merge(df_geo, df_zip_to_sub_county, left_on="zip", right_on="zip", how='left')
    df_geo = pd.merge(df_geo, df_cbsa_codes, on="cbsa_code", how="left")

    return df_geo

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    # df = build_geographic_database()
    # print(df)

    df = get_df_zip_code_complete()
