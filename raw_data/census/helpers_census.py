import raw_data.census.census_data as census
import pandas as pd
import numpy as np
import cfg
import income

import geographic_data.build_geo as geo

# def helper_get_df_cbsa_percentile(year, cbsa_name):
#     pass


def helper_get_df_cbsa_percentile(year, cbsa_name, func_median_for_state, str_col_name):

    """
    Returns the income percentile of all towns in the given CBSA
    :param year: (int) Ex.) 2020
    :param cbsa_name: (str) Ex.) "Dallas-Fort Worth-Arlington, TX"
    :param df_cbsa_calcs: (DataFrame) The DataFrame you want to compute CBSA percentiles for
    :param str_col_name: (str) The col name to calculate the CBSA percentiles on Ex.) "median_household_income_2019_dollars"
    :return:
    """

    df_zip = geo.get_df_zip_code_complete(use_csv=True)
    df_zip = df_zip.loc[df_zip["cbsa_name"] == cbsa_name]
    cbsa_states = df_zip["cbsa_states"].iloc[0].split(",")

    df_cbsa = None
    for state in cbsa_states:
        df_state = func_median_for_state(year, state)
        if df_cbsa is None:
            df_cbsa = df_state
        else:
            df_cbsa = pd.concat([df_cbsa, df_state])

    # Calculate income percentiles
    df_cbsa = df_cbsa.loc[df_cbsa["cbsa_name"] == cbsa_name]
    groupby_cols = ["cbsa_name"]
    df_cbsa[str_col_name + "_cbsa_percentile"] = df_cbsa.groupby(groupby_cols)[str_col_name].rank(pct=True)

    # Fix column order
    columns_order = list(set(df_cbsa.columns) - set(df_zip.columns)) + list(df_zip.columns)
    df_cbsa = df_cbsa[columns_order]
    df_cbsa = df_cbsa.sort_values(by=[str_col_name + "_cbsa_percentile"])

    return df_cbsa



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    col_name = "median_household_income_2019_dollars"
    cbsa_name = "Dallas-Fort Worth-Arlington, TX"
    df = income.get_df_median_income(2020, "TX")

    df_cbsa = helper_get_df_cbsa_percentile(2020, cbsa_name, income.get_df_median_income, col_name)
    print(df_cbsa)