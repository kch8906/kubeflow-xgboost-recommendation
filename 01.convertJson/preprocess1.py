import boto3
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split



def s3_download():
    s3_client = boto3.client('s3', region_name='ap-northeast-2',
                         aws_access_key_id='AKIAVEWKFLQL3R3QD2UU', 
                         aws_secret_access_key='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')

    bucket = 'changhyun-xgboost'
    filename = ['LPOINT_BIG_COMP_01_DEMO.csv', 'LPOINT_BIG_COMP_02_PDDE.csv', 'LPOINT_BIG_COMP_04_PD_CLAC.csv']
    object_name = ['df_customer.csv', 'df_purchase.csv', 'df_product.csv']

    for i in range(len(filename)):
        s3_client.download_file(bucket, filename[i], object_name[i])


def preprocess(data1, data2, data3) -> pd.DataFrame:

    df_customer = data1.drop('zon_hlv', axis=1)
    df_purchase = data2.drop(['rct_no', 'chnl_dv', 'br_c'], axis=1)
    df_product = data3.drop(['pd_nm', 'clac_mcls_nm'], axis=1)
    
    df_merge_01_02 = pd.merge(df_purchase, df_customer, on='cust')
    df_merge_01_02_03 = pd.merge(df_merge_01_02, df_product, on='pd_c')
    df_merge_01_02_03.drop('pd_c', axis=1, inplace=True)
    
    _df = df_merge_01_02_03.sort_values('de_dt').reset_index(drop=True)

    return _df

def convertLabel(df) -> pd.DataFrame:
    for colName in df.columns:
        globals()[f'encoder_{colName}'] = LabelEncoder()
        globals()[f'encoder_{colName}'].fit(df[colName])
        df[colName] = globals()[f'encoder_{colName}'].transform(df[colName])  

    return df

def split_train_test(df) -> pd.DataFrame:
    x = df.drop(columns='clac_hlv_nm', axis=1)
    y = df['clac_hlv_nm']
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=156)
    X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=156)
    
    np.save('x_train.npy', X_train)
    np.save('x_test.npy', X_test)
    np.save('y_train.npy', y_train)
    np.save('y_test.npy', y_test)
    np.save('x_tr.npy', X_tr)
    np.save('x_val.npy', X_val)
    np.save('y_tr.npy', y_tr)
    np.save('y_val.npy', y_val)   

    
if __name__ == "__main__":
    print("Downloading data..")
    s3_download()
    print("Download Success")

    print("Preprocessing data..")    
    df_customer = pd.read_csv('/tmp/df_customer.csv')
    df_purchase = pd.read_csv('/tmp/df_purchase.csv')
    df_product = pd.read_csv('/tmp/df_product.csv')
    df = preprocess(df_customer, df_purchase, df_product)
    le_df = convertLabel(df)
    split_train_test(le_df)


