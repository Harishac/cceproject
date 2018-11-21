import pandas as pd  
pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000           
import math


def read_csv_into_df(file_path):
    #print(file_path)

    #read the CSV and store in dataframe 'df'
    my_df = pd.read_csv(file_path)

    #print the dataframe
    print("Data Frame: \n")
    print(my_df)
    
    #return the dataframe read
    return my_df


def get_xy(a1,b1,c1,a2,b2,c2):
    #The equations will be of the form:
    #a1x + b1y = c1
    #a2x + b2y = c2

    k = b2/b1                              #this eliminates y
    
    #finding x and y
    x = ((k*c1) - c2) / ((k*a1) - a2)
    y = (c1 - (a1*x)) / b1

    return([x,y])           #returning a list

def get_xyz(a1,b1,c1,d1,a2,b2,c2,d2,a3,b3,c3,d3):
    #The equations will be of the form:
    #a1x + b1y + c1z = d1
    #a2x + b2y + c2z = d2
    #a3x + b3y + c3z = d3

    #elimiating z
    k1 = c2/c1
    k2 = c3/c1

    #so, calulating the coefficents of the below resulting 2*2 equation:
    # (k1a1 - a2)x + (k1b1 - b2)y = (k1d1 - d2)
    # (k2a1 - a3)x + (k2b1 - b3)y = (k2d1 - d3)

    a1_new = (k1*a1) - a2
    b1_new = (k1*b1) - b2
    c1_new = (k1*d1) - d2
    a2_new = (k2*a1) - a3
    b2_new = (k2*b1) - b3
    c2_new = (k2*d1) - d3

    #call the function to solve 2 variable equation
    xy = get_xy(a1_new,b1_new,c1_new,a2_new,b2_new,c2_new)
    x = xy[0]
    y = xy[1]
    z = (d1 - (a1*x) - (b1*y)) / c1

    return([x,y,z])             #returning a list


def get_xyzw(a1,b1,c1,d1,e1,a2,b2,c2,d2,e2,a3,b3,c3,d3,e3,a4,b4,c4,d4,e4):
    #The equations will be of the form:
    #a1x + b1y + c1z + d1w = e1
    #a2x + b2y + c2z + d2w = e2
    #a3x + b3y + c3z + d3w = e3
    #a4x + b4y + c4z + d4w = e3

    #elimiating w
    k1 = d2/d1
    k2 = d3/d1
    k3 = d4/d1

    #so, calulating the coefficents of the below resulting 2*2 equation:
    # (k1a1 - a2)x + (k1b1 - b2)y + (k1c1 - c2)z = (k1d1 - d2)
    # (k2a1 - a3)x + (k2b1 - b3)y + (k2c1 - c3)z = (k2d1 - d3)
    # (k3a1 - a4)x + (k3b1 - b4)y + (k2c1 - c4)z = (k2d1 - d4)

    a1_new = (k1*a1) - a2
    b1_new = (k1*b1) - b2
    c1_new = (k1*c1) - c2
    d1_new = (k1*e1) - e2

    a2_new = (k2*a1) - a3
    b2_new = (k2*b1) - b3
    c2_new = (k2*c1) - c3
    d2_new = (k2*e1) - e3

    a3_new = (k3*a1) - a4
    b3_new = (k3*b1) - b4
    c3_new = (k3*c1) - c4
    d3_new = (k3*e1) - e4


    #call the function to solve 3 variable equation
    xyz = get_xyz(a1_new,b1_new,c1_new,d1_new,a2_new,b2_new,c2_new,d2_new,a3_new,b3_new,c3_new,d3_new)
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    w = (e1 - (a1*x) - (b1*y) - (c1*z)) / d1

    return([x,y,z,w])             #returning a list



#main code starts here
sample_file_path = '/home/rajendra/Downloads/cceproject-master/data.csv' #sample data.csv' #employee salary.csv'
df = read_csv_into_df(sample_file_path)

coeff=[]
#l contains number of columns
l = len(df.columns)

col_name_y = df.columns[0]  #we are assuming the dependent variable (y) will be the first column in the file


