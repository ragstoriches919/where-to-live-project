import cfg
import pandas as pd
import numpy as np
import json
import os

import raw_data.census.income as income
import raw_data.census.education as education
import raw_data.census.housing as housing

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Fucntions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def list_diff(list1, list2):
    diff = list(set(list1) - set(list2)) + list(set(list2) - set(list1))
    diff.sort()
    return diff

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Driver Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_stats_for_zip(year, state_abbrev, zcta):

    census_cols = ["zcta", "zip_code", "po_name", "state", "zip_type", "zip_join_type", "cbsa", "year"]

    df_income = income.get_df_income(year, state_abbrev, zcta=zcta)
    df_educ = education.get_df_education_level(year, state_abbrev, zcta=zcta)
    df_housing_values = housing.get_df_housing_values(year, state_abbrev, zcta=zcta)
    df_housing_value_median = housing.get_df_median_home_value(year, state_abbrev, zcta=zcta)

    df_all = pd.merge(df_income, df_educ, on=census_cols)
    df_all = pd.merge(df_all, df_housing_values, on=census_cols)
    df_all = pd.merge(df_all, df_housing_value_median, on=census_cols)

    # Rearrange columns for Census data
    new_cols = list_diff(df_all, census_cols) + census_cols
    df_all = df_all[new_cols]

    return df_all

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    df = get_stats_for_zip(2020, "CT", "06074")

    # a = [1, 2, 3]
    # b = [2, 3, 4]

