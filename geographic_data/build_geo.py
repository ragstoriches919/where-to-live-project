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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_df_zip_codes():
    # https://udsmapper.org/zip-code-to-zcta-crosswalk/
    df_zip_codes = pd.read_csv(CSV_ZIPCODE_TO_ZCTA, encoding='latin-1')
    df_zip_codes.columns = df_zip_codes.columns.str.lower()
    df_zip_codes = df_zip_codes.loc[df_zip_codes["zip_join_type"] == "Zip matches ZCTA"]
    df_zip_codes.columns = ["zip_code", "po_name", "state", "zip_type", "zcta", "zip_join_type"]
    df_zip_codes['zip_code'] = df_zip_codes['zip_code'].astype(str).str.zfill(5)

    # Remove certain values
    df_zip_codes = df_zip_codes[~df_zip_codes["state"].isin(["PR", "VI", "GU"])]
    df_zip_codes = df_zip_codes[df_zip_codes["zip_type"] != "Post Office or large volume customer"]

    return df_zip_codes


def get_df_zcta_to_msa():
    df_zips = pd.read_csv(CSV_ZCTA_TO_MSA, encoding='latin-1')
    df_zips['zcta5'] = df_zips['zcta5'].astype(str).str.zfill(5)
    df_zips = df_zips.rename(columns={"zcta5": "zcta", "cbsaname15": "cbsa_name"})
    df_zips = df_zips[["zcta", "cbsa"]]

    return df_zips


def get_df_zcta_to_county():
    df_county = pd.read_csv(CSV_ZIPCODE_TO_COUNTY)
    df_county['zip'] = df_county['zip'].astype(str).str.zfill(5)
    df_county["tot_ratio"] = pd.to_numeric(df_county["tot_ratio"])

    df_county_grp = df_county.groupby(["zip"])["tot_ratio"].max().reset_index()

    df_county_best = pd.merge(df_county_grp, df_county, on=["zip", "tot_ratio"])

    return df_county_best


def build_geographic_database():

    df_zips = get_df_zip_codes()
    df_msa = get_df_zcta_to_msa()
    df_county = get_df_zcta_to_county()

    df_geo = pd.merge(df_zips, df_msa, on="zcta", how="left")
    df_geo = df_geo.loc[~df_geo["cbsa"].isnull()]
    df_geo = pd.merge(df_geo, df_county[["zip", "county"]], left_on= "zcta", right_on = "zip" )

    # df_geo_null = df_geo.loc[df_geo["cbsa"].isnull()]


    print(df_geo)




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    get_df_zcta_to_county()