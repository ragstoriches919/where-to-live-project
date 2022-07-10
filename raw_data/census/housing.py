import raw_data.census.census_data as census
import pandas as pd
import cfg


def get_df_housing_values(year, state_abbrev, zcta=None):

    group = "B25075"

    census_codes_housing_values = census.get_list_census_codes_by_group(group)
    df_housing_values = census.get_df_census_data(census_codes_housing_values, year, state_abbrev, zcta=zcta)

    for column in df_housing_values.columns:
        print(column)

    df_housing_values["housing_value_<100k"] = df_housing_values['Total:!!Less Than $10,000 Value'] + \
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

    df_housing_values["housing_value_100k-200k"] = df_housing_values['Total:!!$100,000 To $124,999 Value'] + \
                                                   df_housing_values['Total:!!$125,000 To $149,999 Value'] + \
                                                   df_housing_values['Total:!!$150,000 To $174,999 Value'] + \
                                                   df_housing_values['Total:!!$175,000 To $199,999 Value']

    df_housing_values["housing_value_200k-300k"] = df_housing_values['Total:!!$200,000 To $249,999 Value'] + \
                                                   df_housing_values['Total:!!$250,000 To $299,999 Value']

    df_housing_values["housing_value_300k-400k"] = df_housing_values['Total:!!$300,000 To $399,999 Value']

    df_housing_values["housing_value_400k-500k"] = df_housing_values['Total:!!$400,000 To $499,999 Value']
    df_housing_values["housing_value_500k-750k"] = df_housing_values['Total:!!$500,000 To $749,999 Value']
    df_housing_values["housing_value_750k-1mio"] = df_housing_values['Total:!!$750,000 To $999,999 Value']
    df_housing_values["housing_value_1mio-1.5mio"] = df_housing_values['Total:!!$1,000,000 To $1,499,999 Value']
    df_housing_values["housing_value_1.5mio-2mio"] = df_housing_values['Total:!!$1,500,000 To $1,999,999 Value']
    df_housing_values["housing_value_>2mio"] = df_housing_values['Total:!!$2,000,000 Or More Value']

    return df_housing_values


def get_df_median_home_value(year, state_abbrev, zcta=None):

    group = "B25077"
    census_codes_median_value = census.get_list_census_codes_by_group(group)
    df_median_value = census.get_df_census_data(census_codes_median_value, year, state_abbrev, zcta=zcta)

    return df_median_value

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    df = get_df_median_home_value(2020, "MI", "48130")
    print(df)
