import argparse
import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder


def readJson(path: str):
    with open(f'{path}') as f:
        js = json.loads(f.read()) 
        df = pd.DataFrame(js)        

    return df

def merge_frame(frame1, frame2, frame3) -> pd.DataFrame:

    frame1 = frame1.drop('zon_hlv', axis=1)
    frame2 = frame2.drop(['rct_no', 'chnl_dv', 'br_c'], axis=1)
    frame3 = frame3.drop(['pd_nm', 'clac_mcls_nm'], axis=1)
    
    df_merge_01_02 = pd.merge(frame2, frame1, on='cust')
    df_merge_01_02_03 = pd.merge(df_merge_01_02, frame3, on='pd_c')
    df_merge_01_02_03 = df_merge_01_02_03.drop('pd_c', axis=1)
    
    df = df_merge_01_02_03.sort_values('de_dt').reset_index(drop=True)   
    
    return df

def labelEncoding(frame: pd.DataFrame):
    for colName in frame.columns:
        globals()[f'encoder_{colName}'] = LabelEncoder()
        globals()[f'encoder_{colName}'].fit(frame[colName])
        frame[colName] = globals()[f'encoder_{colName}'].transform(frame[colName])

    return frame



if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--df_customer')
    parser.add_argument('--df_purchase')
    parser.add_argument('--df_product')
    args = parser.parse_args()

    df_customer = readJson(args.df_customer)
    df_purchase = readJson(args.df_purchase)
    df_product = readJson(args.df_product)

    merge_df = merge_frame(df_customer, df_purchase, df_product)
    df = labelEncoding(merge_df)

    df.to_json("/tmp/prerprocess.json", orient = "records")
    