#k is used to store the number of independent columns where there is a significant correlation with y
k = l-1
sig_column_names = df.columns[1:]
count = len(df)
#looping through each independent variable


print("Regression Equation:\n")
print("Number of significant variables considered = "+ str(k))

#based on value of k, getting the coefficients for regression equations
if(k == 0 ):
    print("'y' does not have a significant linear relation with any of the input fields.")

elif(k == 1):
    #we need to find a1,b1,c1,a2,b2,c2
    a1 = b1 = c1 = 0 
    a2 = b2 = c2 = 0 

    col_name_x = sig_column_names[0]

    for i in df.index:        
        a1 = a1 + (df.loc[i][col_name_x]**2 )                                  #sum(x)
        c1 = c1 + df.loc[i][col_name_y]                                   #sum(y) 
        a2 = a2 + (df.loc[i][col_name_x]**4)         #sum(x**4)
        c2 = c2 + (df.loc[i][col_name_x] * df.loc[i][col_name_x] * df.loc[i][col_name_y])         #sum(x^2.y)
       
    b1 = count                                           #n  
    b2 = a1                                              #sum(x)
    
    print("a1 = " + str(a1)+"\tb1 = "+str(b1)+"\tc1 = "+str(c1)+"\na2 = "+str(a2)+"\tb2 = "+str(b2)+"\tc2 = "+str(c2)+"\n")

    coeff = get_xy(a1,b1,c1,a2,b2,c2)

    m = coeff[0]
    c = coeff[1]

    print("m = "+str(round(m,3)))
    print("c = "+str(round(c,3)))
    print("equation is:\ny = "+ str(round(m,3)) + "x + "+str(round(c,3)))
    print(col_name_y + " = " + str(round(m,3)) + " * " + col_name_x + " + "  + str(round(c,3)))

    #df['ycal'] = float('NaN')
    #for i in df.index:
    #    df.loc[i]['ycal'] = (m*df.loc[i][col_name_x]) + c

    df['ycal'] = [(m*(df.loc[i][col_name_x]**2)) + c for i in df.index]
    #print df

    sse_list=[(df.loc[i][col_name_y]-df.loc[i]['ycal'])**2 for i in df.index]
#    print 'sqr(y-ycap)', sse_list
    SSE=sum(sse_list)
    print 'SSE= sum(( y-ycap )**2)=', SSE

    yBar= c1/count
    #ssr_list=[]
    ssr_list= [(df.loc[i]['ycal']-yBar)**2 for i in df.index]
    SSR=sum(ssr_list)
    print 'SSR=sum((Ycap-Ybar)**2)=', SSR

    SST=SSE+SSR
    print 'SST= SSE + SSR         =', SST

    dfT=count-1
    dfR=k
    dfE=dfT-dfR
    print 'dfT=',dfT, 'dfR=',dfR, 'dfE=', dfE

    MSR=SSR/dfR
    MSE=SSE/dfE
    print 'MSR =',MSR, 'MSE=',  MSE
    
    F_stats=MSR/MSE
    print "F_stats = ", F_stats

