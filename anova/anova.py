import json
import pandas as pd  
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000           
import math
#import anova_code
import anova_linear
import anova_square

def anova(df, stats):
    #changes done here
    anova_result={}
    coeff = stats["coeff"]
    orginal_df = df.copy()
    return_df = df.copy()
    anova_result={"Linear":anova_linear.annova(df,coeff)}
    #print(anova_result)
    anova_result.update({"Square":anova_square.anova(orginal_df)})
    if((anova_result["Linear"]["F_Stat"])>(anova_result["Square"]["F_Stat"])):
        anova_result["Linear"]["Significant"]="Yes"
        anova_result["Square"]["Significant"]="No"
	return_df = df
    else:
        anova_result["Linear"]["Significant"]="No"
        anova_result["Square"]["Significant"]="Yes"
	return_df= orginal_df
    return anova_result, return_df

if __name__== "__main__":
    print(anova_result)
    with open('result.json', 'w') as fp:     
        json.dump(anova_result, fp)
    
    print("JSON file created")
