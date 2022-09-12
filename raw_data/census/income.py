import raw_data.census.census_data as census
import pandas as pd
import numpy as np
import cfg

import geographic_data.build_geo as geo

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_income_percentages(df_income):

    """
    Get DataFrame by income %.  Helper function for get_df_income()
    :param df_income: DataFrame, from get_df_income()
    :return: DataFrame
    """

    for col in [i for i in df_income.columns if "Household Income" in i]:
        if "Total: Household Income In The Past 12 Months" not in col:
            demographic = col.split(" ")[2]
            df_income["%_Household Income" + demographic] = df_income[col] / df_income["Total: Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)"]

    return df_income


def get_df_income_percentile_state(year, state):

    df_zip = geo.get_df_zip_code_complete(use_csv=True)

    # Percentile ranks for state the zip is in.
    groupby_cols = ["state"]
    df_income = get_df_median_income(year, state)
    df_income["percentile_median_income_state"] = df_income.groupby(groupby_cols)["median_household_income_2019_dollars"].rank(pct=True)

    # Fix column order
    columns_order = list(set(df_income.columns) - set(df_zip.columns)) + list(df_zip.columns)
    df_income = df_income[columns_order]

    return df_income


def get_df_percentile_cbsa(year, cbsa_name):
    df_zip = geo.get_df_zip_code_complete(use_csv=True)
    df_zip = df_zip.loc[df_zip["cbsa_name"] == cbsa_name]
    cbsa_states = df_zip["cbsa_states"].iloc[0].split(",")

    df_income_cbsa = None
    for state in cbsa_states:
        df_income_state = get_df_median_income(year, state)
        if df_income_cbsa is None:
            df_income_cbsa = df_income_state
        else:
            df_income_cbsa = pd.concat([df_income_cbsa, df_income_state])

    # Calculate income percentiles
    df_income_cbsa = df_income_cbsa.loc[df_income_cbsa["cbsa_name"] == cbsa_name]
    groupby_cols = ["cbsa_name"]
    df_income_cbsa["percentile_median_income_cbsa"] = df_income_cbsa.groupby(groupby_cols)["median_household_income_2019_dollars"].rank(pct=True)

    # Fix column order
    columns_order = list(set(df_income_cbsa.columns) - set(df_zip.columns)) + list(df_zip.columns)
    df_income_cbsa = df_income_cbsa[columns_order]

    return df_income_cbsa

    


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_median_income(year, state_abbrev, zcta=None):

    """
    Returns median household income
    :param year: Integer
    :param state_abbrev: String Ex.) "CT"
    :param zcta: String Ex.) "06074"
    :return: DataFrame
    """

    group = "B19013"
    census_codes_income = census.get_list_census_codes_by_group(group)

    df_income = census.get_df_census_data(census_codes_income, year, state_abbrev, zcta=zcta)
    df_income = df_income.rename(columns={
        "Median Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars) ": "median_household_income_2019_dollars"})
    df_income = df_income.loc[df_income["median_household_income_2019_dollars"] >= 0]

    return df_income


def get_df_income_by_cohort(year, state_abbrev, zcta=None):

    """
    Returns median household income by income cohort
    :param year: Integer
    :param state_abbrev: String Ex.) "CT"
    :param zcta: String Ex.) "06074"
    :return: DataFrame
    """

    group = "B19001"

    census_codes_income_cohorts = census.get_list_census_codes_by_group(group)
    df_income_cohorts = census.get_df_census_data(census_codes_income_cohorts, year, state_abbrev, zcta=zcta)
    df_income_cohorts = df_income_cohorts.rename(columns={
        'Total:!!Less Than $10,000 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income <10k',
        'Total:!!$10,000 To $14,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 10-15k',
        'Total:!!$15,000 To $19,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 15-20k',
        'Total:!!$20,000 To $24,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 20-25k',
        'Total:!!$25,000 To $29,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 25-30k',
        'Total:!!$30,000 To $34,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 30-35k',
        'Total:!!$35,000 To $39,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 35-40k',
        'Total:!!$40,000 To $44,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 40-45k',
        'Total:!!$45,000 To $49,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 45-50k',
        'Total:!!$50,000 To $59,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 50-60k',
        'Total:!!$60,000 To $74,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 60-75k',
        'Total:!!$75,000 To $99,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 75-100k',
        'Total:!!$100,000 To $124,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 100-125k',
        'Total:!!$125,000 To $149,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 125-150k',
        'Total:!!$150,000 To $199,999 Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income 150-200k',
        'Total:!!$200,000 Or More Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': 'Household Income >200k'})

    df_income_cohorts = get_df_income_percentages(df_income_cohorts)

    return df_income_cohorts


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    # df = get_df_median_income(2020, "CT")
    # df = get_df_income_percentiles(2020, "06074")

    # get_df_income_percentile_state(2020, "CT")

    get_df_percentile_cbsa(2020, "Worcester, MA-CT")