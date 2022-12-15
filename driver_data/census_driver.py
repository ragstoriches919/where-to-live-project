import cfg
import pandas as pd
import numpy as np
import json
import os

import raw_data.census.education as education
import raw_data.census.housing as housing
import raw_data.census.income as income




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Fucntions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def list_diff(list1, list2):
    return list(set(list1) - set(list2)) + list(set(list2) - set(list1))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Driver Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_stats_for_zip(year, state_abbrev, zcta):

    census_cols = ["zip", "town_name", "state", "cbsa_name", "cbsa_category", "cbsa_states", "sub_county_code",
                   "county_code", "cbsa_code", "county_name", "year", "csa_title"]

    df_income = income.get_df_median_income(year, state_abbrev, zcta=zcta)
    df_educ = education.get_df_education_level(year, state_abbrev, zcta=zcta)
    df_housing = housing.get_df_median_home_value(year, state_abbrev, zcta=zcta)

    df_all = pd.merge(df_income, df_educ, on=census_cols)
    df_all = pd.merge(df_all, df_housing, on=census_cols)

    # Rearrange columns for Census data
    new_cols = list_diff(df_all, census_cols) + census_cols
    df_all = df_all[new_cols]

    return df_all

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    df = get_stats_for_zip(2020, "FL", "33558")
    print(df)





