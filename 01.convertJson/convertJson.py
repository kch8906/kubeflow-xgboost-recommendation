import csv
import boto3
import json
import json, pandas as pd
    
def s3_download():
    s3_client = boto3.client('s3', region_name='ap-northeast-2',
                         aws_access_key_id='aws_access_key_id', 
                         aws_secret_access_key='aws_secret_access_key')

    bucket = 'changhyun-xgboost'
    filenames = ['LPOINT_BIG_COMP_01_DEMO.csv', 'LPOINT_BIG_COMP_02_PDDE.csv', 'LPOINT_BIG_COMP_04_PD_CLAC.csv']
    object_name = ['df_customer.csv', 'df_purchase.csv', 'df_product.csv']

    for i in range(len(filenames)):
        s3_client.download_file(bucket, filenames[i], object_name[i])


def convert_json(df: pd.DataFrame, jsonname: str):
    df.to_json(f"{jsonname}.json", orient = "records")  


if __name__ == "__main__":
    print("Downloading data..")
    s3_download()
    print("Download Success")

    data_file_path = '/tmp/'
    csvNames = ['df_customer', 'df_purchase', 'df_product']


    for csvName in csvNames:
        path = ''.join(data_file_path + csvName + '.csv')
        df = pd.read_csv(path, low_memory=False)
        convert_json(df, csvName)
        

        