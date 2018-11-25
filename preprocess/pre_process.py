import pandas as pd
import numpy as np

def clean_data(location,method="drop"):
    missingvalues=["NA","N/A","na","n/a"]
    df_raw = pd.read_csv(location,na_values=missingvalues)
    df_raw=df_raw.replace('[^0-9]','',regex=True).astype(float)
    #print(df_raw)
    if method=="drop":
        df_method=df_raw.dropna(how='any')
        #print("****Printing the values after filtering the NA****")
    elif method=="avg":
        df_method=df_raw.fillna(df_raw.mean())
    df_method=df_method.fillna(df_raw.mean())
    #print (df_method)
    Q1 = df_method.quantile(0.25)
    Q3 = df_method.quantile(0.75)
    IQR = Q3 - Q1
    #print(IQR)
    df_clean = df_method[~((df_method < (Q1 - 1.5 * IQR)) |(df_method > (Q3 + 1.5 * IQR))).any(axis=1)]
    #print(df_method_out)
    df_outliers=pd.concat([df_method,df_clean]).drop_duplicates(keep=False)
    return df_clean,df_outliers
