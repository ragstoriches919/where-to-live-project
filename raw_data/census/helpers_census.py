import raw_data.census.census_data as census
import pandas as pd
import numpy as np
import cfg

import geographic_data.build_geo as geo


def list_diff(list1, list2):
    """
    Returns columns that are in list1, but not in list2
    (list1 minus list2)
    :param list1: List
    :param list2: List
    :return: List
    """
    return list(set(list1) - set(list2))


def helper_get_df_cbsa_percentile(year, cbsa_name, func_median_for_state, str_col_name):

    """
    Returns the income percentile of all towns in the given CBSA
    :param year: (int) Ex.) 2020
    :param cbsa_name: (str) Ex.) "Dallas-Fort Worth-Arlington, TX"
    :param func_median_for_state: (Function) The state function that we want to find the percentile for.
    :param str_col_name: (str) The col name to groupby on.
    :return: DataFrame
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
    df_cbsa["percentile_cbsa_" + str_col_name] = df_cbsa.groupby(groupby_cols)[str_col_name].rank(pct=True)

    # Fix column order
    columns_order = list(set(df_cbsa.columns) - set(df_zip.columns)) + list(df_zip.columns)
    df_cbsa = df_cbsa[columns_order]
    df_cbsa = df_cbsa.sort_values(by=["percentile_cbsa_" + str_col_name], ascending=False)

    return df_cbsa


def helper_get_df_state_percentile(year, state, func_median_for_state, str_col_name):

    """
    Returns the income percentile of all towns in the given CBSA
    :param year: (int) Ex.) 2020
    :param state: (str) Ex.) "TX"
    :param func_median_for_state: (Function) The state function that we want to find the percentile for.
    :param str_col_name: (str) The col name to groupby on.
    :return: DataFrame
    """

    df_zip = geo.get_df_zip_code_complete(use_csv=True)

    # Percentile ranks for state the zip is in.
    groupby_cols = ["state"]
    df_median = func_median_for_state(year, state)
    df_median["percentile_state_" + str_col_name] = df_median.groupby(groupby_cols)[str_col_name].rank(pct=True)

    # Fix column order
    columns_order = list(set(df_median.columns) - set(df_zip.columns)) + list(df_zip.columns)
    df_median = df_median[columns_order]

    return df_median


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    # col_name = "median_household_income_2019_dollars"
    # cbsa_name = "Worcester, MA-CT"

    # df_cbsa = helper_get_df_cbsa_percentile(2020, cbsa_name, income.get_df_median_income, col_name)
    # print(df_cbsa)

    df = helper_get_df_state_percentile(2020, "CT", )