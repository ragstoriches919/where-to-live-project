import os

API_KEY_CENSUS = r"4715d5f869c5ebbad9f7a58d3fd8deb1ff0401a8"
API_KEY_OPENSTATES = r"ed531324-579a-4ef6-ad87-4cee13663e25"
NOAA_TOKEN = r"kOKWxjRWxlMRqNUUwihFmRXklcbIDqeZ"
API_KEY_DEPT_OF_EDUCATION = r"4GY0IRhzc3so1dsySovTIVrboBCgIiHwmgLDSnjr"
API_KEY_FBI = r"QWuUj9UyWMs08syMCw8xCr7YOhgKBX2mraW7uEaY"
API_KEY_NATIONAL_PARK_SERVICE = r"4lRbwQhgq6wl5bD0ul1QkIJwzsU45zFkU9rEXaY7"
API_KEY_FRED = r"034fc1b6454fa9083ed93717e82ff531"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_CENSUS_CODES = os.path.join(ROOT_DIR, "helper_data", "census_codes.csv")
CSV_STATE_CODES = os.path.join(ROOT_DIR, "helper_data", "state_codes.csv")
CSV_ZTCA_TO_MSA = os.path.join(ROOT_DIR, "helper_data", "ztca_to_msa.csv")
CSV_ZIP_CODE_TO_COORDS = os.path.join(ROOT_DIR, "helper_data", "zip_code_to_coordinates.csv")
CSV_ZIPCODE_TO_ZCTA = os.path.join(ROOT_DIR, "helper_data", "zip_code_to_zcta_2021.csv")
CSV_ZIPCODE_TO_COUNTY = os.path.join(ROOT_DIR, "helper_data", "zip_to_county_crosswalk.csv")
CSV_ZIPCODE_TO_SUB_COUNTY = os.path.join(ROOT_DIR, "helper_data", "zip_to_subcounty_crosswalk.csv")
CSV_CBSA_CODE_MAPPINGS_FROM_USPTO = os.path.join(ROOT_DIR, "helper_data", "cbsa_code_mappings_from_uspto.csv")
CSV_CBSA_CODE_MAPPINGS_FROM_OMB = os.path.join(ROOT_DIR, "helper_data", "cbsa_code_mappings_from_omb.csv") # Better source
CSV_ZIPCODE_TO_CBSA = os.path.join(ROOT_DIR, "helper_data", "zip_to_cbsa.csv")
CSV_CBSA_STATES = os.path.join(ROOT_DIR, "helper_data", "csba_states_mapping.csv")
CSV_ZIP_CODE_MAPPINGS_COMPLETE = os.path.join(ROOT_DIR, "helper_data", "zip_code_mappings_complete.csv")

CSV_FIP_CODES = os.path.join(ROOT_DIR, "helper_data", "fip_codes.csv")

GEOJSON_VOTING_RESULTS = os.path.join(ROOT_DIR, "raw_data", "voting", "voting_data", "voting_results_2020_election.geojson")
