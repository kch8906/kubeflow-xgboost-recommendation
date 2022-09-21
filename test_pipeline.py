from ast import arguments
import kfp
from kfp import dsl
from kfp.components import OutputPath
from kfp import onprem


def convert_json():
    return dsl.ContainerOp(        
        name='Convert Data',
        image='crysiss/kubeflow-convertjson:0.2',
        arguments=[],
        file_outputs={
            'df_customer': '/tmp/df_customer.json',
            'df_purchase': '/tmp/df_purchase.json',
            'df_product': '/tmp/df_product.json'
        }        
    )

def preprocess_op(df_customer, df_purchase, df_product):
    return dsl.ContainerOp(
        name='Preprocess Data',
        image='crysiss/kubeflow-preprocess-a:0.3',
        arguments=[
            '--df_customer', df_customer,
            '--df_purchase', df_purchase,
            '--df_product', df_product
        ],
        file_outputs={
            'df': '/tmp/prerprocess.json'
        }
    )

def spilt_data_op(df):
    return dsl.ContainerOp(
        name='Split Data',
        image='crysiss/kubeflow-split-data:0.2',
        arguments=[
            '--df', df
            ],
        file_outputs={
            'x_tr': '/tmp/x_tr.json',
            'y_tr': '/tmp/y_tr.json',
            'x_val': '/tmp/x_val.json',
            'y_val': '/tmp/y_val.json',
            'x_test': '/tmp/x_test.json',
            'y_test': '/tmp/y_test.json'
        }
    )

def train_op(x_tr, y_tr, x_val, y_val):
    return dsl.ContainerOp(
        name='Train Model',
        image='crysiss/kubeflow-train:0.2',
        arguments=[
            '--x_tr', x_tr,
            '--y_tr', y_tr,
            '--x_val', x_val,
            '--y_val', y_val
            ],
        file_outputs={
            'model': '/tmp/xgb_model.pkl'
        }
    )

def test_op(x_test, y_test, model):
    return dsl.ContainerOp(
        name='Test Model',
        image='crysiss/kubeflow-test:0.5',
        arguments=[
            '--x_test', x_test,
            '--y_test', y_test,
            '--model', model
        ],
        file_outputs={
            'pred_probs': '/tmp/pred_probs.npy'
        }
    )

def extract_top_op(y_test, pred_probs):
    return dsl.ContainerOp(
        name='Extract Top5&10',
        image='crysiss/kubeflow-metric:0.1',
        arguments=[
            '--y_test', y_test,
            '--pred_probs', pred_probs
        ],
        file_outputs={
            'metrics': 'tmp/metrics.json'
        }
    )






@dsl.pipeline(name='XGBOOST-REC Pipeline',
              description='A pipeline that trains and logs a classification model'
)
def data_pipeline():   
    _convert_json = convert_json()

    _preprocess = preprocess_op(
        dsl.InputArgumentPath(_convert_json.outputs['df_customer']),
        dsl.InputArgumentPath(_convert_json.outputs['df_purchase']),
        dsl.InputArgumentPath(_convert_json.outputs['df_product'])
    ).after(_convert_json)

    _spilt_data_op = spilt_data_op(
        dsl.InputArgumentPath(_preprocess.outputs['df'])
    ).after(_preprocess)

    _train_op = train_op(
        dsl.InputArgumentPath(_spilt_data_op.outputs['x_tr']),
        dsl.InputArgumentPath(_spilt_data_op.outputs['y_tr']),
        dsl.InputArgumentPath(_spilt_data_op.outputs['x_val']),
        dsl.InputArgumentPath(_spilt_data_op.outputs['y_val'])
    ).after(_spilt_data_op)

    _test_op = test_op(
        dsl.InputArgumentPath(_spilt_data_op.outputs['x_test']),
        dsl.InputArgumentPath(_spilt_data_op.outputs['y_test']),
        dsl.InputArgumentPath(_train_op.outputs['model']),
    ).after(_train_op)

    _extract_top_op = extract_top_op(
        dsl.InputArgumentPath(_spilt_data_op.outputs['x_test']),
        dsl.InputArgumentPath(_test_op.outputs['pred_probs'])
    ).after(_test_op)



if __name__ == "__main__":
    import kfp.compiler as compiler

    host = 'http://127.0.0.1:8080/'
    namespace = 'kch'
    pipeline_name = 'XGBoost'    
    version = 'v0.1'
    run_name = f'kubeflow study {version}'
    experiment_name = 'xgboost_1'
    pipeline_path = 'xgboost_pipeline.yaml'

    compiler.Compiler().compile(data_pipeline, pipeline_path)
    # client = kfp.Client(host=host, namespace=namespace)

    # pipeline_id = client.get_pipeline_id(pipeline_name)
    # experiment = client.create_experiment(name=experiment_name, namespace=namespace)
    # client.run_pipeline(experiment.id, run_name, pipeline_path)

    
