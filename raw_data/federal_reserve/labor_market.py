import fred_data

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def helper_find_indeed_postings_ids():

    s_indeed = "Job Postings on Indeed in"
    s_msa = "(MSA)"
    df_search = fred_data.search_for_ids_by_category(33509)
    df_search = df_search.loc[df_search["title"].str.contains(s_indeed)]
    df_search = df_search.loc[df_search["title"].str.contains(s_msa)]

    fred_ids = df_search["id"].unique()
    return fred_ids

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_indeed_job_postings(start_date=None, end_date=None):

    """
    Gets Case-Shiller home price indices
    :param: start_date: String Ex.) "2020-01-01"
    :param: end_date: String Ex.) "2020-12-31"
    :return: DataFrame
    """

    indeed_postings_ids = helper_find_indeed_postings_ids()
    df_case_shiller_info = fred_data.get_df_series_data(indeed_postings_ids, start_date=start_date, end_date=end_date)
    df_case_shiller_info.to_csv('test.csv')

    return df_case_shiller_info


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":#

    print(helper_find_indeed_postings_ids())

    # get_df_indeed_job_postings()