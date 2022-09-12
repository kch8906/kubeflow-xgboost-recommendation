import argparse
from io import StringIO
import pandas as pd

def load_data(data):    
    d = StringIO(data)
    _df = pd.read_csv(d, sep=',')

    return _df
         

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--df_customer', type=str)
    parser.add_argument('--df_purchase', type=str)
    parser.add_argument('--df_product', type=str)
    args = parser.parse_args()

    customer = args.df_customer
    df_customer = load_data(customer)
    purchase = args.df_purchase
    df_purchase = load_data(purchase)
    product = args.df_product
    df_product = load_data(product)
   
    # df_customer.drop('zon_hlv', axis=1, inplace=True)
    # df_purchase.drop(['rct_no', 'chnl_dv', 'br_c'], axis=1, inplace=True)
    # df_product.drop(['pd_nm', 'clac_mcls_nm'], axis=1, inplace=True)
    
    # df_merge_01_02 = pd.merge(df_purchase, df_customer, on='cust')
    # df_merge_01_02_03 = pd.merge(df_merge_01_02, df_product, on='pd_c')
    # df_merge_01_02_03.drop('pd_c', axis=1, inplace=True)
    
    # df = df_merge_01_02_03.sort_values('de_dt').reset_index(drop=True)  

    df_customer.to_csv("/tmp/df.csv")