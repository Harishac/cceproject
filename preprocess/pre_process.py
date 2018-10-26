import pandas

def clean_data(location, method):
    """

    :param location: String location of raw file
    :return: data frame of cleaned data
    """

    df_raw = pandas.read_csv(location)

    """
    add logic to clean data
    """
    df_clean = df_raw #just for testing

    return df_clean