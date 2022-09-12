import boto3
import pandas as pd


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

    
if __name__ == "__main__":
    print("Downloading data..")
    s3_download()
    print("Download Success")

    print("Preprocessing data..")    
    df_customer = pd.read_csv('/tmp/df_customer.csv')
    df_purchase = pd.read_csv('/tmp/df_purchase.csv')
    df_product = pd.read_csv('/tmp/df_product.csv')
    df = preprocess(df_customer, df_purchase, df_product)

    df.to_csv('/tmp/df.csv')

