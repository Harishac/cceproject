import pandas as pd  
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000      
pd.options.mode.chained_assignment = None      
import math

#row indexes for easy reference
mean = "Mean"                   
var = "Variance"                
sd = "Standard Deviation"       
covar = "Co-variance"          
cor = "Correlation Factor"      
rsig = "Is r significant?"
#partialr = "Partial Correlation Factor"

def read_csv_into_df(file_path):
    #print(file_path)

    #read the CSV and store in dataframe 'df'
    my_df = pd.read_csv(file_path)

    #print the dataframe
    #print("Data Frame: \n")
    #print(my_df)
    
    #return the dataframe read
    return my_df


def training_data(df):
    count = get_count(df)
    x_train= int(0.7 * count)
    return(df.iloc[0:x_train])

def testing_data(df):
    count = get_count(df)
    x_train= int(0.7 * count)
    df_test = df.iloc[x_train:]
    df_test.reset_index(drop=True, inplace=True)
    return(df_test)


def df_to_dict(df):
    return (df.to_dict('index'))


def dict_to_df(dict):
    df = pd.DataFrame.from_dict(dict, orient='index')
    return df


def get_count(my_df):
    my_count = 0
    for i in my_df.index:
        #print(i)
        my_count = my_count + 1

    #print("\nRecord Count: " + str(my_count))

    return my_count


def get_sum( my_df, my_col_name):
    my_col_sum = 0 
    for i in my_df.index:
        #print(my_df.iloc[i][my_col_name])
        my_col_sum = my_col_sum + my_df.iloc[i][my_col_name]

    #print("\nSum of " + my_col_name + ": " + str(my_col_sum))

    return my_col_sum



def get_mean(statistic_df, my_df, my_col_name):
    my_count = get_count(my_df)
    my_sum = get_sum(my_df,my_col_name)
    my_mean = my_sum / my_count

    statistic_df.loc[mean][my_col_name] = my_mean

    return my_mean



def get_SD(statistic_df, my_df, my_col_name):
    my_count = get_count(my_df)
    my_mean = get_mean(statistic_df, my_df, my_col_name)
    my_sum_of_squares = 0
    
    for i in my_df.index:
        my_sum_of_squares = my_sum_of_squares + ( (my_df.iloc[i][my_col_name] - my_mean) * (my_df.iloc[i][my_col_name] - my_mean))

    my_variance = my_sum_of_squares / (my_count - 1)
    my_sd = math.sqrt(my_variance)

    statistic_df.loc[var][my_col_name] = my_variance
    statistic_df.loc[sd][my_col_name]  = my_sd

    return my_sd


def get_covariance(statistic_df, my_df, my_col_name_x, my_col_name_y):
    my_count = get_count(my_df)
    my_mean_x = get_mean(statistic_df, my_df, my_col_name_x)
    my_mean_y = get_mean(statistic_df, my_df, my_col_name_y)

    my_sum_of_products = 0 
    for i in my_df.index:
        my_sum_of_products = my_sum_of_products + ( (my_df.iloc[i][my_col_name_x] - my_mean_x) * (my_df.iloc[i][my_col_name_y] - my_mean_y))

    my_covariance = my_sum_of_products / (my_count - 1)
    statistic_df.loc[covar][my_col_name_x] = my_covariance

    return my_covariance



def get_r(statistic_df, my_df, my_col_name_x, my_col_name_y):
    my_count = get_count(my_df)
    my_sd_x = get_SD(statistic_df, my_df, my_col_name_x, )
    my_sd_y = get_SD(statistic_df, my_df, my_col_name_y)
    my_covariance = get_covariance(statistic_df, my_df, my_col_name_x, my_col_name_y)

    r =  my_covariance / (my_sd_x * my_sd_y)
    r_significant = 1.96 / math.sqrt(my_count)

    statistic_df.loc[cor][my_col_name_x] = r

    if(r >= r_significant or r <= (-1 * r_significant) ):
        statistic_df.loc[rsig][my_col_name_x] = "Yes"
    else:
        statistic_df.loc[rsig][my_col_name_x] = "No"
    
	


