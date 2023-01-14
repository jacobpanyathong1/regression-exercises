import pandas as pd
import env
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
import matplotlib.pyplot as plt
import seaborn as sns


def sql_query_zillow():
    sql_connection = env.get_connection('zillow')
    filename = "zillow_2017.csv"       #iris CSV
    if os.path.isfile(filename):
        return pd.read_csv(filename)        # filename returned in system files
    else:
        df = pd.read_sql('''SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, taxvaluedollarcnt, yearbuilt, taxamount, fips
        FROM predictions_2017 as a
        JOIN properties_2017 as b
        USING (id)
        JOIN propertylandusetype as c
        USING (propertylandusetypeid)
        WHERE propertylandusedesc = "Single Family Residential";''', sql_connection)      # Read the SQL query into a dataframe
        df.to_csv(filename)        # Write that dataframe to save csv file. //"caching" the data for later.
        return df

def clean_zillow(df):
    df.drop(columns='Unnamed: 0', inplace=True)
    df.calculatedfinishedsquarefeet.fillna(value=1868.28, inplace=True) #fillna mean for sqft
    df.taxvaluedollarcnt.fillna(value=4.58, inplace=True) #fillna mean for dollar
    df.yearbuilt.fillna(value=1961.19, inplace=True) #fillna mean for yearbuilt
    df.taxamount.fillna(value=5.59, inplace=True) #fillna mean for taxamount
    df.columns = ['bedrooms', 'bathrooms', 'sqft', 'taxdollars', 'year', 'taxes', 'fips']
    return df 

def rts_formu():
    df = sql_query_zillow()
    df = clean_zillow(df)
    return df 

def train_validate_test(df):
    train_validate, test = train_test_split(df, train_size =.2, random_state = 100)
    train, validate = train_test_split(train_validate, train_size=.4, random_state = 100)
    return test, validate, train

def pull_tvt_formu():
    df = rts_formu()
    test, validate, train = train_validate_test(df)
    return test, validate, train


def xy_formula(train, validate, test):
    x_train = train.drop(columns=['taxes'])
    y_train = train['taxes']

    x_validate = validate.drop(columns=['taxes'])
    y_validate = validate['taxes']

    x_test = test.drop(columns=['taxes'])
    y_test = test['taxes']

    return x_train, y_train, x_validate, y_validate, x_test, y_test

def plot_variable_pairs():
    train, validate, test = pull_tvt_formu()
    x_train, y_train, x_validate, y_validate, x_test, y_test = xy_formula(train, validate, test)
    cont_var = ['bedrooms', 'bathrooms', 'sqft','taxdollars', 'year', 'taxes', 'fips']

    for col in cont_var:
        plt.hist(train[col], bins =25)
        plt.title(f'{col} distribution')
        plt.show()
        sns.relplot(x='taxdollars', y='taxes', data=train)
        plt.show()
        sns.lmplot(x='taxdollars', y='taxes', data=train)
        plt.show()
def rs_formula(train):
    rs_scaler = RobustScaler()
    rs_scaler.fit(train[['sqft', 'taxdollars', 'taxes', ]])
    more_trouble = rs_scaler.transform((train[['sqft', 'taxdollars', 'taxes', ]]))
    plt.subplot(121)
    plt.hist(train[['sqft', 'taxdollars', 'taxes']], bins=8)
    plt.title('Original data')

    plt.subplot(122)
    plt.hist(more_trouble, bins=8)
    plt.title('Transformed data')
    plt.show()


    