import kfp
from kfp import dsl
from kfp.components import create_component_from_func

def downloadFile_op():

    return dsl.ContainerOp(
        name='Download Data',
        image='crysiss/download_file:0.1',
        arguments=[],
        file_outputs={
            'df_01': '/tmp/df_01.csv',
            'df_02': '/tmp/df_02.csv',
            'df_03': '/tmp/df_03.csv',
        }
    )





@dsl.pipeline(name='REC_XGBOOST Pipeline',
              description='A pipeline that trains and logs a classification model'
)
def data_pipeline():
    _downloadFile_op = downloadFile_op()


if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(data_pipeline, "data_pipeline.tar.gz")