def calculate_statistics(df):
    
    #define statistics df
    #finding number of columns in input dataframe
    l = len(df.columns)

    col_name_y = df.columns[0]  #we are assuming the dependent variable (y) will be the first column in the file

    #column headers for statistics df  
    statistics_header = []
    for i in range(0,l):        
        statistics_header.append(df.columns[i])
                
    #row indexes for statistics df
    statistics_index = []
    statistics_index.append("Mean")
    statistics_index.append("Variance") 
    statistics_index.append("Standard Deviation")
    statistics_index.append("Co-variance") 
    statistics_index.append("Correlation Factor") 
    statistics_index.append("Is r significant?") 
    #statistics_index.append("Partial Correlation Factor")

    #creating a dataframe to store statistics
    statistic_df = pd.DataFrame(index = statistics_index, columns = statistics_header)

    #for each independent variables,
    #finding r, and in the process, mean, var, SD, covar and rsig
    for i in range(1,l):   
        get_r(statistic_df, df, df.columns[i], col_name_y)


    #for dependent variable
    temp = get_mean(statistic_df, df, col_name_y)
    temp = get_SD(statistic_df, df, col_name_y)
    #y values will be "-" for 3 (covariance),4 (r),5 (partial r)
    statistic_df.loc[covar][col_name_y]    = "-"
    statistic_df.loc[cor][col_name_y]      = "-"
    statistic_df.loc[rsig][col_name_y]     = "-"
    #statistic_df.loc[partialr][col_name_y] = "-"

    #hardcoding for testing
    #statistic_df.loc[rsig][2] = "Yes"
    #statistic_df.loc[rsig][3] = "Yes"
    #print("a1 = " + str(a1)+"\nb1 = "+str(b1)+"\nc1 = "+str(c1)+"\na2 = "+str(a2)+"\nb2 = "+str(b2)+"\nc2 = "+str(c2)+"\nk = "+str(k))

    #print("\n\nStatistics calculated:\n")
    #print(statistic_df)

    count = get_count(df)
    r_significant = 1.96 / math.sqrt(count)
    statistic_df.loc[cor][col_name_y] = r_significant
    #print("\nThresold for r to be signficant is: +-"+str(r_significant))
    #print("\n\n")

    return(statistic_df)

 

def solve_eqn(rc, total_n, n, rdf):

    #print("\n\nn: "+str(n))

    if(n == 1):                 #rdf will be 1*2
        y = rdf.iloc[0][1]/rdf.iloc[0][0]           
        rc[total_n - n] = y

    else: #we get df of n * n+1
        k = [None] * (n - 1)
        
        #Step 1: Finding ks

        #eliminates the first variable (a)
        #in range functions, the last number (that is, n-1 is not included)
        #print("\nStep 1: Finding k... (n = "+str(n)+")")
        for i in range(0,n-1):          #0,1,2... n-2 
            #print(rdf.iloc[i+1][0])
            #print(rdf.iloc[0][0]) 
            k[i] = rdf.iloc[i+1][0]/rdf.iloc[0][0]
            #print("k[" + str(i) + "]: " + str(k[i]))

        #print("k values: " + str(k))

        #Step 2: Finding new matrix

        #reduce df to n-1 * n after eliminating one variable
        rdf_new = pd.DataFrame(index=range(0,n-1),columns=range(0,n), dtype='float')
        #print("\nStep 2: Entering loop to calculate new regression matrix...(n = "+str(n)+")")
        #print(rdf_new)
        #print("n-2: " + str(n-2) + "\tn-1: " + str(n-1))
        
        for i in range(0,n-1):          #0,1,... n-2
            #print("\ni: "+str(i))
            for j in range (0, n):      #0,1,....n-1
                #print("j : "+str(j))
                #print("k[i] : " + str(k[i]))
                #print("rdf.iloc[0][j+1] : " + str(rdf.iloc[0][j+1]))
                #print("rdf.iloc[i+1][j+1] : " + str(rdf.iloc[i+1][j+1]))
                rdf_new.iloc[i][j] = (k[i] * rdf.iloc[0][j+1]) - rdf.iloc[i+1][j+1]

        #print("\nNew Regression Matrix (n = "+str(n-1)+") :")
        #print(rdf_new)
        

        #Step 3: Recursive Call
        #print("\nStep 3: Recursively calling  solve_eqn (n = "+str(n-1)+")...")
        solve_eqn(rc, total_n, n-1, rdf_new)
        

        #Step 4: Finding coefficients
        #print("\nStep 4: Calculating regression coefficient (n = "+str(n-1)+") :")
        #calculating and saving the regression coefficient 

        m = total_n - n + 1
        rc[total_n - n] = rdf.iloc[0][n]
        #print("global_rc[global_n - n]: " + str(global_rc[global_n - n]))
        for i in range(0,n-1):          #0,1,....n-2
            #print("\ni :" + str(i))
            #print("rdf.iloc[0][i+1] : " + str(rdf.iloc[0][i+1]))
            #print("global_rc[i+m] : "+str(global_rc[i+m]))
            rc[total_n - n]  = rc[total_n - n] - (rdf.iloc[0][i+1] * rc[i+m]) 
        rc[total_n - n] = rc[total_n - n]  / rdf.iloc[0][0]    

    #print("Regression coefficients so far (n = "+ str(n) +"): \n" + str(rc))


	
