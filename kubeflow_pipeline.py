import kfp
from kfp import dsl
from kfp.components import create_component_from_func


def downloadFile_op():

    return dsl.ContainerOp(
        name='Preprocess_Data',
        image='crysiss/kubeflow-preprocess:0.2',
        arguments=[],
        file_outputs={
            'df': '/tmp/df.csv'
        }
    )


@dsl.pipeline(name='XGBOOST-REC Pipeline',
              description='A pipeline that trains and logs a classification model'
)
def data_pipeline():
    _downloadFile_op = downloadFile_op()

if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(data_pipeline, "data_pipeline2.tar.gz")