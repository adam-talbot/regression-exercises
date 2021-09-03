####### REGRESSION WRANGLE EXERCISES #######

import pandas as pd
import numpy as np
import os
from env import host, user, password

##################### Acquire Zillow Data #####################

def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    It takes in a string name of a database as an argument.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
    
    
def new_zillow_sfr_data():
    '''
    This function reads the data from the Codeup db into a df and returns the df.
    '''
    # Create SQL query.
    sql_query = """
    select bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
    from properties_2017
    where propertylandusetypeid = 261;
    """
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df



def get_zillow_sfr_data():
    '''
    This function reads in data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('zillow_sfr_df.csv'):
        
        # If csv file exists, read in data from csv file.
        df = pd.read_csv('zillow_sfr_df.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame.
        df = new_zillow_sfr_data()
        
        # Write DataFrame to a csv file.
        df.to_csv('zillow_sfr_df.csv')
        
    return df

##################### Acquire and Prepare Zillow Data #####################

def wrangle_zillow():
    df = w.get_zillow_sfr_data()
    df = df.dropna()
    df = df.drop_duplicates()
    df.fips = '0' + df.fips.astype('int').astype('string')
    df.bedroomcnt = df.bedroomcnt.astype('int')
    df.calculatedfinishedsquarefeet = df.calculatedfinishedsquarefeet.astype('int')
    df.yearbuilt = df.yearbuilt.astype('int')
    num_cols = df.select_dtypes('number').columns.tolist()
    for col in num_cols:
        Q1 = np.percentile(df[col], 25, interpolation='midpoint')
        Q3 = np.percentile(df[col], 75, interpolation='midpoint')
        IQR = Q3 - Q1
        UB = Q3 + (1.5 * IQR)
        LB = Q1 - (1.5 * IQR)
        df = df[(df[col] < UB) & (df[col] > LB)]
    return df