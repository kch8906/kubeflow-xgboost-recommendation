import boto3


def s3_download():
    s3_client = boto3.client('s3', region_name='ap-northeast-2',
                         aws_access_key_id='AKIAWPQA2KXZ7LKY4PWI', 
                         aws_secret_access_key='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')

    bucket = 'changhyun-kubeflow'
    filename = ['LPOINT_BIG_COMP_01_DEMO.csv', 'LPOINT_BIG_COMP_02_PDDE.csv', 'LPOINT_BIG_COMP_05_BR.csv']
    object_name = ['df_01.csv', 'df_02.csv', 'df_03.csv']

    for i in range(len(filename)):
        s3_client.download_file(bucket, filename[i], object_name[i])

    
if __name__ == "__main__":
    print("Downloading data..")
    s3_download()