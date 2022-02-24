import pandas as pd
url_fhfa = r"https://www.fhfa.gov/DataTools/Downloads/Documents/HPI/HPI_PO_metro.xls"


def get_df_fhfa_data():

    df_fhfa = pd.read_excel(url_fhfa)
    df_fhfa["cbsa"] = df_fhfa["cbsa"].astype(str)

    return df_fhfa


df = get_df_fhfa_data()
print(df)
