import raw_data.census.census_data as census
import pandas as pd
import cfg

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_internet_by_zip():

    url = r"https://raw.githubusercontent.com/BroadbandNow/Open-Data/master/broadband_data_opendatachallenge.csv"
    df_internet = pd.read_csv(url, encoding='latin-1')
    df_internet["Zip"] = df_internet["Zip"].astype(str).apply(lambda x: "0" + str(x) if int(x) < 10000 else str(x))

    print(df_internet)
    return df_internet


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    get_df_internet_by_zip()
