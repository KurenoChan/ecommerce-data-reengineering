import pandas as pd


def remove_duplicates(df):
    df = df.copy()

    before = df[df.duplicated(keep=False)]
    after = df.drop_duplicates()

    return after, before