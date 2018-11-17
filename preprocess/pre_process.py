import pandas

def clean_data(location,method="drop"):
# assigning the NA values for default values
    missingvalues=["NA","N/A","na","n/a"]
    df_raw = pd.read_csv(location,na_values=missingvalues)
#   print the raw data after defaulting the na values
    print (df_raw)
#  converting all the data to float and cleaning any non numeric values
    df_raw=df_raw.replace('[^0-9]','',regex=True).astype(float)
#   print the data with only numeric values 
    print (df_raw)
# method called in if loop for drop or avg
    if method=="drop":
        df_clean=df_raw.fillna(0)
        print("Printing the values after filling the NA values with zero's")
    elif method=="avg":
        df_clean=df_raw.fillna(df_raw.mean())
        print("Printing the values after filling the NA values with average of the column")
    print (df_clean)
    del (df_raw)
    return df_clean
# Test execution
#clean_data("Location","drop")
#clean_data("Location","avg")
#clean_data("Location")
