import raw_data.census.census_data as census
import matplotlib.pyplot as plt
import pandas as pd
import cfg
# import seaborn as sns

import helpers_census

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_housing_value_shares(df_housing):

    """
    Housing shares by value of housing units
    :param df_housing: DataFrame (get_df_housing_values())
    :return: DataFrame
    """

    housing_columns = [col for col in df_housing.columns if "housing_value" in col]
    for col in housing_columns:
        df_housing["%_" + col] = (df_housing[col] / df_housing["total_number_housing_units"]) * 100

    return df_housing


def create_chart_housing_value_shares(df_housing):

    """
    Shows a histogram of housing values
    :param df_housing: DataFrame
    :return: Matplotlib chart
    """

    # Rename columns in chart
    df_housing = df_housing[[col for col in df_housing.columns if "%" in col]]
    df_housing.columns = [col.replace("%_housing_value_", "") for col in df_housing.columns if "%" in col]

    cols_in_chart = df_housing.columns
    y_values = df_housing[cols_in_chart].values.flatten().tolist()

    x_values = cols_in_chart
    sns.set_style('whitegrid')
    ax = sns.barplot(x_values, y_values, color="#419ff2")
    ax.bar_label(ax.containers[0], fmt='%.0f%%')

    plt.xticks(rotation=90)
    plt.grid()
    plt.show()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_median_home_value(year, state_abbrev, zcta=None):

    """
    Gets median home value
    :param year: Integer
    :param state_abbrev: String
    :param zcta: String Ex.) "06074"
    :return: DataFrame
    """

    group = "B25077"
    census_codes_median_value = census.get_list_census_codes_by_group(group)
    df_median_value = census.get_df_census_data(census_codes_median_value, year, state_abbrev, zcta=zcta)

    df_median_value = df_median_value.rename(columns={
        "Median Value (Dollars) ": "median_home_value"})

    return df_median_value


def get_df_housing_values(year, state_abbrev, zcta=None):

    """
    Aggregates housing values
    :param year: Integer
    :param state_abbrev: String
    :param zcta: String Ex.) "06074"
    :return: DataFrame
    """

    group = "B25075"

    census_codes_housing_values = census.get_list_census_codes_by_group(group)
    df_housing_values = census.get_df_census_data(census_codes_housing_values, year, state_abbrev, zcta=zcta)
    df_housing_values = df_housing_values.rename(columns = {"Total: Value": "total_number_housing_units"})


    df_housing_values["housing_value_<$100k"] = df_housing_values['Total:!!Less Than $10,000 Value'] + \
                                               df_housing_values['Total:!!$10,000 To $14,999 Value'] + \
                                               df_housing_values['Total:!!$15,000 To $19,999 Value'] + \
                                               df_housing_values['Total:!!$20,000 To $24,999 Value'] + \
                                               df_housing_values['Total:!!$25,000 To $29,999 Value'] + \
                                               df_housing_values['Total:!!$30,000 To $34,999 Value'] + \
                                               df_housing_values['Total:!!$35,000 To $39,999 Value'] + \
                                               df_housing_values['Total:!!$40,000 To $49,999 Value'] + \
                                               df_housing_values['Total:!!$50,000 To $59,999 Value'] + \
                                               df_housing_values['Total:!!$60,000 To $69,999 Value'] + \
                                               df_housing_values['Total:!!$70,000 To $79,999 Value'] + \
                                               df_housing_values['Total:!!$80,000 To $89,999 Value'] + \
                                               df_housing_values['Total:!!$90,000 To $99,999 Value']

    df_housing_values["housing_value_$100k-$200k"] = df_housing_values['Total:!!$100,000 To $124,999 Value'] + \
                                                   df_housing_values['Total:!!$125,000 To $149,999 Value'] + \
                                                   df_housing_values['Total:!!$150,000 To $174,999 Value'] + \
                                                   df_housing_values['Total:!!$175,000 To $199,999 Value']

    df_housing_values["housing_value_$200k-$300k"] = df_housing_values['Total:!!$200,000 To $249,999 Value'] + \
                                                   df_housing_values['Total:!!$250,000 To $299,999 Value']

    df_housing_values["housing_value_$300k-$400k"] = df_housing_values['Total:!!$300,000 To $399,999 Value']

    df_housing_values["housing_value_$400k-$500k"] = df_housing_values['Total:!!$400,000 To $499,999 Value']
    df_housing_values["housing_value_$500k-$750k"] = df_housing_values['Total:!!$500,000 To $749,999 Value']
    df_housing_values["housing_value_$750k-$1mio"] = df_housing_values['Total:!!$750,000 To $999,999 Value']
    df_housing_values["housing_value_$1mio-$1.5mio"] = df_housing_values['Total:!!$1,000,000 To $1,499,999 Value']
    df_housing_values["housing_value_$1.5mio-$2mio"] = df_housing_values['Total:!!$1,500,000 To $1,999,999 Value']
    df_housing_values["housing_value_>$2mio"] = df_housing_values['Total:!!$2,000,000 Or More Value']

    df_housing_values = get_df_housing_value_shares(df_housing_values)

    return df_housing_values


def get_df_median_home_price_percentile_cbsa(year, cbsa_name):

    """
    Returns the income percentile of all towns in the given CBSA
    :param year: (int) Ex.) 2020
    :param cbsa_name: (str) Ex.) "Dallas-Fort Worth-Arlington, TX"
    :return:
    """

    col_name = "median_home_value"
    df_income_percentile_cbsa = helpers_census.helper_get_df_cbsa_percentile(year, cbsa_name, get_df_median_home_value, col_name)

    return df_income_percentile_cbsa

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    # df = get_df_housing_values(2020, "MI", "48130")
    # print(df)
    # create_chart_housing_value_shares(df)

    cbsa = "Dallas-Fort Worth-Arlington, TX"

    df = get_df_median_home_price_percentile_cbsa(2020, cbsa)
    df.to_csv("test.csv")

