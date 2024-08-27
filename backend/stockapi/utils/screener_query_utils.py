import json
import os
from io import StringIO

import pandas as pd

COOKIE_gourab = '_ga=GA1.2.1086773364.1670509017; ajs_user_id=m1xia7GWSwR5nyhh1SCGfJUixM43; ajs_anonymous_id=d202f68e-57ed-4aaa-a4b6-39c089bc39bd; csrftoken=nlVFLQ2kHGEOFmr2Nnub8riSDnMqlr6t; sessionid=ia2or2j8yy191epigi80obum3fokwiqs'
CSRF_gourab = "mzECIAEMEcdnNyE2agpghNITSfFazX94zKp7jgwWbIH1iKVUNtJhf4QBlshqKe5n"


def check_gourab_cookie():
    print('sending gourab cookie')
    return COOKIE_gourab


def check_gourab_csrftoken():
    return CSRF_gourab


def clean_BSE(df):
    # Assuming df is the DataFrame you are working with
    # Apply a lambda function to convert each entry to an integer and then to a string,
    # leaving NaN values untouched.
    df['BSE Code'] = df['BSE Code'].apply(lambda x: str(int(x)) if pd.notnull(x) else x)
    return df


def get_screener_util_folder_path():
    return '../../resources/masterdata/'


def get_screener_query_mcap_file():
    screener_util_folder_path = get_screener_util_folder_path()
    if not os.path.exists(screener_util_folder_path):
        os.makedirs(screener_util_folder_path)
    return os.path.join(screener_util_folder_path, 'screener_mcap.csv')


def get_url_suffix(low, high):
    """
    Generates a URL suffix based on provided low and high values for Market Capitalization.

    Parameters:
    - low: The lower limit for Market Capitalization.
    - high: The upper limit for Market Capitalization.

    Returns:
    - A string containing the URL suffix.
    """
    return f"https://www.screener.in/api/export/screen/?sort=&order=&source=&query=Market+Capitalization+%3E+{low}+AND%0D%0AMarket+Capitalization+%3C{high}"


def get_full_url(url_suffix, url_name="raw_query"):
    """
    Appends the url_name parameter to the given URL suffix.

    Parameters:
    - url_suffix: The URL suffix to which the url_name will be appended.
    - url_name: The name of the URL to be appended. Defaults to 'raw_query'.

    Returns:
    - A string containing the full URL.
    """
    return f"{url_suffix}&url_name={url_name}"


def generate_url(x):
    try:
        if pd.notna(x):
            # Convert to float then to int if the value is numeric
            return f'https://www.screener.in/company/{int(float(x))}/consolidated/'
        else:
            return None
    except ValueError:
        # Handle non-numeric values, such as 'RAJVIR'
        return f'https://www.screener.in/company/{x}/consolidated/'


def check_input_if_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        return False
    else:
        return True


def download_to_merged(df):
    try:
        if_dataframe = check_input_if_dataframe(df)

        if not if_dataframe:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(df)

        # Check if 'BSE Code' and 'NSE Code' columns are present
        if 'BSE Code' in df.columns and 'NSE Code' in df.columns:
            # Create a new column 'Merged_data' and fill it with data from 'NSE Code'; if empty, use data from 'BSE
            # Code'
            df['Merged_data'] = df['NSE Code'].fillna(df['BSE Code'])

            return df
        else:
            print("Required columns ('BSE Code', 'NSE Code') not found.")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


def check_for_lapsed_cookie(soup):
    # Check for specific text in the title tag
    title_text = soup.title.string if soup.title else ""
    if "Register - Screener" in title_text or "Login - Screener" in title_text:
        cookie = input("Cookie does not work, please enter a new cookie: ")
        return False
    else:
        return True


def get_data_as_dataframe(response):
    # Check if the request was successful
    if response.status_code == 200:
        # Check the format of the response and convert accordingly
        try:
            # Attempt to load the response as JSON
            json_data = response.json()
            df = pd.DataFrame(json_data)
        except json.JSONDecodeError:
            # If it fails, treat response as CSV
            df = pd.read_csv(StringIO(response.text))
        return df
    else:
        print("error Failed to retrieve data: Status code", response.status_code)
        return None
