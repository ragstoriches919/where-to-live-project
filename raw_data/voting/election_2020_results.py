import cfg
import pandas as pd
import numpy as np
import json
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PICKLE_2020_ELECTION = os.path.join(cfg.ROOT_DIR, "raw_data/voting/pickled_files/election_2020_results.pkl")

# Reference: https://github.com/TheUpshot/presidential-precinct-map-2020


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_df_voting_results_2020():

    with open(cfg.GEOJSON_VOTING_RESULTS) as f:
        d = json.load(f)
        df_votes = pd.json_normalize(d["features"])
        df_votes = df_votes.drop(columns=["type", "properties.votes_per_sqkm", "properties.pct_dem_lead", "geometry.type",
                              "geometry.coordinates"])
        df_votes["fips"] = df_votes["properties.GEOID"].str[:5]
        df_votes["precinct_name"] = df_votes["properties.GEOID"].str[5:].apply(lambda x: x.strip())

        df_fips = pd.read_csv(cfg.CSV_FIP_CODES)
        df_fips["CountyFIPS"] = df_fips["CountyFIPS"].astype(str).apply(lambda x: "0" + str(x) if int(x) < 10000 else str(x))
        df_votes = pd.merge(df_votes, df_fips, left_on="fips", right_on="CountyFIPS", how='left')

        df_votes.to_pickle(PICKLE_2020_ELECTION)

    return df_votes

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    # get_df_voting_results_2020()

    df = pd.read_pickle(PICKLE_2020_ELECTION)
    print(df)