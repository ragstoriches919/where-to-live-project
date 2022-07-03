import raw_data.census.census_data as census
import cfg
import pandas as pd


def get_df_population_stats_by_age(year, state_abbrev, zcta=None):

    df_census_codes = pd.read_csv(cfg.CSV_CENSUS_CODES)

    census_codes_age = list(df_census_codes.loc[df_census_codes["group"] == "B01001"]["census_code"].unique())

    df_census = census.get_df_census_data(census_codes_age, year, state_abbrev, zcta = zcta)

    df_census["Male_<9"] = df_census[['Total:!!Male:!!Under 5 Years Sex By Age', 'Total:!!Male:!!5 To 9 Years Sex By Age']].sum(axis=1)
    df_census["Male_10-19"] = df_census[['Total:!!Male:!!10 To 14 Years Sex By Age', 'Total:!!Male:!!15 To 17 Years Sex By Age', 'Total:!!Male:!!18 And 19 Years Sex By Age']].sum(axis=1)
    df_census["Male_20-29"] = df_census[['Total:!!Male:!!20 Years Sex By Age', 'Total:!!Male:!!21 Years Sex By Age', 'Total:!!Male:!!22 To 24 Years Sex By Age', 'Total:!!Male:!!25 To 29 Years Sex By Age']].sum(axis=1)
    df_census["Male_30-39"] = df_census[['Total:!!Male:!!30 To 34 Years Sex By Age', 'Total:!!Male:!!35 To 39 Years Sex By Age']].sum(axis=1)
    df_census["Male_40-49"] = df_census[['Total:!!Male:!!40 To 44 Years Sex By Age','Total:!!Male:!!45 To 49 Years Sex By Age']].sum(axis=1)
    df_census["Male_50-59"] = df_census[['Total:!!Male:!!50 To 54 Years Sex By Age', 'Total:!!Male:!!55 To 59 Years Sex By Age']].sum(axis=1)
    df_census["Male_60-69"] = df_census[['Total:!!Male:!!60 And 61 Years Sex By Age', 'Total:!!Male:!!62 To 64 Years Sex By Age', 'Total:!!Male:!!65 And 66 Years Sex By Age', 'Total:!!Male:!!67 To 69 Years Sex By Age']].sum(axis=1)
    df_census["Male_70-79"] = df_census[['Total:!!Male:!!70 To 74 Years Sex By Age', 'Total:!!Male:!!75 To 79 Years Sex By Age']].sum(axis=1)
    df_census["Male_>80"] = df_census[['Total:!!Male:!!80 To 84 Years Sex By Age', 'Total:!!Male:!!85 Years And Over Sex By Age']].sum(axis=1)

    df_census["Female_<9"] = df_census[['Total:!!Female:!!Under 5 Years Sex By Age', 'Total:!!Female:!!5 To 9 Years Sex By Age']].sum(axis=1)
    df_census["Female_10-19"] = df_census[['Total:!!Female:!!10 To 14 Years Sex By Age', 'Total:!!Female:!!15 To 17 Years Sex By Age', 'Total:!!Female:!!18 And 19 Years Sex By Age']].sum(axis=1)
    df_census["Female_20-29"] = df_census[['Total:!!Female:!!20 Years Sex By Age', 'Total:!!Female:!!21 Years Sex By Age', 'Total:!!Female:!!22 To 24 Years Sex By Age', 'Total:!!Female:!!25 To 29 Years Sex By Age']].sum(axis=1)
    df_census["Female_30-39"] = df_census[['Total:!!Female:!!30 To 34 Years Sex By Age', 'Total:!!Female:!!35 To 39 Years Sex By Age']].sum(axis=1)
    df_census["Female_40-49"] = df_census[['Total:!!Female:!!40 To 44 Years Sex By Age','Total:!!Female:!!45 To 49 Years Sex By Age']].sum(axis=1)
    df_census["Female_50-59"] = df_census[['Total:!!Female:!!50 To 54 Years Sex By Age', 'Total:!!Female:!!55 To 59 Years Sex By Age']].sum(axis=1)
    df_census["Female_60-69"] = df_census[['Total:!!Female:!!60 And 61 Years Sex By Age', 'Total:!!Female:!!62 To 64 Years Sex By Age', 'Total:!!Female:!!65 And 66 Years Sex By Age', 'Total:!!Female:!!67 To 69 Years Sex By Age']].sum(axis=1)
    df_census["Female_70-79"] = df_census[['Total:!!Female:!!70 To 74 Years Sex By Age', 'Total:!!Female:!!75 To 79 Years Sex By Age']].sum(axis=1)
    df_census["Female_>80"] = df_census[['Total:!!Female:!!80 To 84 Years Sex By Age', 'Total:!!Female:!!85 Years And Over Sex By Age']].sum(axis=1)

    return df_census


def get_df_population_stats_by_race(year, state_abbrev, zcta=None):

    df_census_codes = pd.read_csv(cfg.CSV_CENSUS_CODES)

    census_codes_race = list(df_census_codes.loc[df_census_codes["group"] == "B02001"]["census_code"].unique())
    census_codes_race.append("B03001_003E")

    df_census = census.get_df_census_data(census_codes_race, year, state_abbrev, zcta=zcta)

    return df_census


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    pass

    df = get_df_population_stats_by_race(2019, "CT", zcta="06074")
    df.to_csv('test.csv')
    #
    # census.get_df_census_data(["B02001_009E"], 2019, "CT")