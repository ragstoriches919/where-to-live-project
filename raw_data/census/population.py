import raw_data.census.census_data as census
import cfg
import pandas as pd


def get_df_population_stats_by_age(year, state_abbrev, zcta=None):

    """
    Returns population stats by age
    :param year: Integer
    :param state_abbrev: String Ex.) "CT"
    :param zcta: String Ex.) "06074"
    :return: DataFrame
    """

    group = "B01001"
    census_codes_age = census.get_list_census_codes_by_group(group)
    df_population = census.get_df_census_data(census_codes_age, year, state_abbrev, zcta = zcta)

    df_population["Male_<9"] = df_population[['Total:!!Male:!!Under 5 Years Sex By Age', 'Total:!!Male:!!5 To 9 Years Sex By Age']].sum(axis=1)
    df_population["Male_10-19"] = df_population[['Total:!!Male:!!10 To 14 Years Sex By Age', 'Total:!!Male:!!15 To 17 Years Sex By Age', 'Total:!!Male:!!18 And 19 Years Sex By Age']].sum(axis=1)
    df_population["Male_20-29"] = df_population[['Total:!!Male:!!20 Years Sex By Age', 'Total:!!Male:!!21 Years Sex By Age', 'Total:!!Male:!!22 To 24 Years Sex By Age', 'Total:!!Male:!!25 To 29 Years Sex By Age']].sum(axis=1)
    df_population["Male_30-39"] = df_population[['Total:!!Male:!!30 To 34 Years Sex By Age', 'Total:!!Male:!!35 To 39 Years Sex By Age']].sum(axis=1)
    df_population["Male_40-49"] = df_population[['Total:!!Male:!!40 To 44 Years Sex By Age','Total:!!Male:!!45 To 49 Years Sex By Age']].sum(axis=1)
    df_population["Male_50-59"] = df_population[['Total:!!Male:!!50 To 54 Years Sex By Age', 'Total:!!Male:!!55 To 59 Years Sex By Age']].sum(axis=1)
    df_population["Male_60-69"] = df_population[['Total:!!Male:!!60 And 61 Years Sex By Age', 'Total:!!Male:!!62 To 64 Years Sex By Age', 'Total:!!Male:!!65 And 66 Years Sex By Age', 'Total:!!Male:!!67 To 69 Years Sex By Age']].sum(axis=1)
    df_population["Male_70-79"] = df_population[['Total:!!Male:!!70 To 74 Years Sex By Age', 'Total:!!Male:!!75 To 79 Years Sex By Age']].sum(axis=1)
    df_population["Male_>80"] = df_population[['Total:!!Male:!!80 To 84 Years Sex By Age', 'Total:!!Male:!!85 Years And Over Sex By Age']].sum(axis=1)

    df_population["Female_<9"] = df_population[['Total:!!Female:!!Under 5 Years Sex By Age', 'Total:!!Female:!!5 To 9 Years Sex By Age']].sum(axis=1)
    df_population["Female_10-19"] = df_population[['Total:!!Female:!!10 To 14 Years Sex By Age', 'Total:!!Female:!!15 To 17 Years Sex By Age', 'Total:!!Female:!!18 And 19 Years Sex By Age']].sum(axis=1)
    df_population["Female_20-29"] = df_population[['Total:!!Female:!!20 Years Sex By Age', 'Total:!!Female:!!21 Years Sex By Age', 'Total:!!Female:!!22 To 24 Years Sex By Age', 'Total:!!Female:!!25 To 29 Years Sex By Age']].sum(axis=1)
    df_population["Female_30-39"] = df_population[['Total:!!Female:!!30 To 34 Years Sex By Age', 'Total:!!Female:!!35 To 39 Years Sex By Age']].sum(axis=1)
    df_population["Female_40-49"] = df_population[['Total:!!Female:!!40 To 44 Years Sex By Age','Total:!!Female:!!45 To 49 Years Sex By Age']].sum(axis=1)
    df_population["Female_50-59"] = df_population[['Total:!!Female:!!50 To 54 Years Sex By Age', 'Total:!!Female:!!55 To 59 Years Sex By Age']].sum(axis=1)
    df_population["Female_60-69"] = df_population[['Total:!!Female:!!60 And 61 Years Sex By Age', 'Total:!!Female:!!62 To 64 Years Sex By Age', 'Total:!!Female:!!65 And 66 Years Sex By Age', 'Total:!!Female:!!67 To 69 Years Sex By Age']].sum(axis=1)
    df_population["Female_70-79"] = df_population[['Total:!!Female:!!70 To 74 Years Sex By Age', 'Total:!!Female:!!75 To 79 Years Sex By Age']].sum(axis=1)
    df_population["Female_>80"] = df_population[['Total:!!Female:!!80 To 84 Years Sex By Age', 'Total:!!Female:!!85 Years And Over Sex By Age']].sum(axis=1)

    return df_population


def get_df_population_stats_by_race(year, state_abbrev, zcta=None):

    group = "B02001"
    census_codes_race = census.get_list_census_codes_by_group(group)
    census_codes_race.append("B03001_003E")

    df_race = census.get_df_census_data(census_codes_race, year, state_abbrev, zcta=zcta)
    df_race = df_race.rename(
        columns={"Total:!!White Alone Race":"white",
                 "Total:!!Black Or African American Alone Race": "black", "Total:!!Asian Alone Race": "asian",
                 "Total:!!Native Hawaiian And Other Pacific Islander Alone Race": "pacific_islander",
                 "Total:!!Some Other Race Alone Race": "other", "Total:!!Two Or More Races: Race": "2+",
                 "Total:!!Hispanic Or Latino: Hispanic Or Latino Origin By Specific Origin": "hispanic", "Total:!!American Indian And Alaska Native Alone Race": "native_american"})

    df_race["white"] = df_race["white"] - df_race['hispanic']

    df_race = df_race.drop(
        columns=["Total:!!Two Or More Races:!!Two Races Excluding Some Other Race, And Three Or More Races Race",
                 "Total:!!Two Or More Races:!!Two Races Including Some Other Race Race"])

    return df_race


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    pass

    df = get_df_population_stats_by_race(2020, "CT", zcta="06074")
    df.to_csv('test.csv')


