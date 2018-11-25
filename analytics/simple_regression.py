import pandas as pd
import regression_functions as rf       #all functions are defined in this file

class simple_regression(object):
    def __init__(self):
        pass

    @staticmethod
    def train(df_input):
        """
        :param df_input: A pandas dataframe
        :return:
        """

        try:
            
            ##############################################################################
            # Taking only training data
            ##############################################################################
                        
            #training data - take only 70%        
            df_train = rf.training_data(df_input)

            ##############################################################################
            # Statisitcs related code
            ##############################################################################
            
            #populating statistic_df
            statistic_df = rf.calculate_statistics(df_train)
            #print("\nStatistics Dataframe:")	
            #print(statistic_df)

            #converting to dictionary 
            statistic_dict = rf.df_to_dict(statistic_df)
            #print("\nStatistics Dictionary:")	
            #print(statistic_dict)


            ##############################################################################
            # Regression Coefficient related code
            ##############################################################################

            #finding out regression coefficients (based on number of columns having significant r)
            rc = rf.get_regression_coeff(statistic_df, df_train)
            #print("simple regression rc: ")
            #print(rc)

            ##############################################################################
            # Returning the results in the format required
            ##############################################################################

            coeff = rc                          #regression coefficient as a list
            result = dict()                     #statistics as a dictionary
            result["coeff"] = coeff
            result["stats"] = statistic_dict
            result["status"] = "success"
            return result

        except Exception as e:
            result = dict()
            result["coeff"] = {"error": str(e)}
            result["status"] = "failed"
            return result


    @staticmethod
    def score(df_input, dct_model):
        """
        :param df_input: A pandas Dataframe
        :param dct_model: A json model
        :return: df_output: A pandas dataframe
        """
        try:

            ##############################################################################
            # Taking only testing data
            ##############################################################################
                        
            #testing data - take only 30%           
            df_test = rf.testing_data(df_input)
        
            ##############################################################################
            # Get regression coefficients and stats from the model passed as parameter
            ##############################################################################

            coeff = dct_model.get('coeff')
            #print("coefficients: ")
            #print(coeff)

            statistic_dict = dct_model.get('stats')
            #print("statistics dict:")
            #print(stats_dict)
            statistic_df = rf.dict_to_df(statistic_dict)
            #print("statistics df:")
            
            #print(stats_df)

            ##############################################################################
            # Calculated Expected value of y
            ##############################################################################

            df_output = rf.calculated_expected_values(df_test, coeff, statistic_df)
            #print("output df:")
            #print(df_output)

            ##############################################################################
            # Returning the results in the format required
            ##############################################################################
            #df_output = pd.DataFrame({"a": [1,2,3], "b":[2,3,4]}) # this is testdata, replace with actual calculated data
            result = "success"
            error = None
            return result, df_output, error

        except Exception as e:

            result = "failed"
            df_output = pd.DataFrame() # send empty DF in case of failure
            error = str(e)
            return result, df_output, error


#main for testing

#sample_file_path = 'D:\\Hema\\Other\\CCE\\project\\employee salary.csv'
#input_df = rf.read_csv_into_df(sample_file_path)

#obj = simple_regression()
#my_result = obj.train(input_df)
#print(my_result)

#input_values= {'coeff': [None], 'stats': {'Mean': {'Salary (USDK)': 69.4, 'Education (years)': 12.8, 'Experience (years)': 2.4, 'Working hours (per week)': 46.0}, 'Variance': {'Salary (USDK)': 238.8, 'Education (years)': 7.199999999999999, 'Experience (years)': 2.3000000000000003, 'Working hours (per week)': 30.0}, 'Standard Deviation': {'Salary (USDK)': 15.453155017665487, 'Education (years)': 2.6832815729997477, 'Experience (years)': 1.5165750888103102, 'Working hours (per week)': 5.477225575051661}, 'Co-variance': {'Salary (USDK)': '-', 'Education (years)': 26.6, 'Experience (years)': 6.049999999999999, 'Working hours (per week)': 22.0}, 'Correlation Factor': {'Salary (USDK)': 0.8765386471799175, 'Education (years)': 0.6415023138586662, 'Experience (years)': 0.2581512875192245, 'Working hours (per week)': 0.2599231085030565}, 'Is r significant?': {'Salary (USDK)': '-', 'Education (years)': 'No', 'Experience (years)': 'No', 'Working hours (per week)': 'No'}}, 'status': 'success'}

#output_df = obj.score(input_df,input_values)
#print(output_df)
