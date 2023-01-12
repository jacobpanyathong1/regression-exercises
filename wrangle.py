import pandas as pd
import env
import os

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

def wrangle_zillow(df):
    df.calculatedfinishedsquarefeet.fillna(value=1868.28, inplace=True) #fillna mean for sqft
    df.taxvaluedollarcnt.fillna(value=4.58, inplace=True) #fillna mean for dollar
    df.yearbuilt.fillna(value=1961.19, inplace=True) #fillna mean for yearbuilt
    df.taxamount.fillna(value=5.59, inplace=True) #fillna mean for taxamount
    return df