elif(k == 2):
    #we need to find a1,b1,c1,d1,a2,b2,c2,d2,a3,b3,c3,d3
    a1 = b1 = c1 = d1 = 0
    a2 = b2 = c2 = d2 = 0
    a3 = b3 = c3 = d3 = 0 

    col_name_x1 = sig_column_names[0]
    col_name_x2 = sig_column_names[1]

    for i in df.index:        
        a1 = a1 + (df.loc[i][col_name_x1]**2)                               #sum(x1)
        b1 = b1 + (df.loc[i][col_name_x2]**2)                                   #sum(x2)
        d1 = d1 + df.loc[i][col_name_y]                                    #sum(y) 
        a2 = a2 + (df.loc[i][col_name_x1]**4)        #sum(x1 square)
        b2 = b2 + ((df.loc[i][col_name_x1]**2) * (df.loc[i][col_name_x2]**2))        #sum(x1.x2) 
        d2 = d2 + ((df.loc[i][col_name_x1]**2) * df.loc[i][col_name_y])         #sum(x1.y)
        b3 = b3 + (df.loc[i][col_name_x2]**4)        #sum(x2 square)
        d3 = d3 + ((df.loc[i][col_name_x2]**2) * df.loc[i][col_name_y])         #sum(x2.y)

    c1 = count                                           #n  
    c2 = a1                                              #sum(x1)
    c3 = b1                                              #sum(x2)
    a3 = b2                                              #sum(x1.x2)

    print("a1 = " + str(a1)+"\tb1 = "+str(b1)+"\tc1 = "+str(c1)+"\td1 = "+str(d1))
    print("a2 = " + str(a2)+"\tb2 = "+str(b2)+"\tc2 = "+str(c2)+"\td2 = "+str(d2))
    print("a3 = " + str(a3)+"\tb3 = "+str(b3)+"\tc3 = "+str(c3)+"\td3 = "+str(d3))

    coeff = get_xyz(a1,b1,c1,d1,a2,b2,c2,d2,a3,b3,c3,d3)

    m1 = coeff[0]
    m2 = coeff[1]
    c  = coeff[2]

    print("m1 = "+str(round(m1,3)))
    print("m2 = "+str(round(m2,3)))
    print("c  = "+str(round(c,3)))
    print("equation is:\ny = " + str(round(m1,3)) + "x1 + "+ str(round(m2,3)) + "x2 + " + str(round(c,3)))
    print(col_name_y + " = " + str(round(m1,3)) + " * " + col_name_x1 + " + " + str(round(m2,3)) + " * " + col_name_x2 + " + "   + str(round(c,3)))


    df['ycal'] = [(m1*(df.loc[i][col_name_x1]**2)) + (m2*(df.loc[i][col_name_x2]**2)) + c for i in df.index]
    #print df

    sse_list=[(df.loc[i][col_name_y]-df.loc[i]['ycal'])**2 for i in df.index]
#    print 'sqr(y-ycap)', sse_list
    SSE=sum(sse_list)
    print 'SSE= sum(( y-ycap )**2)=', SSE

    yBar= d1/count
    #ssr_list=[]
    ssr_list= [(df.loc[i]['ycal']-yBar)**2 for i in df.index]
    SSR=sum(ssr_list)
    print 'SSR=sum((Ycap-Ybar)**2)=', SSR

    SST=SSE+SSR
    print 'SST= SSE + SSR         =', SST

    dfT=count-1
    dfR=k
    dfE=dfT-dfR
    print 'dfT=',dfT, 'dfR=',dfR, 'dfE=', dfE

    MSR=SSR/dfR
    MSE=SSE/dfE
    print 'MSR =',MSR, 'MSE=',  MSE
    
    F_stats=MSR/MSE
    print "F_stats = ", F_stats


