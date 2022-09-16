import kfp
from kfp import dsl
from kfp import onprem


@dsl.pipeline(name='XGBOOST-REC Pipeline',
              description='A pipeline that trains and logs a classification model'
)
def data_pipeline():
    vop = dsl.VolumeOp(
        name='kfp_pvc',
        resource_name='kube-pvc',
        size='5Gi',
        modes=dsl.VOLUME_MODE_RWM
    )

    step1 = dsl.ContainerOp(        
        name='Preprocess Data',
        image='crysiss/test-kubeflow:0.1',
        arguments=[],
        file_outputs={},
        pvolumes={"/mnt": vop.volume}
    )

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

    


    