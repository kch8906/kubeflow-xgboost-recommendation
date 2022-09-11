import boto3


def s3_download():
    s3_client = boto3.client('s3', region_name='ap-northeast-2',
                         aws_access_key_id='aws_access_key_id', 
                         aws_secret_access_key='aws_secret_access_key')

    bucket = 'changhyun-xgboost'
    filename = ['LPOINT_BIG_COMP_01_DEMO.csv', 'LPOINT_BIG_COMP_02_PDDE.csv', 'LPOINT_BIG_COMP_04_PD_CLAC.csv']
    object_name = ['df_customer.csv', 'df_purchase.csv', 'df_product.csv']

    for i in range(len(filename)):
        s3_client.download_file(bucket, filename[i], object_name[i])

    
    
if __name__ == "__main__":
    print("Downloading data..")
    s3_download()
