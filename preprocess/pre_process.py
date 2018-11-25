import pandas as pd
import numpy as np

def clean_data(location,method="drop"):

    missingvalues=["NA","N/A","na","n/a"]
    df_raw = pd.read_csv(location,na_values=missingvalues,header=None, skiprows=1)
    df_raw=df_raw.replace('[^0-9]','',regex=True).astype(float)
 
    if method=="drop":
        df_method=df_raw.dropna(how='any')

    elif method=="avg":
        df_method=df_raw.fillna(df_raw.mean())

    df_method=df_method.reset_index(drop=True)

    stds = 1.0
    lenloc=len(df_method.columns)
    if lenloc==1:
        df_method.columns=['Y']
        df_outliers=df_method
    elif lenloc==2:
        df_method.columns=['Y','X1']
        outliers = df_method[['X1']].transform(lambda group: (group - group.mean()).abs().div(group.std())) > stds  
        df_outliers=df_method[outliers.any(axis=1)]
    elif lenloc==3:
        df_method.columns=['Y','X1','X2']
        outliers = df_method[['X1','X2']].transform(lambda group: (group - group.mean()).abs().div(group.std())) > stds  
        df_outliers=df_method[outliers.any(axis=1)]
    elif lenloc==4:
        df_method.columns=['Y','X1','X2','X3']
        outliers = df_method[['X1','X2','X3']].transform(lambda group: (group - group.mean()).abs().div(group.std())) > stds  
        df_outliers=df_method[outliers.any(axis=1)]
    if lenloc==1:
        df_clean=df_method
        df_outliers=[]
    else:
        df_clean=pd.concat([df_method,df_outliers]).drop_duplicates(keep=False)

    return df_clean,df_outliers

