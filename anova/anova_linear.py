#import data from previous groups
import pandas as pd
import scipy.stats as ss

def annova(df, coeff):
    #need from previous groups
      
    k = len(df.columns) -1
    params = len(coeff)
    count = len(df)
    col_name_y=df.columns[0]
    
    if(params ==2):
        m = coeff[0]
        c = coeff[1]

        col_name_x = df.columns[1]

        df['ycal'] = [(m*df.loc[i][col_name_x]) + c for i in df.index]
    elif(params ==3):
        m1 = coeff[0]
        m2 = coeff[1]
        c  = coeff[2]

        col_name_x1 = df.columns[1]
        col_name_x2 = df.columns[2]

        df['ycal'] = [(m1*df.loc[i][col_name_x1]) + (m2*df.loc[i][col_name_x2]) + c for i in df.index]
    elif(params ==4):
        m1 = coeff[0]
        m2 = coeff[1]
        m3 = coeff[2]
        c  = coeff[3]

        col_name_x1 = df.columns[1]
        col_name_x2 = df.columns[2]
        col_name_x3 = df.columns[3]

        df['ycal'] = [(m1*df.loc[i][col_name_x1]) + (m2*df.loc[i][col_name_x2]) + (m3*df.loc[i][col_name_x3]) + c for i in df.index]
    else:
        return "Invalid input"

#    print 'yCap', yCap
    sse_list=[(df.loc[i][col_name_y]-df.loc[i]['ycal'])**2 for i in df.index]
#    print 'sqr(y-ycap)', sse_list
    SSE=sum(sse_list)
    print 'SSE= sum(( y-ycap )**2)=', SSE

    yBar= sum(df[col_name_y]) / len(df[col_name_y])
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

    

    #......Creating ANOVA Table...........
    source=[]
    DF=[]
    SS=[]
    MS=[]
    F=[]
    P=[]

    source.append('Regression')
    source.append('Error')
    source.append('Total')
    DF.append(dfR)
    DF.append(dfE)
    DF.append(dfT)
    SS.append(SSR)
    SS.append(SSE)
    SS.append(SST)
    MS.append(MSR)
    MS.append(MSE)
    MS.append('')
    F.append(F_stats)
    F.append('')
    F.append('')

    aTable = pd.DataFrame(columns=['source', 'DF', 'SS','MS', 'F'])
    for i in range(3):
        aTable = aTable.append({'source': source[i], 'DF':DF[i], 'SS':SS[i],'MS':MS[i], 'F':F[i]}, ignore_index=True)


    print '-------------------------------------------------------'
    print aTable
    print '-------------------------------------------------------'