def get_regression_coeff(statistic_df, df): 
    #k is used to store the number of independent columns where there is a significant correlation with y
    count = get_count(df) 
    l = len(df.columns)
    col_name_y = df.columns[0]
    k = 0 
    sig_column_names = []

    #looping through each independent variable
    for i in range(1,l):             
        #print(statistic_df.loc[rsig][df.columns[i]])
        if (statistic_df.loc[rsig][df.columns[i]] == "Yes"):
            k = k + 1
            sig_column_names.append(df.columns[i])

    n = k + 1

    #print("Regression Equation:\n")
    #print("Number of significant variables considered = "+ str(k))

    #list which stores the final coefficients 
    rc = [None] * n
    #print("\n\nRegression Coefficients Initially:")
    #print(rc)
    #print("\n")

    #based on value of k, getting the coefficients for regression equations
    if(k == 0):
        print("'y' does not have a significant linear relation with any of the input fields.")

    else:
        #creating n * (n+1) dataframe and initialising all elements to 0
        rdf = pd.DataFrame(0, index = range(0, n), columns = range(0, n + 1))
        
        #populating the different elements of matrix - 3 loops
        for i in range(0,n):                     #loop 1: row wise
            for j in range(0,n +1):              #loop 2: column wise
                for p in range(0, count):               #loop 3: for each row in dataset 

                    if(i == 0 and j == n - 1):
                        rdf.iloc[i][j] = rdf.iloc[i][j] + 1

                    elif(i == 0 and j == n):
                        rdf.iloc[i][j] = rdf.iloc[i][j] + (1 * df.iloc[p][col_name_y])

                    elif(i == 0):
                        rdf.iloc[i][j] = rdf.iloc[i][j] + (1 * df.iloc[p][sig_column_names[j]])

                    elif(j == n - 1 ):
                        rdf.iloc[i][j] = rdf.iloc[i][j] + (df.iloc[p][sig_column_names[i-1]] * 1)

                    elif(j == n):
                        rdf.iloc[i][j] = rdf.iloc[i][j] + (df.iloc[p][sig_column_names[i-1]] * df.iloc[p][col_name_y])

                    else:
                        rdf.iloc[i][j] = rdf.iloc[i][j] + (df.iloc[p][sig_column_names[i-1]] * df.iloc[p][sig_column_names[j]])


        #print("\nRegression Matrix (n = " + str(n) + ") :")
        #print(rdf)

        #calling function to get m1,m2,...mk, c in the gloval variable - rc
        solve_eqn(rc, n, n, rdf)
        #print(rc)

        #forming the regression equation string
        generic_eqn = "y = "
        my_eqn = col_name_y + " = "

        #print("k = " + str(k))
        for i in range(0,k):                    #0,1,2....k-1
            #print(i)
            #print(sig_column_names[i])
            generic_eqn = generic_eqn + str(round(rc[i],3)) + " * x" + str(i+1) + " + "
            my_eqn = my_eqn + str(round(rc[i],3)) + " * " + sig_column_names[i] + " + "

        generic_eqn = generic_eqn + str(round(rc[k],3))
        my_eqn = my_eqn + str(round(rc[k],3))

        #print("\nTherefore, Regression equation is: ")
        #print(generic_eqn)
        #print(my_eqn)

    #print("\n\n")
    return rc


def calculated_expected_values(df, coeff, statistic_df):

    #print(coeff)
        
    df_output = df
    l = len(df.columns)             #Number of columns
    count = get_count(df)           #Number of rows
    k = 0
    col_name_y = df.columns[0]
    expected_value_column_name = "Expected value of " + col_name_y
    sig_column_names = []

    if(coeff == [None]):
        df_output[expected_value_column_name] = None
        return df_output

    #get only column names where r is significant
    for i in range(1,l):             
        if (statistic_df.loc[rsig][df.columns[i]] == "Yes"):
            k = k + 1
            sig_column_names.append(df.columns[i])

    
    expected_values = [0.0] *  count

    #print(expected_values)
    #print("coeff(k): " + str(coeff[k]))
    for i in df_output.index:           #for each row
        #print("i : " + str(i))

        for j in range(0,k):            #for each significant column
            #print(str((df_output.loc[i][sig_column_names[j]]) * coeff[j]))
            expected_values[i] = expected_values[i] + (df_output.loc[i][sig_column_names[j]] * coeff[j])
            #print(expected_values[i])
        expected_values[i] = expected_values[i] + coeff[k]

    df_output[expected_value_column_name] = expected_values
    #print(df_output)

    return df_output