elif(k == 3):
    #we need to find a1,b1,c1,d1,e1,a2,b2,c2,d2,e2,a3,b3,c3,d3,e3,a4,b4,c4,d4,e4
    a1 = b1 = c1 = d1 = e1 = 0
    a2 = b2 = c2 = d2 = e2 = 0
    a3 = b3 = c3 = d3 = e3 = 0
    a4 = b4 = c4 = d4 = e4 = 0

    col_name_x1 = sig_column_names[0]
    col_name_x2 = sig_column_names[1]
    col_name_x3 = sig_column_names[2]

    for i in df.index:        
        a1 = a1 + (df.loc[i][col_name_x1]**2)                                  #sum(x1)
        b1 = b1 + (df.loc[i][col_name_x2]**2)                                   #sum(x2)
        c1 = c1 + (df.loc[i][col_name_x3]**2)                                   #sum(x3)
        e1 = e1 + df.loc[i][col_name_y]                                    #sum(y)
        
        a2 = a2 + (df.loc[i][col_name_x1]**4)        #sum(x1 square)
        b2 = b2 + ((df.loc[i][col_name_x1]**2) * (df.loc[i][col_name_x2]**2))        #sum(x1.x2) 
        c2 = c2 + ((df.loc[i][col_name_x1]**2) * (df.loc[i][col_name_x3]**2))        #sum(x1.x3) 
        e2 = e2 + ((df.loc[i][col_name_x1]**2) * df.loc[i][col_name_y])         #sum(x1.y)

        b3 = b3 + (df.loc[i][col_name_x2]**4)        #sum(x2 square)
        c3 = c3 + ((df.loc[i][col_name_x2]**2) * (df.loc[i][col_name_x3]**2))        #sum(x2.x3) 
        e3 = e3 + ((df.loc[i][col_name_x2]**2) * df.loc[i][col_name_y])         #sum(x2.y)

        c4 = c4 + (df.loc[i][col_name_x3]**4)        #sum(x3 square) 
        e4 = e4 + ((df.loc[i][col_name_x3]**2) * df.loc[i][col_name_y])         #sum(x3.y)

    d1 = count                                           #n  
    d2 = a1                                              #sum(x1)
    d3 = b1                                              #sum(x2)
    d4 = c1                                              #sum(x3)
    a3 = b2                                              #sum(x1.x2)
    a4 = c2                                              #sum(x1.x3)
    b4 = c3                                              #sum(x2.x3)

    print("a1 = " + str(a1)+"\tb1 = "+str(b1)+"\tc1 = "+str(c1)+"\td1 = "+str(d1)+"\te1 = "+str(e1))
    print("a2 = " + str(a2)+"\tb2 = "+str(b2)+"\tc2 = "+str(c2)+"\td2 = "+str(d2)+"\te2 = "+str(e2))
    print("a3 = " + str(a3)+"\tb3 = "+str(b3)+"\tc3 = "+str(c3)+"\td3 = "+str(d3)+"\te3 = "+str(e3))
    print("a4 = " + str(a4)+"\tb4 = "+str(b4)+"\tc4 = "+str(c4)+"\td3 = "+str(d4)+"\te3 = "+str(e4))

    coeff = get_xyzw(a1,b1,c1,d1,e1,a2,b2,c2,d2,e2,a3,b3,c3,d3,e3,a4,b4,c4,d4,e4)

    m1 = coeff[0]
    m2 = coeff[1]
    m3 = coeff[2]
    c  = coeff[3]

    print("m1 = "+str(round(m1,3)))
    print("m2 = "+str(round(m2,3)))
    print("m3 = "+str(round(m3,3)))
    print("c  = "+str(round(c,3)))
    print("equation is:\ny = " + str(round(m1,3)) + "x1 + " + str(round(m2,3)) + "x2 + " + str(round(m3,3)) + "x3 + " + str(round(c,3)))
    print(col_name_y + " = " + str(round(m1,3)) + " * " + col_name_x1 + " + " + str(round(m2,3)) + " * " + col_name_x2 + " + " + str(round(m3,3)) + " * " + col_name_x3 + " + "   + str(round(c,3)))

    df['ycal'] = [(m1*(df.loc[i][col_name_x1]**2)) + (m2*(df.loc[i][col_name_x2]**2)) + (m3*(df.loc[i][col_name_x3]**2)) + c for i in df.index]
    #print df

    sse_list=[(df.loc[i][col_name_y]-df.loc[i]['ycal'])**2 for i in df.index]
#    print 'sqr(y-ycap)', sse_list
    SSE=sum(sse_list)
    print 'SSE= sum(( y-ycap )**2)=', SSE

    yBar= d1/count
    #ssr_list=[]
    ssr_list= [(df.loc[i]['ycal']-yBar)**2 for i in df.index]
    SSR=sum(ssr_list)
    print 'SSR=sum((Ycap-Ybar)**2)=', SSR

    SST=SSE+SSR
    print 'SST= SSE + SSR         =', SST

    dfT=count-1
    dfR=k
    dfE=dfT-dfR
    print 'dfT=',dfT, 'dfR=',dfR, 'dfE=', dfE

    MSR=SSR/dfR
    MSE=SSE/dfE
    print 'MSR =',MSR, 'MSE=',  MSE
    
    F_stats=MSR/MSE
    print "F_stats = ", F_stats

else:
    print("Work In Progress...")

print coeff
print("\n")
