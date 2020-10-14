import pandas as pd
import numpy as np

def df_operations(sql_engine):
    """"""

    # Load dataset 1 into data frame 
    ds1 = """
    SELECT  ID AS DSId
            , API
            , WKID
    FROM    dbo.DirectionalSurvey WITH (READUNCOMMITTED);
    """
    df1 = pd.read_sql(ds1, sql_engine)
        
    print(f"DF1: {df1[df1.DSId > 0]}")

    # Load dataset 2 into data frame 
    ds2 = """
    SELECT  ID AS WellID
            , API
            , LATITUDE
            , LONGITUDE
    FROM    dbo.Well WITH (READUNCOMMITTED);
    """

    df2 = pd.read_sql(ds2, sql_engine)

    print(f"DF2: {df2[df2.WellID > 0]}")

    # Join dataset 1 and 2
    result = pd.merge(df1, df2, how='inner', on='API', indicator=True)

    # Update dataset add new derived column
    def tmp_fn(x, y):
        return x + y

    result["DerCol1"] = tmp_fn(result.LATITUDE, result.LONGITUDE)

    print(f"Merge: {result}")
    result2 = result.loc[:, ['DSId', 'API', 'WKID', 'LATITUDE', 'LONGITUDE', 'DerCol1']]

    # Export to SQL Server
    # Creates new table
    result2.to_sql('Results', sql_engine, schema='dbo', index=False, if_exists='replace')
