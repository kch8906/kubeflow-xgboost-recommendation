import argparse
import joblib
import xgboost as xgb
import matplotlib.pyplot as plt

def XGBoost_train(x_tr, y_tr, x_val, y_val):
    dtr = xgb.DMatrix(data=x_tr, label=y_tr)
    dval = xgb.DMatrix(data=x_val, label=y_val)    
    
    params = { 'max_depth':5,
               'num_class':60,
               'eta':0.05,
               'objective':'multi:softprob',
               'eval_metric':'mlogloss',
             }
    num_rounds = 20
    
    eval_list = [(dtr,'train'),(dval,'eval')]
    evals_result = {}

    xgb_model = xgb.train(params = params, dtrain=dtr , num_boost_round=num_rounds, \
                          early_stopping_rounds=10, evals=eval_list, evals_result=evals_result )
    
    
    fig = plt.figure(figsize=(15, 17))
    plt.plot(evals_result['train']['mlogloss'])
    plt.plot(evals_result['eval']['mlogloss'])
    plt.xlabel('epochs')
    plt.ylabel('multi log loss')

    filename = 'xgb_model.model'
    joblib.dump(xgb_model, open(filename, 'wb'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x_tr')
    parser.add_argument('--y_tr')
    parser.add_argument('--x_val')
    parser.add_argument('--y_val')
    args = parser.parse_args()

    XGBoost_train(args.x_tr, args.y_tr, args.x_val, args.y_val)



