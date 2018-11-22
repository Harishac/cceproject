import pandas

def clean_data(location, method):
    """

    :param location: String location of raw file
    :return: data frame of cleaned data
    """

    df_raw = pandas.read_csv(location)

    """
  import pandas as pd
  import numpy as np

  df_raw=pd.read_csv('Source/test1.csv')
  df1=df_raw.replace('[^0-9]','',regex=True).astype(float)
  df2=df1.fillna(df1.mean())
  clean_data=df2
  print(clean_data)
    """
    df_clean = clean_data

    return df_clean
