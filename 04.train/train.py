import argparse
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import json
import dill


def readJson(path: str):
    with open(f'{path}') as f:
        js = json.loads(f.read()) 
        df = pd.DataFrame(js)        

    return df


def XGBoost_train(x_tr, y_tr, x_val, y_val) -> pd.DataFrame:
    dtr = xgb.DMatrix(data=x_tr, label=y_tr)
    dval = xgb.DMatrix(data=x_val, label=y_val)    
    
    params = { 'max_depth':15,
               'num_class':60,
               'eta':0.05,
               'objective':'multi:softprob',
               'eval_metric':'mlogloss',
             }
    num_rounds = 10
    
    eval_list = [(dtr,'train'),(dval,'eval')]
    evals_result = {}

    xgb_model = xgb.train(params = params, dtrain=dtr , num_boost_round=num_rounds, \
                          early_stopping_rounds=10, evals=eval_list, evals_result=evals_result )
    
    
    # fig = plt.figure(figsize=(15, 17))
    # plt.plot(evals_result['train']['mlogloss'])
    # plt.plot(evals_result['eval']['mlogloss'])
    # plt.xlabel('epochs')
    # plt.ylabel('multi log loss')

    model_path = '/tmp/xgb_model.pkl'
    
    with open(f'{model_path}', 'wb') as f:
        dill.dump(xgb_model, f)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x_tr')
    parser.add_argument('--y_tr')
    parser.add_argument('--x_val')
    parser.add_argument('--y_val')
    args = parser.parse_args()

    x_tr = readJson(args.x_tr)
    y_tr = readJson(args.y_tr)
    x_val = readJson(args.x_val)
    y_val = readJson(args.y_val)

    XGBoost_train(x_tr, y_tr, x_val, y_val)





