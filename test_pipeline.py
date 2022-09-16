from ast import arguments
import kfp
from kfp import dsl
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
        image='crysiss/kubeflow-split-data:0.1',
        arguments=[
            '--df', df
            ],
        file_outputs={
            'x_tr': '/tmp/x_tr.npy',
            'y_tr': '/tmp/y_tr.npy',
            'x_val': '/tmp/x_val.npy',
            'y_val': '/tmp/y_val.npy',
            'x_test': '/tmp/x_test.npy',
            'y_test': '/tmp/y_test.npy'
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


if __name__ == "__main__":
    import kfp.compiler as compiler

    host = 'http://127.0.0.1:8080/'
    namespace = 'kch'
    pipeline_name = 'XGBoost'    
    version = 'v0.1'
    run_name = f'kubeflow study {version}'
    experiment_name = 'xgboost_1'
    pipeline_path = 'pipeline.tar.gz'

    compiler.Compiler().compile(data_pipeline, pipeline_path)
    # client = kfp.Client(host=host, namespace=namespace)

    # pipeline_id = client.get_pipeline_id(pipeline_name)
    # experiment = client.create_experiment(name=experiment_name, namespace=namespace)
    # client.run_pipeline(experiment.id, run_name, pipeline_path)

    
