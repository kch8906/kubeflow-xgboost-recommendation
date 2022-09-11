import kfp
from kfp import dsl
from kfp.components import create_component_from_func


def downloadFile_op():

    return dsl.ContainerOp(
        name='Download Data',
        image='crysiss/download_file:0.4',
        arguments=[],
        file_outputs={
            'df_customer': '/tmp/df_customer.csv',
            'df_purchase': '/tmp/df_purchase.csv',
            'df_product': '/tmp/df_product.csv',
        }
    )

def preprocessData_op(df_customer, df_purchase, df_product):

    return dsl.ContainerOp(
        name='Preprocess Data',
        image='crysiss/preprocess-data:0.7',
        arguments=[
            '--df_customer', df_customer,
            '--df_purchase', df_purchase,
            '--df_product', df_product
        ],
        file_outputs={
            'df': '/tmp/df.csv'
        }
    )


@dsl.pipeline(name='XGBOOST-REC Pipeline',
              description='A pipeline that trains and logs a classification model'
)
def data_pipeline():
    _downloadFile_op = downloadFile_op()

    _preprocessData_op = preprocessData_op(
        dsl.InputArgumentPath(_downloadFile_op.outputs['df_customer']),
        dsl.InputArgumentPath(_downloadFile_op.outputs['df_purchase']),
        dsl.InputArgumentPath(_downloadFile_op.outputs['df_product'])
    ).after(_downloadFile_op)


if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(data_pipeline, "data_pipeline5.tar.gz")