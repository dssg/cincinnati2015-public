from datetime import datetime

import pandas as pd
from pandas.util import testing


def iso_date(date_str):
    date_str = datetime.strptime(date_str, '%d%b%Y')
    return date_str.isoformat()


def date(date_str):
    return datetime.strptime(date_str, '%d%b%Y')

def timestamp(date_str):
    d = datetime.strptime(date_str, '%d%b%Y')
    return pd.to_datetime(d)

def assert_frame_equal(expected_df, actual_df):
    expected_df = expected_df.copy().sort(axis=1).sort(axis=0)
    actual_df = actual_df.copy().sort(axis=1).sort(axis=0)
    testing.assert_frame_equal(expected_df, actual_df, check_names=True)
