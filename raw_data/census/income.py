import raw_data.census.census_data as census
import pandas as pd
import cfg


def get_df_income(year, state_abbrev, zcta=None):

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
        'Total:!!$200,000 Or More Household Income In The Past 12 Months (In 2019 Inflation-Adjusted Dollars)': '>200k'})

    for column in df_income_cohorts.columns:
        print(column)

    return df_income_cohorts


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    df = get_df_income(2020, "NJ", zcta="07054")
    print(df)