####### REGRESSION WRANGLE EXERCISES #######

import pandas as pd
import numpy as np
import os
from env import host, user, password
from sklearn.model_selection import train_test_split

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

def split_zillow(df):
    '''
    This function takes in a df and splits it into train, validate, and test dfs
    final proportions will be 80/10/10 for train/validate/test
    '''
    train_validate, test = train_test_split(df, test_size=0.10, random_state=123)
    train, validate = train_test_split(train_validate, test_size=.11, random_state=123)
    return train, validate, test

def wrangle_zillow_no_split():
    '''
    This function aquires and prepares zillow data
    Returns df
    '''
    df = get_zillow_sfr_data()
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

def wrangle_zillow():
    '''
    This function aquires, prepares, and splits zillow data
    Returns train, validate, and test dfs
    '''
    df = get_zillow_sfr_data()
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
    train, validate, test = split_zillow(df)
    return train, validate, test

def add_scaled_columns(train, validate, test, scaler, columns_to_scale):
    '''
    Add scaled copies of columns to train, validate, and split
    '''
    # new column names
    new_column_names = [c + '_scaled' for c in columns_to_scale]
    
    # Fit the scaler on the train
    scaler.fit(train[columns_to_scale])
    
    # transform train validate and test
    train = pd.concat([
        train,
        pd.DataFrame(scaler.transform(train[columns_to_scale]), columns=new_column_names, index=train.index),
    ], axis=1)
    
    validate = pd.concat([
        validate,
        pd.DataFrame(scaler.transform(validate[columns_to_scale]), columns=new_column_names, index=validate.index),
    ], axis=1)
    
    
    test = pd.concat([
        test,
        pd.DataFrame(scaler.transform(test[columns_to_scale]), columns=new_column_names, index=test.index),
    ], axis=1)
    
    return train, validate, test